# Cloud Deployment & Demo Access Guide

## 1. Quick Cloud Deploy (Render, Railway, Replit, etc.)
- **Render:**
  1. Go to https://render.com and create a new Web Service.
  2. Connect your GitHub repo or upload the code.
  3. Set build command: `pip install -r requirements.txt`
  4. Set start command: `python app.py`
  5. Add environment variables:
     - `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` (from your Spotify Developer Dashboard)
     - `SECRET_KEY` (any random string)
     - `DEMO_SECRET` (your secret link code, e.g. `letmein2025`)
     - `DEBUG` (optional, `True` or `False`)
  6. Deploy. Your app will be live at a public URL.

- **Railway:**
  1. Go to https://railway.app and create a new project.
  2. Deploy from GitHub or upload code.
  3. Add the same environment variables as above.
  4. Set up Python build and start commands.
  5. Deploy and get your public URL.

- **Replit:**
  1. Import the repo or upload code.
  2. Add environment variables in the Secrets tab.
  3. Click "Run" to start the app.

## 2. Secure Demo Access (No Password Prompt)
- Share your app URL with the secret query parameter, e.g.:
  `https://your-app.onrender.com/?access=letmein2025`
- All main routes require this secret. If missing or wrong, users are redirected to login.
- No password prompt, just a secret link for easy sharing.

## 3. Notes
- **Spotify API:** You must set up your own Spotify Developer credentials.
- **Session Security:** The secret is stored in the session after first access.
- **Multiple Users:** Each user can have their own session and mood history.
- **No installation needed for users:** Just share the link with the secret.

## 4. Troubleshooting
- If you see Spotify errors, check your API credentials and environment variables.
- If you see "Access denied", make sure you are using the correct secret in the URL.

## 5. Example .env file
```
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SECRET_KEY=your_flask_secret
DEMO_SECRET=letmein2025
DEBUG=True
```

---
For more help, see the README or open an issue.
