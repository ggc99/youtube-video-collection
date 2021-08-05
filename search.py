from googleapiclient.discovery import build
import requests
import subprocess
import os
import argparse
from display import prompt_question, action_options, print_msg

def saveToHistory(opened_ids):
    print("Saving videos to history...")
    with open(VIDEO_IDS_HISTORY, 'a') as f:
        for video_id in opened_ids:
            f.write(video_id + '\n')

def build_ps_cmd(url_list, browser='msedge'):
    s = ''
    for url in url_list:
        s += f'start {browser} "--inprivate {url}"\n'
    return s

def openAction():
    number_of_videos = 0
    video_ids = []

    number_tabs_in = prompt_question('number_of_tabs')['number_of_tabs']
    with open(VIDEO_IDS_FILE) as f:
        number_of_videos = min(sum(1 for _ in f), number_tabs_in)
        
    with open(VIDEO_IDS_FILE) as f, open(VIDEO_IDS_FILE+'_temp', 'w') as out:
        video_ids = [next(f)[:-1] for x in range(number_of_videos)]
        for l in f: 
            out.write(l)
    os.remove(VIDEO_IDS_FILE)
    os.rename(VIDEO_IDS_FILE+'_temp', VIDEO_IDS_FILE)
    
    youtube_urls = [f'https://youtube.com/watch?v={x}' for x in video_ids]

    print_msg('', header="Opening Youtube urls:", list_content=youtube_urls)
    
    powershell_cmd = build_ps_cmd(youtube_urls)
    
    completed = subprocess.run(["powershell", "-Command", powershell_cmd], capture_output=True)

    saveToHistory(video_ids)   
    

def searchAction():
    #TODO: Add search by related ID functionality
    searchByKeywordAction()   

def searchByKeywordAction():
    keywords = [x[:-1] for x in open("./keyword_input.txt").readlines()[:-1]]
    
    print_msg('', list_content=keywords, header='Found keywords in input file')

    keywords_continue = prompt_question('keywords_confirmation')
    if keywords_continue['keywords_continue']:
        user_in = prompt_question('translate_flag')
        translate_flag = user_in['translate_flag']
        number_of_results = prompt_question('number_of_results')['number_of_results']
        query_list = keywords.copy()
        if translate_flag:
            for keyword in keywords:
                translation_list = translate(keyword)
                query_list += translation_list
                print('*' * 25, query_list)
        searchByKeyword(query_list, number_of_results)
    return

def checkIdHistory(ids):
    print("Checking ids in history...")
    new_ids = []
    ids_count = 0
    history = []
    with open(VIDEO_IDS_HISTORY, "r") as f:
        history = [x[:-1] for x in f.readlines()]
    with open(VIDEO_IDS_FILE, "r") as f:
        history = history + [x[:-1] for x in f.readlines()]
    for video_id in ids:
        if (video_id not in history) and ids_count<10:
            new_ids.append(video_id)
            ids_count += 1
    return new_ids

def searchByKeyword(query_words, number_of_results):
    for query in query_words:
        print_msg('', header=f'Searching for {query}')
        response = youtube.search().list(
                part = 'snippet',
                maxResults=number_of_results,
                q=query,
                type="video"
            ).execute()

        ids = [x['id']['videoId'] for x in response['items']]
        print_msg('', subheader='Found ids:', list_content=ids)
        new_ids = checkIdHistory(ids)
        saveIdsToFile(new_ids, VIDEO_IDS_FILE)

        
def saveIdsToFile(id_list, filename):
    print_msg(f'count: {len(id_list)}\nfile:{filename}', header='Saving Video IDs') 
    with open(filename, 'a') as f:
        for video_id in id_list:
            f.write(video_id + '\n')
    

def translate(word):
    print_msg('', header=f'Translating {word}')
    translation = []
    for lang in TRANSLATE_LANGUAGES:
        query_url = f'{MYMEMORY_URL}?q={word}&langpair=en|{lang}&de={MYMEMORY_EMAIL}&mt=1'
        translate_request = requests.get(query_url)
        if translate_request.status_code == 200:
            response_translation = translate_request.json()['responseData']['translatedText']
            translation.append(response_translation)
            print(f'{lang}: {response_translation}')
        else:
            print(f'Error translating to {lang}: {translate_request.status_code}')
    return translation

if __name__ == '__main__': 
    
    global YT_API_KEY
    global youtube

    global MYMEMORY_API_KEY
    global MYMEMORY_EMAIL
    global MYMEMORY_URL
    
    parser = argparse.ArgumentParser()

    # Youtube input settings
    parser.add_argument('--youtube_api_key', type=str, required=True, help='your YouTube API key. You can obtain it from your Google cloud account.')
    
    # MyMemory input settings (This is the translator)
    parser.add_argument('--mymemory_email', type=str, required=True, help='your MyMemory account email.')

    # Storage Settings
    parser.add_argument('--results_path', type=str, default='./video_queue.txt', help="the path to a file to serve as a queue for video to be opened")
    parser.add_argument('--history_path', type=str, default='./video_history.txt', help="the path to a file to save the history of videos visited")
    
    args = parser.parse_args()

    YT_API_KEY = args.youtube_api_key
    youtube = build('youtube', 'v3', developerKey = YT_API_KEY)

    MYMEMORY_EMAIL = args.mymemory_email
    MYMEMORY_URL = 'https://api.mymemory.translated.net/get'

    VIDEO_IDS_FILE = args.results_path
    VIDEO_IDS_HISTORY = args.history_path

    TRANSLATE_LANGUAGES = ["es", "ger", "ar", "fr"] 

    quit = False
    



    while not quit:
        user_action = prompt_question('action')
        if user_action['action'] == action_options['search']:
            searchAction()
        elif user_action['action'] == action_options['open']:
            openAction()
        elif user_action['action'] == action_options['quit']:
            quit = True

