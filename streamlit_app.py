"""
YouTube Search App with Transcript Filter
A Streamlit web application that searches YouTube videos and filters by transcript availability.
"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.milestone1.search_youtube import YouTubeSearcher
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

# Page configuration
st.set_page_config(
    page_title="YouTube Search with Transcripts",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS for white background and better styling
st.markdown("""
    <style>
    .stApp {
        background-color: white;
    }
    .main {
        background-color: white;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        color: #1a1a1a;
        text-align: center;
        padding: 1.5rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .video-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        border: 1px solid #e9ecef;
    }
    .video-title {
        color: #2c3e50;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .channel-name {
        color: #7f8c8d;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    .transcript-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    .badge-available {
        background-color: #d4edda;
        color: #155724;
    }
    .badge-auto {
        background-color: #cce5ff;
        color: #004085;
    }
    .badge-unavailable {
        background-color: #f8d7da;
        color: #721c24;
    }
    .stButton>button {
        background-color: #667eea;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        border: none;
        font-weight: 500;
    }
    .stButton>button:hover {
        background-color: #764ba2;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.markdown("<h1>🎬 YouTube Search with Transcripts</h1>", unsafe_allow_html=True)

# Initialize session state
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'last_query' not in st.session_state:
    st.session_state.last_query = ""

# Search interface
col1, col2 = st.columns([3, 1])

with col1:
    search_query = st.text_input(
        "Search YouTube videos",
        placeholder="Enter your search query...",
        label_visibility="collapsed"
    )

with col2:
    transcript_filter = st.checkbox("Only show videos with English transcripts", value=False)

# Popular topics
st.markdown("### 🎯 Popular Topics")
topics_col1, topics_col2, topics_col3, topics_col4 = st.columns(4)

with topics_col1:
    if st.button("🎤 TED Talks"):
        search_query = "TED talk"
    if st.button("📚 Khan Academy"):
        search_query = "Khan Academy"

with topics_col2:
    if st.button("🎓 Crash Course"):
        search_query = "Crash Course"
    if st.button("🌌 Kurzgesagt"):
        search_query = "Kurzgesagt"

with topics_col3:
    if st.button("💻 freeCodeCamp"):
        search_query = "freeCodeCamp"
    if st.button("🌍 National Geographic"):
        search_query = "National Geographic"

with topics_col4:
    if st.button("🏛️ MIT OpenCourseWare"):
        search_query = "MIT OpenCourseWare"
    if st.button("🎓 Stanford Online"):
        search_query = "Stanford Online"

def check_transcript_availability(video_id):
    """
    Check if a video has English transcripts available.
    Returns: (has_transcript, is_auto_generated)
    """
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Check for manual English transcript
        try:
            transcript = transcript_list.find_manually_created_transcript(['en'])
            return True, False
        except:
            pass
        
        # Check for auto-generated English transcript
        try:
            transcript = transcript_list.find_generated_transcript(['en'])
            return True, True
        except:
            pass
        
        return False, False
        
    except (TranscriptsDisabled, NoTranscriptFound):
        return False, False
    except Exception as e:
        return False, False

def get_transcript(video_id):
    """Get English transcript for a video (manual or auto-generated)."""
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Try manual transcript first
        try:
            transcript = transcript_list.find_manually_created_transcript(['en'])
            transcript_data = transcript.fetch()
            return " ".join([entry['text'] for entry in transcript_data])
        except:
            pass
        
        # Try auto-generated transcript
        try:
            transcript = transcript_list.find_generated_transcript(['en'])
            transcript_data = transcript.fetch()
            return " ".join([entry['text'] for entry in transcript_data])
        except:
            pass
        
        return None
        
    except Exception as e:
        return None

# Perform search
if search_query and search_query != st.session_state.last_query:
    st.session_state.last_query = search_query
    
    with st.spinner("Searching YouTube..."):
        try:
            searcher = YouTubeSearcher()
            results = searcher.search_videos(search_query, max_results=20)
            
            # Check transcript availability for each video
            results_with_transcripts = []
            for video in results:
                has_transcript, is_auto = check_transcript_availability(video['video_id'])
                video['has_transcript'] = has_transcript
                video['is_auto_generated'] = is_auto
                results_with_transcripts.append(video)
            
            # Filter by transcript if requested
            if transcript_filter:
                results_with_transcripts = [v for v in results_with_transcripts if v['has_transcript']]
            
            st.session_state.search_results = results_with_transcripts
            
        except Exception as e:
            st.error(f"Error searching YouTube: {str(e)}")
            st.info("💡 Make sure you have set your YouTube API key in the .env file")

# Display results
if st.session_state.search_results:
    st.markdown(f"### 📺 Found {len(st.session_state.search_results)} videos")
    
    if transcript_filter and len(st.session_state.search_results) == 0:
        st.warning("No videos with English transcripts found. Try disabling the transcript filter or searching for different content.")
    
    for idx, video in enumerate(st.session_state.search_results[:10], 1):
        with st.container():
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            
            # Video title and metadata
            st.markdown(f'<div class="video-title">{idx}. {video["title"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="channel-name">📺 {video["channel"]}</div>', unsafe_allow_html=True)
            
            # Transcript availability badge
            if video['has_transcript']:
                if video['is_auto_generated']:
                    st.markdown('<span class="transcript-badge badge-auto">✓ Auto-generated English transcript</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="transcript-badge badge-available">✓ Manual English transcript</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="transcript-badge badge-unavailable">✗ No English transcript (not accessible via API)</span>', unsafe_allow_html=True)
            
            # Video description
            if video['description']:
                with st.expander("📄 Description"):
                    st.write(video['description'])
            
            # Embedded video player
            video_url = f"https://www.youtube.com/watch?v={video['video_id']}"
            st.video(video_url)
            
            # Show transcript if available
            if video['has_transcript']:
                with st.expander("📝 View Transcript"):
                    with st.spinner("Loading transcript..."):
                        transcript_text = get_transcript(video['video_id'])
                        if transcript_text:
                            st.text_area(
                                "Transcript",
                                transcript_text,
                                height=200,
                                label_visibility="collapsed"
                            )
                        else:
                            st.info("Transcript is available on YouTube but couldn't be loaded via API.")
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("---")

elif st.session_state.last_query:
    st.info("No results found. Try a different search query.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; padding: 1rem;'>
    <p>💡 Search across all YouTube videos • Filter by English transcripts • Watch embedded videos</p>
    <p style='font-size: 0.8rem;'>Note: Some videos have captions on YouTube but may not be accessible via API</p>
</div>
""", unsafe_allow_html=True)
