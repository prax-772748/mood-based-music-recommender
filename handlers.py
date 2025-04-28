import logging
from functools import wraps
from flask import render_template, jsonify
from werkzeug.exceptions import HTTPException
import spotipy
from config import ERROR_MESSAGES, DEBUG

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SpotifyError(Exception):
    """Custom exception for Spotify API related errors"""
    pass

def handle_spotify_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except spotipy.SpotifyException as e:
            logger.error(f"Spotify API error: {str(e)}")
            return render_template('error.html', 
                                error_message="Unable to connect to Spotify. Please try again later.",
                                error_details=str(e) if DEBUG else None)
        except Exception as e:
            logger.exception("Unexpected error in Spotify handler")
            return render_template('error.html', 
                                error_message="An unexpected error occurred.",
                                error_details=str(e) if DEBUG else None)
    return wrapper

def handle_api_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException as e:
            logger.error(f"HTTP error {e.code}: {str(e)}")
            return jsonify({
                'error': str(e),
                'status_code': e.code
            }), e.code
        except Exception as e:
            logger.exception("Unexpected API error")
            return jsonify({
                'error': 'Internal server error',
                'details': str(e) if DEBUG else None
            }), 500
    return wrapper

def handle_playlist_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Playlist error: {str(e)}")
            return render_template("error.html", message=ERROR_MESSAGES['playlist_fetch']), 500
    return wrapper

def handle_mood_input_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            logger.error(f"Invalid mood input: {str(e)}")
            return render_template("error.html", message=ERROR_MESSAGES['invalid_mood']), 400
        except Exception as e:
            logger.error(f"Mood processing error: {str(e)}")
            return render_template("error.html", message="An unexpected error occurred"), 500
    return wrapper

def format_playlist_response(playlists, emotion, language):
    """Format playlist response with additional metadata"""
    return {
        'playlists': playlists,
        'metadata': {
            'emotion': emotion,
            'language': language,
            'count': len(playlists)
        }
    }

def validate_mood_input(text):
    """Validate mood input text"""
    if not text or not isinstance(text, str):
        raise ValueError("Mood input must be a non-empty string")
    if len(text.strip()) == 0:
        raise ValueError("Mood input cannot be empty or just whitespace")
    if len(text) > 500:
        raise ValueError("Mood input too long (maximum 500 characters)")
    return text.strip()

def safe_emoji_prediction(text):
    """Safely predict emoji from text with error handling"""
    from emoji_predictor import predict_emoji
    try:
        return predict_emoji(text)
    except Exception as e:
        logger.error(f"Error predicting emoji: {str(e)}")
        return "😐"  # Default neutral emoji

def log_mood_prediction(mood_text, predicted_emoji, user_id=None):
    """Log mood predictions for analysis"""
    logger.info(
        f"Mood Prediction: text='{mood_text}', emoji={predicted_emoji}, user={user_id or 'anonymous'}"
    )

def format_error_response(message, status_code=400):
    """Format error response"""
    return jsonify({
        'error': True,
        'message': message,
        'status_code': status_code
    }), status_code