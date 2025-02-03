import os
import re
import unicodedata
import random
import requests
from time import time
from flask import session
from threading import Lock

NUM_ATTEMPTS = 8
KEYBOARD = [
    # Numbers ommited at the moment to prevent issues with titles starting with track numbers
    # ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
]
LETTERS = {letter for row in KEYBOARD for letter in row}

import requests
import time
import random

class LastFmService:
    def __init__(self):
        self.lock = Lock()
        self.last_call = None
        self.waiting_time = 1   # Wait to make only 1 call per second
        self.n_tracks = 60     # Fetch the first 60 top tracks from the artist
        self.api_key = os.getenv('LASTFM_API_KEY')
        self.url = "https://ws.audioscrobbler.com/2.0/"
        self.headers = {"User-Agent": "HangTracks/0.1.0 (https://github.com/albert-ce)"}

    def _wait_rate_limiting(self):
        with self.lock:
            if self.last_call:
                time_since_last_call = time.time() - self.last_call
                if time_since_last_call < self.waiting_time:
                    time.sleep(self.waiting_time - time_since_last_call)
            self.last_call = time.time()

    def search_artist(self, artist_name):
        params = {
            "method": "artist.search",
            "api_key": self.api_key,
            "artist": artist_name,
            "limit": 1,
            "format": "json"
        }
        self._wait_rate_limiting()
        response = requests.post(self.url, data=params, headers=self.headers)
        data = response.json()

        artists_found = data.get('results', {}).get('artistmatches', {}).get('artist')
        if artists_found:
            return artists_found[0]
        else:
            return None

    def _get_random_artist(self):       
        if not session['artists']:
            raise KeyError(f"Not artists selected")

        random.seed(time.time())
        return random.choice(session['artists'])

    def _get_random_title(self, artist):       
        params = {
            "method": "artist.gettoptracks",
            "api_key": self.api_key,
            "artist": artist,
            "limit": self.n_tracks,
            "format": "json"
        }
        self._wait_rate_limiting()
        response = requests.post(self.url, data=params, headers=self.headers)
        data = response.json()

        tracks = data.get('toptracks', {}).get('track')
        if not tracks:
            raise ValueError(f"Random artist has no recordings")

        random.seed(time.time())
        random_track = random.choice(tracks)
        return random_track['name'], random_track['url']
        
    def get_random_track(self):
        artist = self._get_random_artist()
        title, url = self._get_random_title(artist)

        title = re.sub("\(.*\)", "", title)
        title = re.sub("\[.*\]", "", title)
        title = re.sub("- Remastered.*", "", title)
        title = re.sub("- Mono/Remastered.*", "", title)
        title = re.sub("^\s*", "", title)
        title_cleaned = re.sub("\s*$", "", title)

        return title_cleaned, {"artist":artist, "url":url}

class HangmanGame:
    def _get_base_letters(self, text):
        normalized_text = unicodedata.normalize('NFD', text)
        return ''.join(c for c in normalized_text if unicodedata.category(c) != 'Mn' or c==c == '̃')
    
    def start(self, secret, img_path = 'img/hangman/{n_mistakes}.svg'):
        self.secret = secret.upper()
        self.base_letters_secret = self._get_base_letters(self.secret)
        self.display = ''.join(["_" if letter in LETTERS else letter for letter in self.base_letters_secret])
        self.mistakes_left = NUM_ATTEMPTS
        self.mistakes = set()
        self.hits = set()
        self.ended = "_" not in self.display
        self.win = "_" not in self.display
        self.img_path = img_path

    def guess(self, letter):
        letter = letter.upper()
        if not self.ended and letter not in self.mistakes:
            if letter in self.base_letters_secret:
                self.display = ''.join([secret_letter if base_letter == letter else display_letter
                                        for base_letter, display_letter, secret_letter
                                        in zip(self.base_letters_secret, self.display, self.secret)])
                self.hits.add(letter)
                if "_" not in self.display:
                    self.win = True
                    self.ended = True
            else:
                self.mistakes.add(letter)
                self.mistakes_left -= 1
                if self.mistakes_left == 0:
                    self.ended = True
    
    def get_data(self):
        return {
            'secret': self.secret,
            'base_letters_secret': self.base_letters_secret,
            'display': self.display,
            'mistakes_left': self.mistakes_left,
            'mistakes': list(self.mistakes),
            'hits': list(self.hits),
            'ended': self.ended,
            'win': self.win,
            'img_path': self.img_path,
            "img": self.img_path.format(n_mistakes=len(self.mistakes)),
        }
    
    def load_state(self, data):
        self.secret = data['secret']
        self.base_letters_secret = data['base_letters_secret']
        self.display = data['display']
        self.mistakes_left = data['mistakes_left']
        self.mistakes = set(data['mistakes'])
        self.hits = set(data['hits'])
        self.ended = data['ended']
        self.win = data['win']
        self.img_path = data['img_path']