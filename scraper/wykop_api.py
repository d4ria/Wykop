
import json
import datetime
import itertools
import requests as r
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import SSLError, ReadTimeout
import time

class Wykop:

    def __init__(self, api_key='aNd401dAPp', api_secret=''):

        self.api_key = api_key
        self.api_secret = api_secret

    """ API METHODS """
    def entries_all(self, start_page=1, limit=50, page_step=1):
        method_url = 'https://a2.wykop.pl/Entries/Stream/'
        data = {'page':start_page, 'firstid':'1'}

        return self._paginated_stream(method_url, data, {}, limit, page_step=page_step)

    def entries_hot(self, limit=50):
        method_url = 'https://a2.wykop.pl/Entries/Hot/'
        data = {'page':'1', 'period':'24'}

        return self._paginated_stream(method_url, data, {}, limit)

    def entries_active(self, limit=50):
        method_url = 'https://a2.wykop.pl/Entries/Active/'
        data = {'page':'1'}

        return self._paginated_stream(method_url, data, {}, limit)

    def entry(self, entry_id):
        method_url = f'https://a2.wykop.pl/Entries/Entry/{entry_id}/'

        return self._get(method_url)
        
    def entry_voters(self, entry_id):
        method_url = f'https://a2.wykop.pl/Entries/Upvoters/{entry_id}/'

        return self._get(method_url, {})

    def entry_comment(self, comment_id):
        method_url = f'https://a2.wykop.pl/Entries/Comment/{comment_id}/'

        return self._get(method_url, {})

    def hits(self):
        method_url = 'https://a2.wykop.pl/Hits/Popular/'

        return self._get(method_url)
        
    def promoted_links(self, limit=50):
        method_url = 'https://a2.wykop.pl/Links/Promoted/'
        data = {'page':'1'}
        
        return self._paginated_stream(method_url, data, {}, limit)

    def upcoming_links(self, limit=50):
        method_url = 'https://a2.wykop.pl/Links/Upcoming/'
        data = {'page':'1'}
        
        return self._paginated_stream(method_url, data, {}, limit)

    def link(self, link_id, with_comments=True):
        method_url = f'https://a2.wykop.pl/Links/Link/{link_id}/withcomments/{with_comments}/'

        return self._get(method_url)

    def top_links(self, year, month=None, limit=50):
        method_url = f'https://a2.wykop.pl/Links/Top/{year}/'

        if month:
            method_url = method_url + f'{month}/'
        
        return self._get(method_url)

    def link_comments(self, link_id, sort='old'):
        method_url = f'https://a2.wykop.pl/Links/Comments/{link_id}/sort/{sort}/'

        return self._get(method_url)['data']

    def link_comment(self, comment_id):
        method_url = f'https://a2.wykop.pl/Links/Comment/{comment_id}'

        return self._get(method_url)

    def user_profile(self, login):
        method_url = f'https://a2.wykop.pl/Profiles/Index/{login}/'
        
        return self._get(method_url)

    def search_links(self, q, what='all', sort='best', when='all', votes='0',
                    date_from=None, date_to=None, limit=50):
        """ 
        q - query string (min 3 chars)
        what - type of links (all, promoted, archived, duplicates)
        sort - sorting (best, diggs, comments, new)
        when - date range (all, today, yesterday, week, month, range)
        votes - minimum vote count
        date_from - from date (YYYY-MM-DD)
        date_to - to date (YYYY-MM-DD)
        """
        method_url = f'https://a2.wykop.pl/Search/Links/{q}'
        data = {}
        post_data = {
            'page': 1,
            'what': what,
            'sort': sort,
            'when': when,
            'votes': votes,
            'from': date_from,
            'to': date_to,
        }

        if q:
            post_data['q'] = q
        
        return self._paginated_stream(method_url, data, post_data, limit)

    def search_entries(self, q='', what='all', sort='best', when='all', votes='0',
                    date_from=None, date_to=None, limit=50):
        """ 
        q - query string (min 3 chars)
        what - type of links (all, promoted, archived, duplicates)
        sort - sorting (best, diggs, comments, new)
        when - date range (all, today, yesterday, week, month, range)
        votes - minimum vote count
        date_from - from date (YYYY-MM-DD)
        date_to - to date (YYYY-MM-DD)
        """
        method_url = f'https://a2.wykop.pl/Search/Entries/'
        data = {}
        post_data = {
            'page': 1,
            'when': when,
            'votes': votes,
            'from': date_from,
            'to': date_to,
        }

        if q:
            post_data['q'] = q

        return self._paginated_stream(method_url, data, post_data, limit)

    def tag_index(self, tag, limit=50):
        method_url = f'https://a2.wykop.pl/Tags/Index/{tag}'
        data = {'page':'1'}

        return self._paginated_stream(method_url, data, {}, limit)

    def tag_links(self, tag, limit=50):
        method_url = f'https://a2.wykop.pl/Tags/Links/{tag}'
        data = {'page':'1'}

        return self._paginated_stream(method_url, data, {}, limit)

    def tag_entries(self, tag, limit=50):
        method_url = f'https://a2.wykop.pl/Tags/Entries/{tag}'
        data = {'page':'1'}

        return self._paginated_stream(method_url, data, {}, limit)

    """ INTERNALS """
    def _paginated_stream(self, method_url, get_data, post_data, limit=50, page_step=1):
        """ """
        returned = 0
        urls_stream = self._url_page_generator(str(method_url), get_data, post_data, page_step=page_step)

        for url in urls_stream:
            entries = self._get(url, {}, post_data)
            for e in entries['data']:
                yield e
                returned += 1
                if returned >= limit and limit > 0:
                    return

    def _url_page_generator(self, method_url, get_data, post_data, page_step=1):
        start_page = int(get_data.get('page', 0))
        for page_num in itertools.count(start=start_page, step=page_step):
            get_data['page'] = page_num 
            yield self._get_url(method_url, get_data, post_data)

    def _get_url(self, method_url, get_params={}, post_params={}, data='full', output='clear'):
        api_key = self.api_key

        if not 'appkey' in method_url:
            method_url = method_url + f'/appkey/{api_key}/data/{data}/output/{output}/'

        for k, v in get_params.items():
            method_url = method_url + f'/{k}/{v}'

        return method_url

    def _get(self, method_url, get_params={}, post_params={}, data='full', output='clear'):
        method_url = self._get_url(method_url, get_params, post_params, data, output)
        
        post = None
        while post is None:
            try:
                post = r.post(method_url, 
                    data=post_params, 
                    timeout=10.0)
            except SSLError:
                pass
                print('ssl error')
                time.sleep(2.0)
            except ReadTimeout:
                pass                
        if post.status_code == 200:
            return json.loads(post.text, object_hook=self._date_hook) 
        return {}

    def _date_hook(self, json_dict):
        for (key, value) in json_dict.items():
            try:
                json_dict[key] = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            except:
                pass
        return json_dict

if __name__ == '__main__':
    w = Wykop()


    print(w.user_profile('TheLSC'))