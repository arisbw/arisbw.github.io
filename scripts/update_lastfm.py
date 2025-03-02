import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_top_artists(api_key, username, period='7day', limit=5):
    """Fetch top artists from Last.fm"""
    url = 'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': 'user.gettopartists',
        'user': username,
        'api_key': api_key,
        'format': 'json',
        'period': period,
        'limit': limit
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    
    if 'error' in data:
        raise Exception(f"Last.fm API error: {data['message']}")
    
    artists = []
    for artist in data['topartists']['artist']:
        artists.append({
            'name': artist['name'],
            'playcount': int(artist['playcount']),
            'url': artist['url']
        })
    
    return artists

def get_recent_tracks(api_key, username, limit=10):
    """Fetch recent tracks from Last.fm"""
    url = 'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': 'user.getrecenttracks',
        'user': username,
        'api_key': api_key,
        'format': 'json',
        'limit': limit
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    tracks = []
    for track in data['recenttracks']['track']:
        # Skip currently playing track if any
        if '@attr' in track and track['@attr'].get('nowplaying') == 'true':
            continue
            
        tracks.append({
            'artist': track['artist']['#text'],
            'name': track['name'],
            'album': track['album']['#text'],
            'url': track['url']
        })
    
    return tracks

def update_music_data():
    """Update music data file"""
    api_key = os.getenv('LASTFM_API_KEY')
    username = 'arisbw'
    
    if not api_key:
        raise ValueError("Last.fm API key not found in environment variables")
    
    data = {
        'last_updated': datetime.now().isoformat(),
        'top_artists': get_top_artists(api_key, username),
        'recent_tracks': get_recent_tracks(api_key, username)
    }
    
    # Ensure the _data directory exists
    os.makedirs('_data', exist_ok=True)
    
    # Save the data
    with open('_data/music.json', 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    update_music_data()
