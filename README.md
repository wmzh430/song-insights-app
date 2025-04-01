# 🎵 Song Insights Web App

A simple Flask-based web application that allows an admin to input a song (Artist and Title), then returns:
- A **1-sentence summary** of the song's lyrics
- A list of **countries mentioned** in the lyrics

---

## 🚀 Features

- ✅ Enter artist and song title via web form
- ✅ Retrieves partial lyrics using the Musixmatch API
- ✅ Summarizes the lyrics in a single sentence using GPT-4
- ✅ Extracts any mentioned countries using GPT-4
- ✅ Caches results to avoid redundant API calls
- ✅ Displays error if lyrics are not found

---

## 🧠 Tech Stack

- Backend: [Python 3.10+](https://www.python.org/), [Flask](https://flask.palletsprojects.com/)
- APIs: 
  - [Musixmatch API](https://developer.musixmatch.com/) – for fetching lyrics
  - [OpenAI GPT API](https://platform.openai.com/docs/) – for summarization and country extraction
- Deployment: Works locally or can be deployed on services like Heroku, Render, or Fly.io

---

## 📦 Setup Instructions

1. **Clone the repository**
```bash
git https://github.com/wmzh430/song-insights-app.git
cd song-insights-app
```

2. **Create and activate a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create a `.env` file**
```ini
MUSIXMATCH_API_KEY=your_musixmatch_api_key
OPENAI_API_KEY=your_openai_api_key
```
 ⚠️ Do not share your .env or API keys in public repositories.

 ## 🔧 Running the App
 Once everything is set up, run the app using:
```bash
python app.py
```
Then open your browser and visit:
http://127.0.0.1:5000/