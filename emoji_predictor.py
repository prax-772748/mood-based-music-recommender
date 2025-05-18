import logging
import os
import random
from typing import Any, Dict, List, Tuple, Set, Optional
from transformers.pipelines import pipeline
from emotion_mappings import (
    emotion_to_emoji, 
    emotion_patterns, 
    positive_sentiment_words, 
    negative_sentiment_words,
    get_emotion_name
)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize dependencies with error handling
def initialize_dependencies() -> bool:
    try:
        global nltk, wordnet, pipeline, GoogleTranslator, Nominatim, spotipy, SpotifyClientCredentials
        import nltk
        from nltk.corpus import wordnet
        from transformers import pipeline
        from deep_translator import GoogleTranslator
        from geopy.geocoders import Nominatim
        import spotipy
        from spotipy.oauth2 import SpotifyClientCredentials
        
        # Download required NLTK data
        try:
            nltk.data.find('corpora/wordnet')
            nltk.data.find('corpora/omw-1.4')
        except LookupError:
            nltk.download('wordnet')
            nltk.download('omw-1.4')
        
        return True
    except ImportError as e:
        logging.error(f"Failed to import required dependencies: {e}")
        return False

# Initialize dependencies
if not initialize_dependencies():
    logging.warning("Running with limited functionality due to missing dependencies")

# Load multiple emotion detection models with error handling and fallbacks
def initialize_models() -> List[Optional[any]]:
    models = []
    try:
        from transformers import pipeline
        model_configs = [
            ("j-hartmann/emotion-english-distilroberta-base", "text-classification"),
            ("bhadresh-savani/distilbert-base-uncased-emotion", "text-classification"),
            ("nateraw/bert-base-uncased-emotion", "text-classification")
        ]
        
        for model_name, task in model_configs:
            try:
                model = pipeline(task, model=model_name, top_k=None)
                models.append(model)
                logging.info(f"Successfully loaded model: {model_name}")
            except Exception as e:
                logging.warning(f"Failed to load model {model_name}: {e}")
                continue
                
    except Exception as e:
        logging.error(f"Error initializing models: {e}")
    
    return models

# Initialize models with fallback
models = initialize_models()
if not models:
    logging.warning("No ML models available. Using rule-based fallback for emotion detection.")

# Playlist Templates for Supported Languages
playlist_templates = {
    "en": "{emotion} Mix",
    "hi": "{emotion} गाने",
    "ta": "{emotion} பாடல்கள்",
    "te": "{emotion} పాటలు",
    "ml": "{emotion} പാട്ടുകൾ",
    "bn": "{emotion} গান",
    "mr": "{emotion} गाणी",
    "gu": "{emotion} ગીતો",
    "kn": "{emotion} ಹಾಡುಗಳು",
    "pa": "{emotion} ਗੀਤ",
    "as": "{emotion} গীত",
    "or": "{emotion} ଗୀତ",
    "ne": "{emotion} गीतहरू",
    "ks": "{emotion} گانے",
    "bo": "{emotion} གླུ་དབྱངས།",
    "mni": "{emotion} ꯂꯩꯂꯩ",
    "doi": "{emotion} गीत",
    "brx": "{emotion} गीत"
}

def get_playlist_name(emotion: str, language: str) -> str:
    """Generate a playlist name when needed."""
    emotion_playlist_names = {
        'joyful': ['Happy Hits', 'Feel Good Mix', 'Upbeat Classics'],
        'sad': ['Melancholy Mix', 'Rainy Day Songs', 'Soulful Ballads'],
        'energetic': ['Power Mix', 'Workout Hits', 'Energy Boost'],
        'peaceful': ['Chill Vibes', 'Relaxation Station', 'Peaceful Moments'],
        'romantic': ['Love Songs', 'Romantic Hits', 'Sweet Serenades'],
        'neutral': ['Easy Listening', 'All-Time Favorites', 'Classic Mix']
    }
    
    # Get list of names for the emotion or use neutral as fallback
    names = emotion_playlist_names.get(emotion, emotion_playlist_names['neutral'])
    
    # Return a random name from the list
    return random.choice(names)

