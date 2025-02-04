![Fortune Lyrics Banner](static/img/banner.png)

# HangTracks: Play hangman with your favorite songs

**HangTracks** is a web app built with Python that fetches a random title from your favourite artists and turns it into a game of hangman. It uses Last.fm's API to select artists and tracks, transforming music into a unique challenge.
- **Quick**: As fast as playing *Wordle*.
- **Simple**: A classic game everyone knows.
- **Personalized**: It uses song titles of your favorite artists.
- **Challenging**: The number of allowed mistakes is limited — starting at 4, with 1 extra per added artist.

## Try it out

Explore the online version of this project and see it in action!

[![Demo Button](https://img.shields.io/badge/%20-Play%20it%20here!-ffc534?labelColor=black&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAADwAAAA8CAIAAAC1nk4lAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAASdSURBVGhD7ZjNLixBFMeZMCGYuESC%2BIzPCCEzxE6EiESCWExEInZi6REsPIGNlYVYeQNbDyCx5gVkiI8Rn0G7%2F9vnPzV1u3u6e7rHvZv%2BLWZOnXPq1JmqU9XVUxYRERERiHJ%2Bh6a8vPyXSUtLS0NDQ01NzdfX1%2Fv7%2B83NTSaTub29zWaz39%2Ff9P6%2FJBKJra0twzerq6u1tbXsHJTgM20YmLbgM4eVAWwUSZBuyWTy7OyMDRvpdPr6%2BhqFgWKorq5ubm4%2BPj6mzUYqlTo%2FP2fjh8DKcpk1kByKhB6u1NfXw5ndNLAB6FFy7ON1dHTQViQ9PT0MYYLIgDYf%2BC0PS9wwFakIHDPGb1cs0SsqKsJnDBAkHo%2BzYRvFBe%2BkOzs7VSwME4vFsKDSDM%2Fn5ycCsuE7b%2B8J01PUB3AEDo2NjdhwdXV1kF9eXh4eHu7v719fX%2BlRAH0UrGSoeUFnBVUFmJ6epl9uYwlKg8%2FW1lZ6OyGeAlUBwCnLGIaB5zO1NsRBUnRHebLn3%2BjnKU53aotlbW2NMQr89KamJpgkIR3pIlBlQ9%2BCCvYxoapY2NswcAGiSgMDwyQZAPEEKGh6mKBAR0ZGxERXDTppiCdwryVncGiwt9OPnpqagp4jmxl3d3fTVgCcPHNzc5Ze%2BKQ5x8rKCvQCVf5hP8PADqMqx9jYmIwKxIcGH1RWVsKfnZ3yxo3ADPkHqvzDfraLAXYklIWG9IkZOB8EO54GE7ECzxPWCvsZhuXhB40aDJ%2FUFo%2BKAyBTa7K3tweN4OsYwR1I9bGHm5iYEL3dFAAVSqC2rMxe%2BsvLy7TZgVn3BmjSZqKsFn1gHAPaT1I0dYd80cgR43ITmpycVFYXt6KYmZmhZO4WEfDYF0GB4QAutGwrLD9O2N%2Ffp%2FkHphlgqzmGdUxGOXhsz6enJ0oa6%2BvrlEIT7Pfnk3ZccbzqiYA6EwG%2F%2BOTkROSSsLi4SMl31XnMtEq6t7dXRcxmsyKUBP3FFo8eSq74TXpoaEgEEGxNC6Fvu9Ik%2FfHxIUJVVZUIJQf1Rsk3HklfXV2J8Pb2JkLJ0afD5xp6JK1eky4uLkQAPreLT9rb20VAWLWw7ngkrbi8vKRk%2FudCqRTMzs6KgDrBe67IfvlzfNtYWlqiWTvwNzY2qCoFKqxeG0qpoxzyMw0tJS8ODw8phUZfNDXlBcmVZT7p4eFh97zVPQHFl0wmRQ5JOp2WHYKhT09PRekIHGKOewnzb1kXvTyAskKgKgTytu8Y0JIGmvoh89dGxPUllUrR0eTx8ZE2k%2Fn5eSghYHpECMPz87OaZst%2FmZubm0dHRwcHB9vb24ODg0jM15mLcBLRgj43%2BsWyWNBdD0XtD9HW1qYGAwsLCzQUg5lwPuOi3wUDICOpIYHPOwOIx%2BPSRXXHJ20%2FjRpPMNPwXmJxYx%2BT8fFx2v4NGNKSAZq7u7ujo6M4fTGjWHSsQCKRGBgY2NnZsTv39%2FczVpE4nXy%2BQWayqfUti4Qoadgdwv6fG5K%2Bvj7LLLoAT2xl9vzv6P%2F9McEc1BpGV1cXvcMRqjwK0WiCasbj4%2B7uLpPJ0BARERERERFRMsrKfgMz5JegQxZuawAAAABJRU5ErkJggg%3D%3D)](https://hangtracks.onrender.com)

## Features
- Easy-to-use artist search and selection.
- Retrieves a random title from its artist's top songs.
- Implements a clean and easy-to-play version of hangman.
- Adjusts allowed mistakes based on selected artists, starting at 4 and increasing by 1 per artist (up to 10).
- Turns the music you love into a fun challenge.

---

## Troubleshooting
The game experience can be affected by:

- **Title Accuracy**: Last.fm song titles may not always be 100% accurate. HangTracks cleans the titles and selects only the top songs to minimize this issue.
- **Special Characters**: Non-vowel special characters like "ç" or "ñ" are not included in the virtual keyboard, so they won’t be hidden. However, for vowels with accents or diacritics (e.g., "á", "ï"), use the base letter (e.g., "a", "i") to guess them.

## Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/albert-ce/HangTracks.git
cd HangTracks
```

### 2. Install Requirements
Ensure you have Python 3.7+ installed. Then, install the required Python libraries:
```bash
pip install -r requirements.txt
```

### 3. Get Secret Tokens

> [!WARNING]  
> This app requires a Last.fm API token to function. Follow the instructions below to generate and configure it.

#### Last.fm
1. Go to the [Last.fm API](https://www.last.fm/api) page and create an account or log in.
2. Once logged in, visit the [Get an API account](https://www.last.fm/api/account/create) page and create a new API application.
3. Note down your **API key**.
4. Save your **API key** in a `.env` file in the root directory of the project:
    ```.env
    LASTFM_API_KEY='your-api-key'
    ```

#### Flask Secret Key
1. The app also requires a secret key for secure sessions. To generate one, you can use the following command:
    ```bash
    python -c "import secrets; print(secrets.token_hex(32))"
    ```
2. Save your generated secret key in the `.env` file:
    ```env
    FLASK_SECRET_KEY='your-flask-secret-key'
    ```

---

## Running the App

1. Start the app:
    ```bash
    flask run
    ```

2. Once the app is running, open your browser and go to `http://127.0.0.1:5000` to start playing HangTracks locally.

## Third-Party API Disclaimer

*This application uses Discogs’ API but is not affiliated with, sponsored or endorsed by Discogs. ‘Discogs’ is a trademark of Zink Media, LLC.*

## Third-Party Attributions

This source code uses third-party libraries, including:
- **requests**: For Last.fm API interaction.
- **Flask**: For the web framework.
- **python-dotenv**: For managing environment variables.
- **gunicorn**: For serving the app in production.

For more details on third-party libraries used, see the [ATTRIBUTION.md](ATTRIBUTION.md) file.