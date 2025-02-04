import os
import re
import unicodedata
import secrets
import requests
import time
from flask import session
from threading import Lock
import urllib.parse

KEYBOARD = [
    # Numbers ommited at the moment to prevent issues with titles starting with track numbers
    # ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
]
LETTERS = {letter for row in KEYBOARD for letter in row}

class LastFmService:
    def __init__(self):
        self.lock = Lock()
        self.last_call = None
        self.waiting_time = 1   # Wait to make only 1 call per second
        self.headers = {
            "User-Agent": "HangTracks/0.1.0 +https://hangtracks.onrender.com/",
            "Authorization": "Discogs key="+os.getenv('DISCOGS_KEY')+", secret="+os.getenv('DISCOGS_SECRET')
        }

    def _wait_rate_limiting(self):
        with self.lock:
            if self.last_call:
                time_since_last_call = time.time() - self.last_call
                if time_since_last_call < self.waiting_time:
                    time.sleep(self.waiting_time - time_since_last_call)
            self.last_call = time.time()

    def search_artist(self, artist_name):
        artist_name = urllib.parse.quote(artist_name)
        url = f"https://api.discogs.com/database/search?q={artist_name}&type=artist"
        self._wait_rate_limiting()
        response = requests.get(url, headers=self.headers)
        data = response.json()

        artists_found = data.get('results')
        if artists_found:
            return artists_found[0]
        else:
            return None

    def _get_random_artist(self):       
        if not session['artists']:
            raise KeyError(f"Not artists selected")

        return secrets.choice(list(session['artists'].items()))

    def _get_random_release(self, artist):
        artist_id, artist_name = artist       
        url = f"https://api.discogs.com/artists/{artist_id}/releases"
        self._wait_rate_limiting()
        response = requests.get(url, headers=self.headers)
        data = response.json()

        releases = data.get('releases')
        if not releases:
            raise ValueError(f"Random artist has no releases")

        release = {}
        while True:
            release = secrets.choice(releases)
            if release.get("artist") == artist_name:
                return release
            releases.remove(release)
            if not releases:
                raise ValueError("Random artist has no self-made releases")

    def _get_random_title(self, release):       
        url = release.get('resource_url')
        self._wait_rate_limiting()
        response = requests.get(url, headers=self.headers)
        data = response.json()

        tracks = data.get('tracklist')
        if not tracks:
            raise ValueError(f"Random release has no tracks")

        random_track = secrets.choice(tracks)
        return random_track['title'], data.get('uri')
        
    def get_random_track(self):
        artist = self._get_random_artist()
        release = self._get_random_release(artist)
        title, url = self._get_random_title(release)

        title = re.sub("\(.*\)", "", title)
        title = re.sub("\[.*\]", "", title)
        title = re.sub("- Remastered.*", "", title)
        title = re.sub("- Mono/Remastered.*", "", title)
        title = re.sub("^\s*", "", title)
        title_cleaned = re.sub("\s*$", "", title)

        return title_cleaned, {"artist":release["artist"], "album":release["title"], "url":url}

IMG_IDS = {1:[0,2,4,9,10],
           2:[0,2,4,7,9,10],
           3:[0,2,3,4,7,9,10],
           4:[0,1,2,3,4,7,9,10],
           5:[0,1,2,3,4,5,7,9,10],
           6:[0,1,2,3,4,5,6,7,9,10],
           7:[0,1,2,3,4,5,6,7,8,9,10]}


class HangmanGame:
    def _get_base_letters(self, text):
        normalized_text = unicodedata.normalize('NFD', text)
        result = []
        for char in normalized_text:
            # Normalize only vowels (á --> a)
            if unicodedata.category(char) == 'Mn' and result and result[-1].lower() in "aeiou":
                continue
            result.append(char)
        return unicodedata.normalize('NFC', ''.join(result))
    
    def start(self, secret, difficulty = 1, img_path = 'img/hangman/{img_id}.svg'):
        self.secret = secret.upper()
        self.base_letters_secret = self._get_base_letters(self.secret)
        self.display = ''.join(["_" if letter in LETTERS else letter for letter in self.base_letters_secret])
        self.difficulty = min(difficulty, 7)
        self.mistakes_left = 3+difficulty
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
            'difficulty': self.difficulty,
            'mistakes_left': self.mistakes_left,
            'mistakes': list(self.mistakes),
            'hits': list(self.hits),
            'ended': self.ended,
            'win': self.win,
            'img_path': self.img_path,
            "img": self.img_path.format(img_id=IMG_IDS[self.difficulty][len(self.mistakes)]),
        }
    
    def load_state(self, data):
        self.secret = data['secret']
        self.base_letters_secret = data['base_letters_secret']
        self.display = data['display']
        self.difficulty = data['difficulty']
        self.mistakes_left = data['mistakes_left']
        self.mistakes = set(data['mistakes'])
        self.hits = set(data['hits'])
        self.ended = data['ended']
        self.win = data['win']
        self.img_path = data['img_path']