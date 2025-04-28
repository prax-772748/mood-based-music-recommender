import unittest
from app import app, normalize_text, predict_emoji, combined_emotion

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def test_post_analysis(self):
        response = self.app.post("/", data={"text_input": "I feel happy", "username": "TestUser"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Detected Mood(s):", response.data)
    
    def test_normalize_text(self):
        self.assertEqual(normalize_text("I am happy"), "joyful")
        self.assertEqual(normalize_text("I feel sad"), "sad")
        self.assertEqual(normalize_text("I am calm"), "calm")
    
    def test_predict_emoji(self):
        emoji, playlists = predict_emoji("I am happy", ip_address="8.8.8.8")
        assert emoji == "😀"
        assert "Happy Mix" in playlists

    def test_combined_emotion(self):
        emotions = combined_emotion("I feel joyful and excited")
        assert len(emotions) > 0
        assert emotions[0][0] in ["joyful", "excited"]
    
if __name__ == "__main__":
    unittest.main()