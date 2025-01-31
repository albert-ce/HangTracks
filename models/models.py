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
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ñ'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
]
LETTERS = {letter for row in KEYBOARD for letter in row}

import requests
import time
import random

class MusicBrainzService:
    def __init__(self):
        self.lock = Lock()
        self.last_call = None
        self.waiting_time = 1
        self.user_agent = "HangTracks/0.1.0 (https://github.com/albert-ce)"
        self.headers = {"User-Agent": self.user_agent}

    def _wait_rate_limiting(self):
        # Wait to make only 1 call per second
        with self.lock:
            if self.last_call:
                time_since_last_call = time.time() - self.last_call
                if time_since_last_call < self.waiting_time:
                    time.sleep(self.waiting_time - time_since_last_call)
            self.last_call = time.time()

    def search_artist(self, artist_name):
        url = f"https://musicbrainz.org/ws/2/artist/?query=artist:{artist_name}&fmt=json"
        self._wait_rate_limiting()
        response = requests.get(url, headers=self.headers)
        data = response.json()

        if data.get('artists'):
            return data['artists'][0]
        else:
            return None

    def _get_total_recordings(self, artist_mbid):
        url = f"https://musicbrainz.org/ws/2/recording/?query=arid:{artist_mbid}&fmt=json"
        self._wait_rate_limiting()
        response = requests.get(url, headers=self.headers)
        data = response.json()

        if 'recordings' in data:
            return int(data.get('count', 0))
        else:
            return 0

    def _get_random_recording(self):
        if not session['artists']:
            raise KeyError(f"Not artists selected")

        artist_mbid = random.choice(list(session['artists'].keys()))
        total_recordings = self._get_total_recordings(artist_mbid)

        if total_recordings == 0:
            raise ValueError(f"Random artist has no recordings")

        random_offset = random.randint(0, total_recordings - 1)
        url = f"https://musicbrainz.org/ws/2/recording/?query=arid:{artist_mbid}&offset={random_offset}&limit=1&fmt=json"
        self._wait_rate_limiting()
        response = requests.get(url, headers=self.headers)
        data = response.json()

        if 'recordings' in data and data['recordings']:
            return data['recordings'][0]
        else:
            return None
        
    def get_random_track(self):
        recording = self._get_random_recording()
        artist = recording["artist-credit"][0]["name"]
        album = recording["releases"][0]["release-group"]["title"]
        title = recording['title']
        title = re.sub("\(.*\)", "", title)
        title = re.sub("\[.*\]", "", title)
        title = re.sub("- Remastered.*", "", title)
        title = re.sub("- Mono/Remastered.*", "", title)
        title = re.sub("^\s*", "", title)
        title_cleaned = re.sub("\s*$", "", title)
        return title_cleaned, {"album":album, "artist":artist}
    

class HangmanGame:
    def _get_base_letters(self, text):
        normalized_text = unicodedata.normalize('NFD', text)
        return ''.join(c for c in normalized_text if unicodedata.category(c) != 'Mn')
    
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