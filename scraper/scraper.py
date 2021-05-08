import numpy as np
import pandas as pd
import os, re, json
from src.dataframes import create_dataframes, create_links_dataframes, create_userss_dataframes
from wykop_api import Wykop
from datetime import datetime, timedelta
import traceback
import tqdm

def filter_stream(stream, date_from=None, date_to=None, limit=0):
    posts = []
    for p in stream:
        if date_from is not None and p['date'] < date_from:
            break
        if len(posts) > limit:
            break
        if date_to is not None and p['date'] > date_to:
            continue
        #if p['comments_count'] == 0 and p['vote_count'] < 3:
            #continue
        
        posts.append(p)
    
    return posts

def scrape_all(folder=None, date_from=None, date_to=None, limit=0, last_entry_id=0):

    if folder is None:
        folder = f"./data/{datetime.now().strftime('%Y_%m_%d__%H_%M_%S')}/"
    os.makedirs(folder, exist_ok=True)

    w = Wykop()

    if not last_entry_id:
        last_entry_id = int(next(w.entries_all(1))['id'])

    entries_full = []

    for e_id in range(last_entry_id, 0, -25):
        try:
            e = w.entry(e_id)
            if not e or not e.get('data'):
                continue

            e = e['data']

            if date_from is not None and e['date'] < date_from:
                break
            if date_to is not None and e['date'] > date_to:
                continue
            if e['comments_count'] == 0 and e['vote_count'] < 3:
                continue

            entries_full.append(e)
            num_entries = len(entries_full)
            print(e.get('date'))
            print(f'Num entries = {num_entries}')

            if limit > 0 and num_entries >= limit:
                break
            
        except Exception as e:
            print(traceback.format_exc())

    def myconverter(o):
        if isinstance(o, datetime):
            return o.__str__()

    with open(os.path.join(folder, 'data.json'), 'w') as outfile:
        json.dump(entries_full, outfile, default=myconverter)

    create_dataframes(folder, entries_full)


def scrape_all_links(folder=None, limit=0, last_link_id=0):

    if folder is None:
        folder = f"./data/{datetime.now().strftime('links_%Y_%m_%d__%H_%M_%S')}/"
    os.makedirs(folder, exist_ok=True)

    w = Wykop()

    if not last_link_id:
        last_link_id = int(next(w.upcoming_links(1))['id'])

    links_full = []

    for l_id in range(last_link_id, 0, -1):
        try:
            link = w.link(l_id)
            if not link or not link.get('data'):
                continue

            link = link['data']

            if link['comments_count'] == 0 and link['vote_count'] < 3:
                continue

            links_full.append(link)
            num_links = len(links_full)
            print(link.get('date'))
            print(f'Num entries = {num_links}')

            if limit > 0 and num_links >= limit:
                break
            
        except Exception as e:
            print(traceback.format_exc())

    def myconverter(o):
        if isinstance(o, datetime):
            return o.__str__()

    with open(os.path.join(folder, 'data.json'), 'w') as outfile:
        json.dump(links_full, outfile, default=myconverter)

    create_links_dataframes(folder, links_full)


def scrape_users(user_logins, folder=None):
    if folder is None:
        folder = f"./data/{datetime.now().strftime('users_%Y_%m_%d__%H_%M_%S')}/"
    os.makedirs(folder, exist_ok=True)

    w = Wykop()

    total_users = len(user_logins)
    profiles = []

    for u_login in tqdm.tqdm(user_logins, total=total_users):
        try:
            user_profile = w.user_profile(u_login)
            if not user_profile or not user_profile.get('data'):
                print('error:', u_login, user_profile)
                continue

            user_profile = user_profile['data']

            profiles.append(user_profile)
            num_profiles = len(profiles)
            #print(f'Num profiles = {num_profiles} ({total_users} total)')
        except Exception as e:
            print(traceback.format_exc())

    def myconverter(o):
        if isinstance(o, datetime):
            return o.__str__()

    with open(os.path.join(folder, 'data.json'), 'w') as outfile:
        json.dump(profiles, outfile, default=myconverter)

    create_userss_dataframes(folder, profiles)


if __name__ == '__main__':
    scrape_all_links()
    #date_from = datetime.now() - timedelta(hours=2)
    #date_to = datetime.now() - timedelta(hours=1)

    #scrape_all(date_from=None, date_to=date_to, limit=100000)
    #comments = pd.read_csv('./wykop_scraper/data/latest/comments.csv').dropna(subset=['text'])
    #users = comments.author_login.dropna().tolist() + comments.receiver.dropna().tolist()
    #users = list(set(users))
    #scrape_users(users[:])