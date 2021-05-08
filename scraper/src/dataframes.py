

import pandas as pd
import re
import os

def get_receiver(text):
    receiver = re.findall(r'^@([a-zA-Z0-9_-]+):', text)

    if any(receiver):
        return receiver[0]
    
    return None
 
def get_mentions(text):
    mentions = re.findall(r'@([a-zA-Z0-9_-]+)[: ]', text)

    return mentions

def get_hashtags(text):
    return re.findall(r'\W(\#[a-zA-Z0-9]+\b)(?!;)', text)

def entries_dataframe(entries):
    entry_id, date, text, author_login  = [], [], [], []
    vote_count, comments_count, status, url = [], [], [], []
    receiver = []

    for e in entries:
        if not e:
            continue

        entry_id.append(e.get('id'))
        date.append(e.get('date'))
        text.append(e.get('body'))
        author_login.append(e.get('author').get('login'))
        vote_count.append(e.get('vote_count'))
        comments_count.append(e.get('comments_count'))
        status.append(e.get('status'))
        url.append(e.get('url'))
        receiver.append(get_receiver(e.get('body', '')))

    data = {'entry_id': entry_id, 'date': date, 'text': text,
            'author_login': author_login, 'vote_count': vote_count,
            'comments_count': comments_count, 'status': status,
            'url': url, 'receiver': receiver
            }

    df = pd.DataFrame.from_dict(data)

    return df


def links_dataframe(links):
    link_id, date, description, tags  = [], [], [], []
    source_url, vote_count, bury_count, comment_count = [], [], [], []
    related_count, author_login, plus18, status, is_hot = [], [], [], [], []
    
    for e in links:
        if not e:
            continue

        link_id.append(e.get('id'))
        date.append(e.get('date'))
        description.append(e.get('description', ''))
        tags.append(e.get('tags', ''))
        source_url.append(e.get('source_url', ''))
        vote_count.append(e.get('vote_count'))
        bury_count.append(e.get('bury_count'))
        comment_count.append(e.get('comment_count'))
        related_count.append(e.get('related_count'))
        author_login.append(e.get('author').get('login'))
        plus18.append(e.get('plus18'))
        status.append(e.get('status'))
        is_hot.append(e.get('is_hot'))

    data = {'link_id': link_id, 'date': date, 'description': description,
            'tags': tags, 'source_url': source_url,
            'vote_count': vote_count, 'bury_count': bury_count,
            'comment_count': comment_count, 'related_count': related_count,
            'author_login': author_login, 'plus18': plus18,
            'status': status, 'is_hot': is_hot
            }

    df = pd.DataFrame.from_dict(data)

    return df

def entries_comments_dataframe(entries):
    comments = []
    for e in entries:
        if not e:
            continue

        if 'comments' in e:
            comments.extend(e['comments'])

    comment_id, entry_id, date, text, author_login  = [], [], [], [], []
    vote_count, status, receiver = [], [], []

    for c in comments:
        if not c:
            continue

        comment_id.append(c.get('id'))
        entry_id.append(c.get('entry_id'))
        date.append(c.get('date'))
        text.append(c.get('body'))
        author_login.append(c.get('author').get('login'))
        vote_count.append(c.get('vote_count'))
        status.append(c.get('status'))
        receiver.append(get_receiver(c.get('body', '')))

    data = {'comment_id': comment_id, 'entry_id': entry_id, 'date': date,
            'text': text, 'author_login': author_login,
            'vote_count': vote_count, 'status': status,
            'receiver': receiver
            }
            
    df = pd.DataFrame.from_dict(data)

    return df

def links_comments_dataframe(links):
    comments = []
    for e in links:
        if not e:
            continue

        if 'comments' in e:
            comments.extend(e['comments'])

    comment_id, link_id, date, text, author_login  = [], [], [], [], []
    vote_count, status, vote_count_plus, vote_count_minus, parent_id = [], [], [], [], []
    

    for c in comments:
        if not c:
            continue

        comment_id.append(c.get('id'))
        link_id.append(c.get('link_id'))
        date.append(c.get('date'))
        text.append(c.get('body'))
        author_login.append(c.get('author').get('login'))
        vote_count.append(c.get('vote_count'))
        vote_count_plus.append(c.get('vote_count_plus'))
        vote_count_minus.append(c.get('vote_count_minus'))
        parent_id.append(c.get('parent_id'))

    data = {'comment_id': comment_id, 'link_id': link_id, 'date': date,
            'text': text, 'author_login': author_login,
            'vote_count': vote_count, 'vote_count_plus': vote_count_plus,
            'vote_count_minus': vote_count_minus, 'parent_id': parent_id
            }
            
    df = pd.DataFrame.from_dict(data)

    return df

