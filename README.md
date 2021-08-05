# Youtube Video Collection Tool

This tool was created to assist in collecting video feed from Youtube in order to train a deep learning model.

It allows for searching of Youtube videos in an easy manner and runs on Python. (Optimized for Windows).

The video IDs are saved and can be easily managed to be opened for manual annotation. It was built to relate a Video ID with a corresponding annotation. 

## Setup
Make sure Python 3.7 and pip are installed

Create a Google Cloud account to obtain a YouTube API key. Once your account is created go to console.cloud.google.com

Create a MyMemory account at https://mymemory.translated.net/.

Install the required packages. Run `pip install -r requirements.txt` to install the dependencies.


## Few Notes Before Running

`keyword_input.txt` file: Any queries you want to search for must be separated by a new line and the file must end with a new line

The video queue: There must be a video queue file. This file is used to open the videos you just searched for. (This can be used to create manual annotations of the videos)

## Running
Run `python search.py --youtube_api_key <YOUR API KEY> --mymemory_email <YOUR MYMEMORY ACCOUNT EMAIL>