def generate_mood_to_playlist() -> Dict[str, Dict[str, str]]:
    """Generate a dynamic mood_to_playlist dictionary."""
    mood_to_playlist = {}
    for emoji, emotion in emotion_to_emoji.items():
        mood_to_playlist[emoji] = {
            lang: get_playlist_name(emotion, lang)
            for lang in playlist_templates.keys()
        }
    return mood_to_playlist

# Generate the mood_to_playlist dictionary dynamically
mood_to_playlist = generate_mood_to_playlist()

def get_synonyms(word: str) -> Set[str]:
    """Get synonyms for a given word using WordNet."""


    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return synonyms

def get_emotion_synonyms() -> Dict[str, Set[str]]:
    """Generate dynamic mapping of emotions to synonyms."""


    base_emotions = list(emotion_patterns.keys())
    emotion_synonyms = {}
    for emotion in base_emotions:
        emotion_synonyms[emotion] = get_synonyms(emotion)
    return emotion_synonyms

emotion_synonyms = get_emotion_synonyms()

state_to_language = {
    "Andhra Pradesh": "te",  # Telugu
    "Arunachal Pradesh": "en",  # English
    "Assam": "as",  # Assamese
    "Bihar": "hi",  # Hindi
    "Chhattisgarh": "hi",  # Hindi
    "Goa": "en",  # English
    "Gujarat": "gu",  # Gujarati
    "Haryana": "hi",  # Hindi
    "Himachal Pradesh": "hi",  # Hindi
    "Jharkhand": "hi",  # Hindi
    "Karnataka": "kn",  # Kannada
    "Kerala": "ml",  # Malayalam
    "Madhya Pradesh": "hi",  # Hindi
    "Maharashtra": "mr",  # Marathi
    "Manipur": "mni",  # Manipuri
    "Meghalaya": "en",  # English
    "Mizoram": "en",  # English
    "Nagaland": "en",  # English
    "Odisha": "or",  # Odia
    "Punjab": "pa",  # Punjabi
    "Rajasthan": "hi",  # Hindi
    "Sikkim": "ne",  # Nepali
    "Tamil Nadu": "ta",  # Tamil
    "Telangana": "te",  # Telugu
    "Tripura": "en",  # English
    "Uttar Pradesh": "hi",  # Hindi
    "Uttarakhand": "hi",  # Hindi
    "West Bengal": "bn",  # Bengali
    # Union Territories
    "Delhi": "hi",  # Hindi
    "Jammu and Kashmir": "ks",  # Kashmiri
    "Ladakh": "bo",  # Bodo
    "Puducherry": "ta",  # Tamil
    "Chandigarh": "hi",  # Hindi
    "Andaman and Nicobar Islands": "en",  # English
    "Lakshadweep": "ml",  # Malayalam
    "Dadra and Nagar Haveli and Daman and Diu": "gu"  # Gujarati
}