def user_dataframe(user_profiles):
    login, color, sex, avatar  = [], [], [], []
    signup_at, links_added_count, links_published_count, comments_count = [], [], [], []
    rank, followers, following, entries, entries_comments = [], [], [], [], []
    diggs, about, city, background, www, name = [], [], [], [], [], []
    
    for e in user_profiles:
        if not e:
            continue

        login.append(e.get('login'))
        color.append(e.get('color'))
        sex.append(e.get('sex'))
        avatar.append(e.get('avatar'))
        signup_at.append(e.get('signup_at'))
        links_added_count.append(e.get('links_added_count'))
        links_published_count.append(e.get('links_published_count'))
        comments_count.append(e.get('comments_count'))
        rank.append(e.get('rank'))
        followers.append(e.get('followers'))
        following.append(e.get('following'))
        entries.append(e.get('entries'))
        entries_comments.append(e.get('entries_comments'))

        diggs.append(e.get('diggs'))
        about.append(e.get('about'))
        city.append(e.get('city'))
        background.append(e.get('background'))
        www.append(e.get('www'))
        name.append(e.get('name'))

    data = {'login': login, 'color': color, 'sex': sex,
            'avatar': avatar, 'signup_at': signup_at,
            'links_added_count': links_added_count, 'links_published_count': links_published_count,
            'comments_count': comments_count, 'rank': rank,
            'followers': followers, 'following': following,
            'entries': entries, 'entries_comments': entries_comments,
            'diggs': diggs, 'about': about,
            'city': city, 'background': background,
            'www': www, 'name': name,
            }

    df = pd.DataFrame.from_dict(data)

    return df

def entries_tags_dataframe(entries):
    entry_id, comment_id, tag = [], [], [] 
    for e in entries:

        if not e:
            continue

        for t in get_hashtags(e.get('body', '')):
            entry_id.append(e['id'])
            comment_id.append(None)
            tag.append(t)
        
        for c in e.get('comments', []):
            for t in get_hashtags(c.get('body', '')):
                entry_id.append(int(e['id']))
                comment_id.append(int(c['id']))
                tag.append(t)

        data = {'entry_id': entry_id, 'comment_id': comment_id, 'tag': tag }
            
    df = pd.DataFrame.from_dict(data)

    return df

def entries_mentions_dataframe(entries):
    entry_ids, comment_ids, mentions = [], [], [] 
    for e in entries:
        if not e:
            continue

        entry_id = int(e['id'])

        for m in get_mentions(e.get('body', '')):
            entry_ids.append(entry_id)
            comment_ids.append(None)
            mentions.append(m)
        
        for c in e.get('comments', []):
            comment_id = int(c['id'])
            comment_text = c.get('body', '')
            for m in get_mentions(comment_text):
                entry_ids.append(entry_id)
                comment_ids.append(comment_id)
                mentions.append(m)

        data = {'entry_id': entry_ids, 'comment_id': comment_ids, 'mention': mentions}
            
    df = pd.DataFrame.from_dict(data)

    return df

def create_dataframes(folder, entries_full):
    entries_df = entries_dataframe(entries_full)
    entries_comments_df = entries_comments_dataframe(entries_full)
    entries_tags_df = entries_tags_dataframe(entries_full)
    entries_mentions_df = entries_mentions_dataframe(entries_full)

    entries_df.to_csv(os.path.join(folder, 'entries.csv'), index=False)
    entries_comments_df.to_csv(os.path.join(folder, 'comments.csv'), index=False)
    entries_tags_df.to_csv(os.path.join(folder, 'tags.csv'), index=False)
    entries_mentions_df.to_csv(os.path.join(folder, 'mentions.csv'), index=False)

def create_links_dataframes(folder, links_full):
    links_df = links_dataframe(links_full)
    links_comments_df = links_comments_dataframe(links_full)
    links_tags_df = entries_tags_dataframe(links_full)
    links_mentions_df = entries_mentions_dataframe(links_full)

    links_df.to_csv(os.path.join(folder, 'links.csv'), index=False)
    links_comments_df.to_csv(os.path.join(folder, 'comments.csv'), index=False)
    links_tags_df.to_csv(os.path.join(folder, 'tags.csv'), index=False)
    links_mentions_df.to_csv(os.path.join(folder, 'mentions.csv'), index=False)


def create_userss_dataframes(folder, profiles):
    profiles_df = user_dataframe(profiles)
    profiles_df.to_csv(os.path.join(folder, 'profiles.csv'), index=False)
    