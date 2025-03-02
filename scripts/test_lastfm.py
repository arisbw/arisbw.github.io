from dotenv import load_dotenv
import os
import requests

def test_api_key():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('LASTFM_API_KEY')
    if not api_key:
        print("❌ Error: LASTFM_API_KEY not found in .env file")
        return False
    
    print(f"Found API key: {api_key[:4]}...{api_key[-4:]}")
    
    # Test API key with a simple request
    url = 'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': 'user.getinfo',
        'user': 'arisbw',
        'api_key': api_key,
        'format': 'json'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'user' in data:
            print("✅ Success! API key is working")
            print(f"Connected to Last.fm account: {data['user']['name']}")
            return True
        else:
            print("❌ Error: Unexpected API response")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == '__main__':
    test_api_key()
