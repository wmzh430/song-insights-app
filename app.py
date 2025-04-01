# app.py
from flask import Flask, request, render_template, redirect, url_for
import requests
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# API keys (Store securely in real project)
MUSIXMATCH_API_KEY = os.getenv("MUSIXMATCH_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# Cache to avoid redundant requests
cache = {}

# Home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        artist = request.form['artist']
        title = request.form['title']
        return redirect(url_for('song_summary', artist=artist, title=title))
    return render_template('index.html')

# Fetch lyrics from Musixmatch API
def get_lyrics(artist, title):
    url = f"https://api.musixmatch.com/ws/1.1/matcher.lyrics.get"
    params = {"q_artist": artist, "q_track": title, "apikey": MUSIXMATCH_API_KEY}
    response = requests.get(url, params=params)
    data = response.json()
    if data["message"]["header"]["status_code"] != 200:
        return None
    lyrics = data["message"]["body"].get("lyrics", {}).get("lyrics_body", "")
    return lyrics

# Summarize lyrics using OpenAI GPT
def summarize_lyrics(lyrics):
    prompt = f"Summarize the following lyrics in one concise sentence:\n{lyrics}"
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50
    )
    summary = response.choices[0].message.content.strip()
    return summary

# Extract countries mentioned using OpenAI GPT
def extract_countries(lyrics):
    prompt = f"From the following song lyrics, extract only the names of sovereign countries that are explicitly mentioned. Return the result as a comma-separated list with no explanation, no extra text, and no formatting — just the country names.\n\n Lyrics:\n{lyrics}\nIf none, return 'None'."
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50
    )
    extracted = response.choices[0].message.content.strip()
    if extracted.lower() == 'none':
        return []
    return [country.strip() for country in extracted.split(",")]

@app.route('/summary')
def song_summary():
    artist = request.args.get('artist')
    title = request.args.get('title')
    cache_key = f"{artist}-{title}"

    if cache_key in cache:
        summary, countries = cache[cache_key]
    else:
        lyrics = get_lyrics(artist, title)
        if not lyrics:
            return render_template('error.html', message="Lyrics not found.")

        summary = summarize_lyrics(lyrics)
        countries = extract_countries(lyrics)

        cache[cache_key] = (summary, countries)

    return render_template('summary.html', artist=artist, title=title, summary=summary, countries=countries)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
