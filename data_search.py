from tqdm import tqdm
import requests
import praw
import re
import time
import json

pattern = re.compile('https://(.*?)\.com/')

with open('keyword_sheet.json', 'r') as f:
    keyword_sheet = json.load(f)

reddit = praw.Reddit()

response = requests.get('https://api.stackexchange.com/2.3/sites').json()['items']

sites_info = {}
for res in response:
    sites_info[res['site_url']] = res['api_site_parameter']

ordr = 99 - len(keyword_sheet)

for failure_name, symptoms in tqdm(keyword_sheet.items(), total=len(keyword_sheet), desc='Keyword searching'):
    ordr += 1
    print(f'Search about {failure_name}... ({ordr}/99)')

    init_start, total_passage = 1, []

    with tqdm(total=100, desc='Page rounding') as pbar:
        while init_start:
            params = {
                'q': f'Cloud {failure_name}: {symptoms}',
                'start': init_start
            }
            response = requests.get('https://www.googleapis.com/customsearch/v1', params=params).json()

            if not int(response['searchInformation']['totalResults']):
                break

            if init_start == 1:
                totalResults = int(response['searchInformation']['totalResults'])
                if totalResults > 10:
                    pages = list(range(11, 101 if totalResults > 100 else totalResults, 10)) + [False]
                else:
                    pages = [False]

            q_ids, c_ids = {}, []
            for res in response['items']:
                if res['link'][:23] == 'https://www.reddit.com/':
                    try:
                        c_id = res['link'].split('/')[6]
                    except IndexError:
                        continue
                    c_ids.append('t3_' + c_id)
                else:
                    try:
                        domain = pattern.search(res['link']).group(1)
                        api_site_parameter = sorted([y for x,y in sites_info.items() if domain in x], key=len)[0]
                    except (IndexError, AttributeError):
                        continue

                    try:
                        q_id = res['link'].split('/')[4]
                    except IndexError:
                        continue
                    if q_id.isdigit():
                        if api_site_parameter in q_ids.keys():
                            q_ids[api_site_parameter].append(q_id)
                        else:
                            q_ids[api_site_parameter] = [q_id]

                if not pages[0]:
                    target_ids = {x: ';'.join(y) for x,y in q_ids.items()}
                else:
                    target_ids = {x: ';'.join(y) for x,y in q_ids.items() if len(y) == 10}
                for site, ids in target_ids.items():
                    params = {
                        'order': 'desc',
                        'sort': 'activity',
                        'site': site,
                        'filter': 'withbody'
                    }
                    try:
                        response = requests.get(f'https://api.stackexchange.com/2.3/questions/{ids}',
                                                params=params).json()['items']
                    except KeyError:
                        continue

                    questions = {str(x['question_id']): '**' + x['title'] + '**<br>' + x['body']
                                 for x in response if x['is_answered']}
                    ids = ';'.join(questions.keys())

                    params = {
                        'order': 'desc',
                        'sort': 'activity',
                        'site': site,
                        'filter': 'withbody'
                    }
                    try:
                        response = requests.get(f'https://api.stackexchange.com/2.3/questions/{ids}/answers',
                                                params=params).json()['items']
                    except KeyError:
                        continue

                    posts = []
                    for question_id, question in questions.items():
                        posts.append({'question': question,
                                      'answer': [{'score': x['score'], 'body': x['body']}
                                                 for x in response if x['question_id'] == int(question_id)]})

                    del q_ids[site]

                    total_passage.extend(posts)

                for submission in reddit.info(fullnames=c_ids):
                    submission.comments.replace_more(limit=1)
                    total_passage.append({
                        'question': '**' + submission.title + '**<br>' + submission.selftext,
                        'answer': [{'score': x.score, 'body': x.body} for x in submission.comments]
                    })
                    time.sleep(1)
                c_ids = []

            init_start = pages.pop(0)

            pbar.update(10)

    print(f'Number of total passage until current phase:', len(total_passage))
    print(reddit.auth.limits)

    if total_passage:
        with open(f'knowledges/{failure_name.replace(" ", "_").replace("/", "")}.json', 'w') as f:
            json.dump({'items': total_passage}, f)
