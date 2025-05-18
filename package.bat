@echo off
echo Packaging Music Mood Recommender...

rem Create a new zip file
powershell Compress-Archive -Force -Path ^
"app.py", ^
"config.py", ^
"emoji_predictor.py", ^
"emotion_mappings.py", ^
"handlers.py", ^
"requirements.txt", ^
"README.md", ^
"static", ^
"templates" ^
-DestinationPath "music_mood_recommender.zip"

echo.
echo Project packaged successfully as 'music_mood_recommender.zip'
echo Now you can share this zip file everyone with the setup instructions in README.md
pause