# Cloud Deployment & Demo Access Guide

## 1. Deployment Instructions (Render)

1. Go to https://render.com and create a new Web Service
2. Connect your GitHub repository
3. Configure the following settings:
   - **Name**: mood-music-recommender (or your preferred name)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Python Version**: 3.11.0

4. Add the following environment variables:
   ```
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   SECRET_KEY=your_random_secret_key
   DEMO_SECRET=your_access_code
   DEBUG=false
   ```

5. Deploy the service

## 2. Troubleshooting

If you encounter deployment issues:

1. Check the deployment logs in Render dashboard
2. Verify all environment variables are set correctly
3. Make sure Spotify API credentials are valid
4. Check the Python version is set to 3.11.0
5. Ensure gunicorn is in requirements.txt

## 3. Testing Deployment

1. After deployment, append `?access=your_demo_secret` to the URL
2. Test different emotions and languages to verify playlist recommendations
3. Monitor logs for any errors

## 4. Maintenance

- Monitor usage and adjust the free instance settings if needed
- Keep dependencies updated
- Check Spotify API quota usage
- Monitor error logs regularly
