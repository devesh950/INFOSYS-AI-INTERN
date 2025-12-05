"""
YouTube Search Functionality
Searches YouTube videos using the YouTube Data API v3.
"""

import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class YouTubeSearcher:
    """Handles YouTube video searches using the YouTube Data API."""
    
    def __init__(self, api_key=None):
        """
        Initialize the YouTube API client.
        
        Args:
            api_key (str): YouTube Data API key. If None, loads from .env file.
        """
        self.api_key = api_key or os.getenv('YOUTUBE_API_KEY')
        if not self.api_key:
            raise ValueError("YouTube API key not found. Please set YOUTUBE_API_KEY in .env file.")
        
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
    
    def search_videos(self, query, max_results=10):
        """
        Search for YouTube videos.
        
        Args:
            query (str): Search query
            max_results (int): Maximum number of results to return (default: 10)
            
        Returns:
            list: List of dictionaries containing video information:
                - video_id: YouTube video ID
                - title: Video title
                - channel: Channel name
                - description: Video description
        """
        try:
            # Call the YouTube API
            request = self.youtube.search().list(
                part='snippet',
                q=query,
                type='video',
                maxResults=max_results,
                relevanceLanguage='en',
                videoCaption='any'
            )
            response = request.execute()
            
            # Extract video information
            videos = []
            for item in response.get('items', []):
                video_info = {
                    'video_id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'channel': item['snippet']['channelTitle'],
                    'description': item['snippet']['description']
                }
                videos.append(video_info)
            
            return videos
            
        except Exception as e:
            print(f"Error searching YouTube: {e}")
            return []