def normalize_text(text: str) -> str:
    """Enhanced text normalization with context-aware emotion detection."""


    text = text.lower().strip()
    
    # First try context-based sentence analysis
    def analyze_sentence_context(sentence: str) -> Optional[str]:
        # Common sentence patterns that indicate emotions
        context_patterns = {
            'joyful': [
                'had a great', 'feeling good about', 'looking forward to',
                'cant wait', 'excited about', 'loving this'
            ],
            'sad': [
                'missing', 'wish i could', 'not feeling', 'cant handle',
                'tired of', 'dont want to'
            ],
            'anxious': [
                'worried about', 'nervous for', 'hope everything',
                'not sure if', 'what if', 'stress about'
            ],
            'nostalgic': [
                'remember when', 'back in', 'used to', 'those days',
                'thinking about old', 'miss those'
            ],
            'peaceful': [
                'taking time', 'enjoying the', 'relaxing with',
                'feeling zen', 'at peace', 'calm day'
            ]
        }
        
        for emotion, patterns in context_patterns.items():
            if any(pattern in sentence for pattern in patterns):
                return emotion
        return None

    # Try context-based analysis first
    context_emotion = analyze_sentence_context(text)
    if context_emotion:
        return context_emotion
    
    # If no context match, try pattern matching from emotion_patterns
    for emotion, patterns in emotion_patterns.items():
        if any(pattern in text for pattern in patterns):
            return emotion
    
    # If still no match, use ML model analysis
    try:
        results = models[0](text)[0]  # Use first model for quick analysis
        if results and results[0]['score'] > 0.6:  # Only use if confidence is high
            return results[0]['label'].lower()
    except Exception as e:
        logging.warning(f"ML model analysis failed: {e}")
    
    # If everything fails, do sentiment analysis
    positive_count = sum(1 for word in positive_sentiment_words if word in text)
    negative_count = sum(1 for word in negative_sentiment_words if word in text)
    
    if positive_count > negative_count:
        return 'joyful'
    elif negative_count > positive_count:
        return 'sad'
    
    return "neutral"

def combined_emotion(text: str) -> List[Tuple[str, float]]:
    """Enhanced emotion detection with multiple models and confidence scoring."""


    try:
        # First try the basic emotion detection
        normalized_emotion = normalize_text(text)
        if normalized_emotion != "neutral":
            logging.info(f"combined_emotion: text='{text}', detected='{normalized_emotion}' (rule-based)")
            return [(normalized_emotion, 1.0)]

        # Use all models for comprehensive analysis
        all_results = []
        weights = [0.4, 0.3, 0.3]  # Different weights for different models
        
        for model, weight in zip(models, weights):
            try:
                results = model(text)[0]
                # Apply weight to scores
                weighted_results = [
                    (result['label'].lower(), result['score'] * weight)
                    for result in results
                ]
                all_results.extend(weighted_results)
            except Exception as e:
                logging.warning(f"Model failed: {e}")
                continue

        # Aggregate scores with context boost
        aggregated_scores = {}
        for label, score in all_results:
            if label in aggregated_scores:
                aggregated_scores[label] += score
            else:
                aggregated_scores[label] = score

        # Normalize scores
        total_score = sum(aggregated_scores.values())
        if total_score > 0:
            for label in aggregated_scores:
                aggregated_scores[label] /= total_score

        # Sort and return top emotions
        sorted_emotions = sorted(aggregated_scores.items(), key=lambda x: x[1], reverse=True)
        if sorted_emotions:
            logging.info(f"combined_emotion: text='{text}', top_emotions={sorted_emotions[:2]}")
        return sorted_emotions[:4]  # Return top 4 emotions with confidence scores

    except Exception as e:
        logging.error(f"Error in combined_emotion: {e}")
        return [("neutral", 1.0)]

