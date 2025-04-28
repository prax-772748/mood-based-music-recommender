"""
Centralized emotion mappings for the music recommendation app.
Contains emoji mappings and emotion detection patterns.
"""

# Comprehensive Emotion-to-Emoji Mapping
emotion_to_emoji = {
    # Positive Emotions
    "joyful": "😀",
    "peaceful": "😌",
    "excited": "🤩",
    "hopeful": "🌟",
    "content": "😊",
    "energetic": "⚡",
    "cheerful": "😁",
    "grateful": "🙏",
    "inspired": "✨",
    "loving": "😍",
    "playful": "😜",
    "uplifted": "🎉",
    "blissful": "😇",
    "confident": "💪",
    "proud": "🏆",
    "affectionate": "❤️",
    "optimistic": "🌈",
    "curious": "🤔",
    "empowered": "🔥",
    "nostalgic": "🎶",
    
    # Negative Emotions
    "sad": "😢",
    "lonely": "😔",
    "angry": "😡",
    "frustrated": "😤",
    "anxious": "😰",
    "fearful": "😨",
    "disappointed": "😞",
    "melancholic": "🎻",
    "heartbroken": "💔",
    "envious": "😒",
    "guilty": "😓",
    "jealous": "😠",
    "tense": "😬",
    "annoyed": "😑",
    "vulnerable": "🤕",
    "overwhelmed": "😵",
    "regretful": "😟",
    "bitter": "😖",
    "desperate": "😩",
    
    # Neutral Emotions
    "calm": "😌",
    "relaxed": "🛋️",
    "serene": "🌅",
    "thoughtful": "🤔",
    "reflective": "🪞",
    "indifferent": "😑",
    "conflicted": "🤷",
    "dreamy": "🌙",
    "surprised": "😲",
    "awestruck": "😮",
    "neutral": "😐",
    "balanced": "⚖️",
    "unknown": "🎵",
    
    # Additional Emotions
    "determined": "💯",
    "motivated": "🎯",
    "creative": "🎨",
    "satisfied": "😋",
    "blessed": "🙌",
    "victorious": "🏅",
    "adventurous": "🌎",
    "refreshed": "🌊",
    "appreciated": "💝",
    "focused": "🎯",
    "balanced": "☯️",
    "mindful": "🧘",
    "free": "🦋",
    "magical": "✨",
    "powerful": "⚡",
    "brave": "🦁",
    "silly": "🤪",
    "grumpy": "😾",
    "mischievous": "😈",
    "hangry": "🍔",
    "sleepy": "😴",
    "hyper": "🤸",
    "sassy": "💁",
    "goofy": "🤓",
    "dramatic": "🎭",
    "puzzled": "🤔",
    "sick": "🤒",
    "stressed": "😫",
    "tired": "😩",
    "wired": "⚡",
    "zealous": "🔥",
    "ecstatic": "🤩",
    "giggly": "😝",
    "rebellious": "😎",
    "feisty": "💪",
    "fierce": "🐯",
    "gentle": "🕊️",
    "humble": "🙇",
    "mysterious": "🔮",
    "nervous": "😰",
    "nostalgic": "📷",
    "passionate": "❤️‍🔥",
    "peaceful": "🕊️",
    "pensive": "🤔",
    "playful": "🎮",
    "proud": "🦚",
    "romantic": "🌹",
    "sarcastic": "😏",
    "shocked": "😱",
    "sophisticated": "🎩",
    "spicy": "🌶️",
    "spiritual": "🕉️",
    "sweet": "🍯",
    "wild": "🎪",
    
    # Fallback states
    "default": "🎵",
    "indeterminate": "🎶"
}

