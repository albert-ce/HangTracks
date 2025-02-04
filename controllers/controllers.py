from flask import *
from models.models import *

setup = Blueprint('setup', __name__)
game = Blueprint('game', __name__)

music = LastFmService()

@setup.route('/setup/add_artist')
def add_artist():
    search = request.args.get('search')
    if not search:
        abort(400, description="The 'search' argument is required")

    artist = music.search_artist(search)
    artist_found = artist is not None

    if artist_found:
        session.setdefault('artists', {})[str(artist['id'])] = artist['title']
        session.modified = True

    return jsonify({
        "html": render_template('artists.html', artists_data=session.get('artists', {})),
        "artist_found": artist_found
    })

@setup.route('/setup/remove_artist')
def remove_artist():
    id = request.args.get('id')
    if not id:
        abort(400, description="The 'id' argument is required")

    if id in session.get('artists', {}):
        del session['artists'][id]
        session.modified = True

    return render_template('artists.html', artists_data=session.get('artists', {}))

@setup.route('/setup/check_artists')
def check_artists():
    return jsonify({"artists_exist": bool(session.get('artists'))})

@game.route('/play')
def play():
    if not session.get('artists'):
        return redirect(url_for('index'))
    return render_template('play.html')

@game.route('/game/start')
def start_game():
    secret, session['track_data'] = music.get_random_track()
    hangman = HangmanGame()
    difficulty = len(session.get('artists', {}))
    hangman.start(secret, difficulty)
    session['game_data'] = hangman.get_data()
    return jsonify({
        "html": render_template('game.html', game_data=session['game_data'], keyboard=KEYBOARD),
        "win": hangman.win
    })

@game.route('/game/guess')
def guess():
    letter = request.args.get('letter')
    if not letter or len(letter) != 1:
        abort(400, description="Invalid letter input")

    hangman = HangmanGame()
    hangman.load_state(session['game_data'])
    hangman.guess(letter)
    session['game_data'] = hangman.get_data()

    if session['game_data']['ended']:
        if session['game_data']['win']:
            return render_template('won.html', game_data=session['game_data'], track_data=session["track_data"])
        else:
            return render_template('lost.html', game_data=session['game_data'], track_data=session["track_data"])
    return render_template('game.html', game_data=session['game_data'], keyboard=KEYBOARD)
