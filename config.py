"""Configuration management for the music recommendation app."""
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Debug and Error configurations
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
ERROR_MESSAGES = {
    "spotify_error": "There was an error with the Spotify API.",
    "playlist_error": "No matching playlist found for the selected mood.",
    "mood_input_error": "Invalid mood input. Please check your entry and try again.",
    "playlist_fetch": "Unable to fetch playlists at this time.",
    "invalid_mood": "Please provide a valid mood description."
}

# Application settings
SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24).hex())
HOST = '127.0.0.1'
PORT = 5000

# Ensure Spotify API credentials are set via environment variables
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID', 'your_spotify_client_id')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET', 'your_spotify_client_secret')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_config():
    """Validate that all required configuration is present"""
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        raise ValueError("Missing Spotify API credentials")

# Validate configuration on import
validate_config()