def get_spotify_playlist(emotion: str, language: str) -> List[Dict[str, Any]]:
    """
    Copilot: Generate search queries dynamically using emotion and language
    """
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    import os
    import logging

    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    if not client_id or not client_secret:
        logging.error("Spotify client ID or secret not set in environment variables.")
        return get_default_playlists()

    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    all_playlists = []

    # Copilot: Generate search queries dynamically using emotion and language
    queries = [
        f"{emotion} {language} playlist",
        f"{emotion} {language} songs",
        f"{emotion} playlist",
        f"{emotion} songs",
        f"{language} playlist",
        f"{language} songs"
    ]

    for query in queries:
        try:
            # Copilot: Pass the market parameter for regional focus
            results = sp.search(q=query, type='playlist', limit=6, market='IN')
            if (results and isinstance(results, dict) and
                'playlists' in results and
                results['playlists'] is not None and
                'items' in results['playlists'] and
                results['playlists']['items'] is not None and
                isinstance(results['playlists']['items'], list) and
                len(results['playlists']['items']) > 0):
                for playlist in results['playlists']['items']:
                    followers = 0
                    if 'followers' in playlist and playlist['followers'] is not None:
                        followers = playlist['followers'].get('total', 0)
                    all_playlists.append({
                        'name': playlist.get('name', 'Unknown'),
                        'url': playlist.get('external_urls', {}).get('spotify', ''),
                        'image': playlist['images'][0]['url'] if playlist.get('images') else None,
                        'language': language.upper(),
                        'description': playlist.get('description', ''),
                        'followers': followers
                    })
            if all_playlists:
                break
        except Exception as e:
            logging.warning(f"Spotify search failed for query '{query}': {e}")
            continue

    if not all_playlists:
        return get_default_playlists()

    # Remove duplicates by playlist URL
    seen_urls = set()
    unique_playlists = []
    for playlist in all_playlists:
        if playlist['url'] not in seen_urls:
            unique_playlists.append(playlist)
            seen_urls.add(playlist['url'])
    all_playlists = unique_playlists

    # Sort by followers and return top 4
    all_playlists.sort(key=lambda x: x.get('followers', 0), reverse=True)
    return all_playlists[:4]

def get_default_playlists() -> List[Dict[str, Any]]:
    """Return default playlists when no matches are found."""


    return [
        {
            'name': 'Global Top Hits',
            'url': 'https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M',
            'image': None,
            'language': 'INTERNATIONAL',
            'description': 'Today\'s top hits from around the world.',
            'followers': 0
        },
        {
            'name': 'Chill Vibes',
            'url': 'https://open.spotify.com/playlist/37i9dQZF1DX889U0CL85jj',
            'image': None,
            'language': 'INTERNATIONAL',
            'description': 'Relaxing beats for any mood.',
            'followers': 0
        },
        {
            'name': 'Feel Good Mix',
            'url': 'https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0',
            'image': None,
            'language': 'INTERNATIONAL',
            'description': 'Uplifting songs to boost your mood.',
            'followers': 0
        },
        {
            'name': 'Mood Booster',
            'url': 'https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0',
            'image': None,
            'language': 'INTERNATIONAL',
            'description': 'Feel-good music for any occasion.',
            'followers': 0
        }
    ]

def predict_emoji(text: str, state: str) -> Tuple[str, str, str]:
    """Enhanced emoji prediction with better language matching and emotion detection."""
    try:
        # Get the language code for the state
        language = state_to_language.get(state, 'en')
        logging.debug(f"predict_emoji: state={state}, resolved_language={language}")
        # Get emotions with confidence scores
        emotions = combined_emotion(text)
        if not emotions:
            logging.warning("No emotions detected, using default")
            logging.debug(f"predict_emoji: text='{text}', state='{state}', emotion='neutral', emoji='🎵', language='{language}'")
            return emotion_to_emoji.get('default', '🎵'), get_emotion_name('neutral', language), language
        # Get the top emotion
        top_emotion, confidence = emotions[0]
        # Get emoji for the emotion, with fallbacks
        emoji = emotion_to_emoji.get(top_emotion)
        if not emoji:
            emoji = emotion_to_emoji.get('default', '🎵')
            logging.info(f"Using fallback emoji for emotion: {top_emotion}")
        # Get the localized emotion name
        emotion_name = get_emotion_name(top_emotion, language)
        logging.info(f"predict_emoji: text='{text}', state='{state}', emotion='{top_emotion}', emoji='{emoji}', language='{language}', confidence={confidence}")
        return emoji, emotion_name, language
    except Exception as e:
        logging.error(f"Error in predict_emoji: {e}")
        return emotion_to_emoji.get('default', '🎵'), get_emotion_name('neutral', language), 'en'