# Expanded emotion mappings with sentence patterns
emotion_patterns = {
    'joyful': [
        'happy', 'joy', 'delighted', 'excited', 'wonderful', 'great',
        'feeling good', 'having a great day', 'loving life', 'so happy',
        'feeling blessed', 'amazing day', 'best day'
    ],
    'sad': [
        'sad', 'unhappy', 'depressed', 'down', 'blue', 'miserable',
        'feeling down', 'having a bad day', 'want to cry', 'missing',
        'heartbroken', 'lonely', 'lost', 'feeling empty'
    ],
    'angry': [
        'angry', 'mad', 'furious', 'irritated', 'annoyed',
        'cant stand', 'hate this', 'so frustrated', 'fed up',
        'getting on my nerves', 'makes me mad'
    ],
    'peaceful': [
        'peaceful', 'calm', 'relaxed', 'serene', 'tranquil',
        'at peace', 'feeling zen', 'meditation', 'mindful',
        'taking it easy', 'chilling'
    ],
    'energetic': [
        'energetic', 'active', 'lively', 'pumped', 'dynamic',
        'full of energy', 'ready to go', 'feeling strong',
        'cant sit still', 'lets do this'
    ],
    'romantic': [
        'love', 'romantic', 'passionate', 'in love',
        'feeling butterflies', 'crush', 'heart racing',
        'cant stop thinking about'
    ],
    'nostalgic': [
        'nostalgic', 'memories', 'remember', 'missing old days',
        'good old times', 'throwback', 'reminiscing', 'back then',
        'used to', 'childhood memories'
    ],
    'anxious': [
        'anxious', 'worried', 'nervous', 'stressed',
        'cant stop worrying', 'overthinking', 'scared about',
        'fear', 'panic', 'feeling uneasy'
    ],
    # Additional emotion patterns
    'spiritual': [
        'enlightened', 'connected', 'divine', 'sacred',
        'spiritual awakening', 'universal love', 'inner peace',
        'higher purpose', 'meditation', 'mindfulness'
    ],
    'rebellious': [
        'breaking rules', 'different path', 'my own way',
        'against the grain', 'rebel', 'not following',
        'standing out', 'unique', 'controversial'
    ],
    'creative': [
        'inspired to create', 'artistic flow', 'imagination flowing',
        'new ideas', 'creative energy', 'making art',
        'expressing myself', 'innovative mood', 'artistic spirit'
    ],
    'adventurous': [
        'seeking adventure', 'exploring', 'discovering',
        'trying new things', 'taking risks', 'wanderlust',
        'travel mood', 'expedition', 'quest'
    ],
    'fierce': [
        'unstoppable', 'powerful', 'strong minded',
        'determined', 'intense', 'fierce attitude',
        'showing strength', 'dominating', 'commanding'
    ]
}

# Language-specific emotion names
emotion_names = {
    'en': {
        'joyful': 'Joyful',
        'sad': 'Sad',
        'angry': 'Angry',
        'peaceful': 'Peaceful',
        'energetic': 'Energetic',
        'romantic': 'Romantic',
        'nostalgic': 'Nostalgic',
        'anxious': 'Anxious'
    },
    'hi': {
        'joyful': 'खुश',
        'sad': 'दुखी',
        'angry': 'गुस्सा',
        'peaceful': 'शांत',
        'energetic': 'ऊर्जावान',
        'romantic': 'रोमांटिक',
        'nostalgic': 'यादगार',
        'anxious': 'चिंतित'
    },
    'te': {
        'joyful': 'సంతోషం',
        'sad': 'విచారం',
        'angry': 'కోపం',
        'peaceful': 'శాంతి',
        'energetic': 'శక్తివంతమైన',
        'romantic': 'రొమాంటిక్',
        'nostalgic': 'గతకాలపు',
        'anxious': 'ఆందోళన'
    },
    'ta': {
        'joyful': 'மகிழ்ச்சி',
        'sad': 'சோகம்',
        'angry': 'கோபம்',
        'peaceful': 'அமைதி',
        'energetic': 'சக்திவாய்ந்த',
        'romantic': 'காதல்',
        'nostalgic': 'நினைவுகள்',
        'anxious': 'பதற்றம்'
    },
    'ml': {
        'joyful': 'സന്തോഷം',
        'sad': 'ദുഃഖം',
        'angry': 'ദേഷ്യം',
        'peaceful': 'സമാധാനം',
        'energetic': 'ഊർജ്ജസ്വലമായ',
        'romantic': 'റൊമാന്റിക്',
        'nostalgic': 'നോസ്റ്റാൾജിക്',
        'anxious': 'ആശങ്ക'
    }
}

def get_emotion_name(emotion, language_code):
    """Get the emotion name in the specified language."""
    if language_code in emotion_names:
        return emotion_names[language_code].get(emotion, emotion.title())
    return emotion.title()

# Sentiment Analysis Words
positive_sentiment_words = [
    'good', 'great', 'awesome', 'fantastic', 'wonderful', 'amazing',
    'love', 'happy', 'excellent', 'perfect', 'brilliant', 'beautiful',
    'blessed', 'grateful', 'thankful', 'joyful', 'delighted', 'pleased',
    'superb', 'outstanding'
]

negative_sentiment_words = [
    'bad', 'terrible', 'horrible', 'awful', 'hate', 'dislike',
    'sad', 'angry', 'worst', 'poor', 'disappointing', 'frustrated',
    'upset', 'irritated', 'annoyed', 'miserable', 'depressed', 'unhappy',
    'despair', 'regret'
]