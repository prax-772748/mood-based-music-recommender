// Common mood suggestions for autocomplete
const moodSuggestions = [
    "happy and energetic",
    "peaceful and calm",
    "romantic and dreamy",
    "sad and emotional",
    "excited and motivated",
    "relaxed and content",
    "nostalgic and reflective",
    "focused and determined",
    "creative and inspired",
    "playful and cheerful"
];

document.addEventListener('DOMContentLoaded', function() {
    initializeMoodInput();
    initializeVoiceInput();
    initializeAnimations();
    enhancePlaylistCards();
});

function initializeMoodInput() {
    const moodInput = document.getElementById('text_input');
    const suggestionsContainer = document.querySelector('.mood-suggestions');
    
    if (moodInput && suggestionsContainer) {
        // Create suggestions UI
        moodInput.addEventListener('input', function(e) {
            const value = e.target.value.toLowerCase();
            if (value.length < 3) {
                suggestionsContainer.style.display = 'none';
                return;
            }

            const matches = moodSuggestions.filter(suggestion => 
                suggestion.toLowerCase().includes(value)
            );

            if (matches.length) {
                suggestionsContainer.innerHTML = matches
                    .map(match => `<div class="mood-suggestion">${match}</div>`)
                    .join('');
                suggestionsContainer.style.display = 'block';

                // Add click handlers to suggestions
                document.querySelectorAll('.mood-suggestion').forEach(suggestion => {
                    suggestion.addEventListener('click', function() {
                        moodInput.value = this.textContent;
                        suggestionsContainer.style.display = 'none';
                    });
                });
            } else {
                suggestionsContainer.style.display = 'none';
            }
        });

        // Hide suggestions when clicking outside
        document.addEventListener('click', function(e) {
            if (!moodInput.contains(e.target)) {
                suggestionsContainer.style.display = 'none';
            }
        });
    }
}

function initializeVoiceInput() {
    const voiceBtn = document.querySelector('.voice-btn');
    const voiceIndicator = document.getElementById('voice-indicator');
    
    if (voiceBtn && 'webkitSpeechRecognition' in window) {
        const recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        
        recognition.onstart = function() {
            voiceIndicator.classList.remove('hidden');
            voiceBtn.classList.add('active');
        };
        
        recognition.onend = function() {
            voiceIndicator.classList.add('hidden');
            voiceBtn.classList.remove('active');
        };
        
        recognition.onresult = function(event) {
            const text = event.results[0][0].transcript;
            document.getElementById('text_input').value = text;
        };
        
        window.startVoiceInput = function() {
            recognition.start();
        };
    } else if (voiceBtn) {
        voiceBtn.style.display = 'none';
    }
}

function initializeAnimations() {
    // Add entrance animations to cards
    const cards = document.querySelectorAll('.playlist-card, .mood-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });

    // Add hover effects to buttons
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('mousedown', function(e) {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            
            btn.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    });
}

function enhancePlaylistCards() {
    const playlistCards = document.querySelectorAll('.playlist-card');
    
    playlistCards.forEach(card => {
        // Add keyboard navigation
        card.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                const link = this.querySelector('.btn-spotify');
                if (link) link.click();
            }
        });

        // Lazy load images
        const img = card.querySelector('img');
        if (img) {
            img.loading = 'lazy';
            
            // Add loading animation
            img.addEventListener('load', function() {
                this.classList.add('loaded');
            });
        }
    });
}

// Handle form submissions with loading state
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function() {
        const btn = this.querySelector('button[type="submit"]');
        if (btn) {
            btn.disabled = true;
            btn.innerHTML = '<span class="loading-dots">Processing</span>';
        }
    });
});
