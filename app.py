import os
from flask import Flask, render_template, request, redirect, url_for, session
import logging
from typing import Any, Callable, Dict, List, Optional
from emoji_predictor import (
    predict_emoji, 
    normalize_text, 
    combined_emotion, 
    state_to_language, 
    get_spotify_playlist
)
from handlers import handle_spotify_error, handle_playlist_error, handle_mood_input_error, validate_mood_input
from datetime import datetime
from config import DEBUG, PORT, HOST, SECRET_KEY
from functools import wraps
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger: logging.Logger = logging.getLogger(__name__)

app: Flask = Flask(__name__)
app.secret_key = SECRET_KEY

MOOD_HISTORY_FILE: str = "mood_history.json"

def load_mood_history() -> Dict[str, Dict[str, Any]]:
    try:
        with open(MOOD_HISTORY_FILE, "r") as file:
            history = json.load(file)
            for username in history:
                if isinstance(history[username], list):
                    history[username] = {
                        "state": "Unknown",
                        "mood_history": history[username]
                    }
            return history
    except FileNotFoundError:
        return {}

def save_mood_history(history: Dict[str, Dict[str, Any]]) -> None:
    with open(MOOD_HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

def login_required(f: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Simple security layer: require ?access=SECRET for all main routes except login
DEMO_SECRET: str = os.getenv('DEMO_SECRET', 'letmein2025')

def require_secret(f: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        # Allow if already in session, else check query param
        if session.get('access_granted'):
            return f(*args, **kwargs)
        access = request.args.get('access')
        if access == DEMO_SECRET:
            session['access_granted'] = True
            return f(*args, **kwargs)
        # If not granted, redirect to login with a message
        return redirect(url_for('login', error='Access denied. Use your secret link.'))
    return decorated_function

@app.route("/", methods=["GET", "POST"])
def login() -> Any:
    if request.method == "POST":
        username: Optional[str] = request.form.get("username")
        if not username:
            return render_template("error.html", message="Username is required"), 400
        history = load_mood_history()
        session['username'] = username
        if username in history:
            return redirect(url_for("mood_input", username=username))
        else:
            return redirect(url_for("state_selection", username=username))
    return render_template("login.html")

@app.route("/state_selection", methods=["GET", "POST"])
@login_required
def state_selection() -> Any:
    username: Optional[str] = request.args.get("username") or session.get('username')
    if not username:
        return redirect(url_for("login"))
    if request.method == "POST":
        state: Optional[str] = request.form.get("state")
        if not state:
            return render_template("error.html", message="Please select a state"), 400
        history = load_mood_history()
        history[username] = {"state": state, "mood_history": []}
        save_mood_history(history)
        return redirect(url_for("mood_input", username=username))
    return render_template("state_selection.html", username=username, state_languages=state_to_language)

@app.route("/mood_input", methods=["GET"])
@login_required
def mood_input() -> Any:
    username: Optional[str] = session.get('username')
    if not username:
        return redirect(url_for("login"))
    history = load_mood_history()
    user_data = history.get(username, {"state": "Unknown", "mood_history": []})
    state: str = user_data.get("state", "Unknown")
    mood_history: List[Dict[str, Any]] = user_data.get("mood_history", [])
    return render_template("mood_input.html", username=username, state=state, mood_history=mood_history)

@app.route("/logout")
def logout() -> Any:
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/clear_history", methods=["POST"])
@login_required
def clear_history() -> Any:
    username: Optional[str] = session.get('username')
    if not username:
        return redirect(url_for("login"))
    history = load_mood_history()
    if username in history:
        state = history[username].get("state")
        history[username] = {"state": state, "mood_history": []}
        save_mood_history(history)
    return redirect(url_for("mood_input", username=username))

@app.route("/process_mood", methods=["POST"])
@login_required
@handle_mood_input_error
def process_mood() -> Any:
    username: Optional[str] = session.get('username')
    if not username:
        return redirect(url_for("login"))
    text: Optional[str] = request.form.get("text")
    if not text:
        return render_template("error.html", message="Please enter your mood"), 400
    try:
        text = validate_mood_input(text)
        normalized_text = normalize_text(text)
        history = load_mood_history()
        user_data = history.get(username, {"state": "Unknown", "mood_history": []})
        state: str = user_data.get("state", "Unknown")
        emoji, top_emotion, language = predict_emoji(normalized_text, state)
        emotions = combined_emotion(normalized_text)
        top_emotion = emotions[0][0] if emotions else "neutral"
        playlists = get_spotify_playlist(top_emotion, language)
        if not playlists or len(playlists) == 0:
            logger.warning(f"No playlists found for emotion '{top_emotion}' and language '{language}'. Using default playlists.")
            playlists = get_spotify_playlist('neutral', language)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mood_entry = {
            "text": text,
            "emoji": emoji,
            "timestamp": timestamp
        }
        if username not in history:
            history[username] = {"state": state, "mood_history": []}
        history[username]["mood_history"].insert(0, mood_entry)
        save_mood_history(history)
        session['playlists'] = playlists
        session['emoji'] = emoji
        session['emotion'] = top_emotion
        return redirect(url_for('show_playlists'))
    except Exception as e:
        logger.error(f"Error processing mood: {str(e)}")
        return render_template("error.html", message="An error occurred while processing your mood. Please try again."), 500

@app.route("/show_playlists")
@login_required
def show_playlists() -> Any:
    playlists = session.get('playlists', None)
    emoji = session.get('emoji', None)
    emotion = session.get('emotion', None)
    username = session.get('username')
    if not playlists or not emoji or not emotion:
        return redirect(url_for('mood_input'))
    return render_template("index.html", playlists=playlists, emoji=emoji, emotion=emotion, username=username)

@app.route("/mood_trends")
@login_required
def mood_trends() -> Any:
    username: Optional[str] = session.get('username')
    if not username:
        return redirect(url_for('login'))
    history = load_mood_history()
    user_data = history.get(username, {"state": "Unknown", "mood_history": []})
    mood_history: List[Dict[str, Any]] = user_data.get("mood_history", [])
    return render_template("mood_trends.html", username=username, mood_history=mood_history)

@app.errorhandler(400)
def bad_request_error(error: Exception) -> Any:
    return render_template("error.html", message="Bad Request. Please check your input."), 400

@app.errorhandler(404)
def not_found_error(error: Exception) -> Any:
    return render_template("error.html", message="Page not found."), 404

@app.errorhandler(500)
def internal_error(error: Exception) -> Any:
    return render_template("error.html", message="An unexpected error occurred. Please try again later."), 500

# Ensure NLTK WordNet corpus is downloaded at runtime
try:
    import nltk
    nltk.data.find('corpora/wordnet')
except (ImportError, LookupError):
    import nltk
    nltk.download('wordnet')

if __name__ == "__main__":
    try:
        logger.info(f"Initializing application on {HOST}:{PORT}")
        app.run(host=HOST, port=PORT, debug=DEBUG)
    except Exception as e:
        logger.error(f"Error starting application: {e}")
        import sys
        sys.exit(1)