"""
QueryTube - Real-Time YouTube Search
Search ALL of YouTube and get top 5 most relevant videos instantly!
"""

import streamlit as st
from src.milestone1.search_youtube import YouTubeSearcher
from youtube_transcript_api import YouTubeTranscriptApi
import time

# Page configuration
st.set_page_config(
    page_title="QueryTube - YouTube Search",
    page_icon="🎥",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    /* Background gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Main content - solid white */
    .block-container {
        background: #ffffff;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    }
    
    /* Headers - dark text */
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: #1a1a1a !important;
    }
    
    /* Search box */
    .stTextInput input {
        background: white !important;
        color: #1a1a1a !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 10px !important;
        padding: 12px !important;
        font-size: 16px !important;
    }
    
    .stTextInput input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102,126,234,0.1) !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
        color: white;
        font-weight: 700;
        padding: 12px 40px;
        border-radius: 30px;
        border: none;
        font-size: 16px;
        box-shadow: 0 4px 15px rgba(255,107,53,0.3);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255,107,53,0.5);
    }
    
    /* Video cards */
    .video-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .video-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        border-color: #667eea;
    }
    
    .video-title {
        color: #1a1a1a !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        margin-bottom: 10px !important;
    }
    
    .video-meta {
        color: #606060 !important;
        font-size: 14px !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize YouTube searcher
@st.cache_resource
def load_searcher():
    return YouTubeSearcher()

try:
    searcher = load_searcher()
except Exception as e:
    st.error(f"❌ Error loading YouTube API: {e}")
    st.stop()

# Header
st.markdown("""
<div style="text-align: center; padding: 40px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            border-radius: 20px; margin-bottom: 30px; box-shadow: 0 8px 32px rgba(0,0,0,0.3);">
    <h1 style="color: white !important; margin: 0; font-size: 48px; font-weight: 800;">
        🎥 QueryTube
    </h1>
    <p style="color: rgba(255,255,255,0.95) !important; margin: 15px 0 0 0; font-size: 22px; font-weight: 600;">
        Search ALL of YouTube • Get Top 5 Most Relevant Videos
    </p>
    <p style="color: rgba(255,255,255,0.85) !important; margin: 10px 0 0 0; font-size: 16px;">
        🚀 Real-time search • No pre-downloading needed
    </p>
</div>
""", unsafe_allow_html=True)

# Search section
st.markdown("### 🔍 What do you want to watch today?")

# Filter option
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("")  # Spacing
with col2:
    only_transcripts = st.checkbox("📝 Only show videos with transcripts", value=False)

col1, col2 = st.columns([3, 1])

with col1:
    query = st.text_input(
        "Search YouTube",
        placeholder="Type anything... (e.g., 'python tutorial', 'cooking recipes', 'funny cats')",
        label_visibility="collapsed",
        key="search_query"
    )

with col2:
    search_button = st.button("🔍 Search", use_container_width=True)

# Example searches - Topics with transcripts
st.markdown("**💡 Popular Topics (High Transcript Availability):**")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🎓 TED Talks", use_container_width=True):
        st.session_state.clicked_query = "TED talks"
        st.rerun()

with col2:
    if st.button("📺 Khan Academy", use_container_width=True):
        st.session_state.clicked_query = "Khan Academy"
        st.rerun()

with col3:
    if st.button("🎬 Crash Course", use_container_width=True):
        st.session_state.clicked_query = "Crash Course"
        st.rerun()

with col4:
    if st.button("🔬 Kurzgesagt", use_container_width=True):
        st.session_state.clicked_query = "Kurzgesagt"
        st.rerun()

col5, col6, col7, col8 = st.columns(4)

with col5:
    if st.button("💻 freeCodeCamp", use_container_width=True):
        st.session_state.clicked_query = "freeCodeCamp"
        st.rerun()

with col6:
    if st.button("🌍 Nat Geo", use_container_width=True):
        st.session_state.clicked_query = "National Geographic"
        st.rerun()

with col7:
    if st.button("📚 MIT Lectures", use_container_width=True):
        st.session_state.clicked_query = "MIT OpenCourseWare"
        st.rerun()

with col8:
    if st.button("🎓 Stanford", use_container_width=True):
        st.session_state.clicked_query = "Stanford lecture"
        st.rerun()

# Handle button clicks BEFORE getting query
if 'clicked_query' in st.session_state:
    query = st.session_state.clicked_query
    search_button = True
    del st.session_state.clicked_query
else:
    # Get query from text input
    query = st.session_state.get('search_query', '')

# Perform search
if search_button and query:
    with st.spinner(f"🔍 Searching YouTube for '{query}'..."):
        videos = searcher.search_videos(query, max_results=20)  # Get more videos to filter
    
    if videos:
        # Filter videos if transcript-only option is selected
        if only_transcripts:
            filtered_videos = []
            with st.spinner("🔍 Checking transcripts..."):
                for video in videos:
                    try:
                        # Check if English transcript exists (manual or auto-generated)
                        transcript_list = YouTubeTranscriptApi.list_transcripts(video['video_id'])
                        try:
                            # Try to find English transcript (manual or auto)
                            transcript = transcript_list.find_transcript(['en'])
                            filtered_videos.append(video)
                            if len(filtered_videos) >= 5:  # Stop after finding 5
                                break
                        except:
                            # Try auto-generated English transcript
                            try:
                                transcript = transcript_list.find_generated_transcript(['en'])
                                filtered_videos.append(video)
                                if len(filtered_videos) >= 5:
                                    break
                            except:
                                continue
                    except:
                        continue
            
            videos = filtered_videos
        else:
            videos = videos[:5]  # Just take first 5 if no filter
        
        if videos:
            st.success(f"✅ Found {len(videos)} video{'s' if len(videos) != 1 else ''}!")
        else:
            st.warning("⚠️ No videos with English transcripts found. Try a different search or uncheck the filter.")
            st.stop()
        
        st.markdown("---")
        
        for i, video in enumerate(videos, 1):
            st.markdown(f"""
            <div class="video-card">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
                    <span style="background: #FF0000; color: white; padding: 6px 12px; 
                                 border-radius: 6px; font-weight: 700;">#{i}</span>
                    <span class="video-title">{video['title']}</span>
                </div>
            """, unsafe_allow_html=True)
            
            # Smaller video player with column layout
            col1, col2 = st.columns([3, 2])
            
            with col1:
                st.video(video['url'])
            
            with col2:
                # Metadata
                st.markdown(f"""
                <div class="video-meta">
                    📺 <strong>Channel:</strong> {video['channel_title']}<br>
                    📅 <strong>Published:</strong> {video['published_date'][:10]}<br><br>
                    <a href="{video['url']}" target="_blank" 
                       style="display: inline-block; background: #FF0000; color: white; 
                              padding: 8px 20px; border-radius: 20px; text-decoration: none; 
                              font-weight: 600; font-size: 13px;">
                        ▶️ Open in YouTube
                    </a>
                </div>
                """, unsafe_allow_html=True)
            
            # Try to get English transcript (manual or auto-generated)
            with st.expander("📝 View Transcript"):
                try:
                    # Try to get English transcript specifically
                    transcript_list = YouTubeTranscriptApi.list_transcripts(video['video_id'])
                    
                    # Try manual English first
                    try:
                        transcript = transcript_list.find_transcript(['en'])
                        transcript_data = transcript.fetch()
                        transcript_text = " ".join([entry['text'] for entry in transcript_data])
                        st.success("✅ English transcript available")
                        st.text_area("Transcript", transcript_text, height=150, label_visibility="collapsed")
                    except:
                        # Try auto-generated English
                        try:
                            transcript = transcript_list.find_generated_transcript(['en'])
                            transcript_data = transcript.fetch()
                            transcript_text = " ".join([entry['text'] for entry in transcript_data])
                            st.success("✅ English transcript available (Auto-generated)")
                            st.text_area("Transcript", transcript_text, height=150, label_visibility="collapsed")
                        except:
                            # Try any other available transcript
                            try:
                                available = list(transcript_list)
                                if available:
                                    first_transcript = available[0]
                                    transcript_data = first_transcript.fetch()
                                    transcript_text = " ".join([entry['text'] for entry in transcript_data])
                                    st.info(f"📝 Transcript available in {first_transcript.language}")
                                    st.text_area("Transcript", transcript_text, height=150, label_visibility="collapsed")
                                else:
                                    st.warning("⚠️ Transcript not accessible via API")
                                    st.info("💡 This video may have captions on YouTube, but they're not accessible through the API. Click 'Open in YouTube' to view with captions.")
                            except:
                                st.warning("⚠️ Transcript not accessible via API")
                                st.info("💡 This video may have captions on YouTube, but they're not accessible through the API. Click 'Open in YouTube' to view with captions.")
                except Exception as e:
                    st.warning("⚠️ Transcript not accessible via API")
                    st.info("💡 This video may have captions on YouTube, but they're not accessible through the API. Click 'Open in YouTube' to view with captions.")
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    else:
        st.warning("😕 No videos found. Try different keywords!")

elif search_button:
    st.warning("⚠️ Please enter a search query!")

else:
    # Show placeholder
    st.info("👆 Enter your search query above and click Search to find videos!")
    
    st.markdown("---")
    st.markdown("""
    ### ✨ How it works:
    1. **Type any topic** you want to learn about or watch
    2. **Click Search** - we'll search ALL of YouTube instantly  
    3. **Get top 5 videos** most relevant to your query
    4. **Watch directly** in the app or click to open in YouTube
    5. **View transcripts** if available (click the dropdown)
    
    ### 🎯 No limitations:
    - ✅ Search **any topic** on YouTube
    - ✅ Get **instant results** - no pre-downloading
    - ✅ Works with **ALL YouTube videos**, not just specific channels
    - ✅ Shows **embedded video players** for instant viewing
    - ✅ Displays **transcripts** when available
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            border-radius: 15px; margin-top: 30px;">
    <p style="color: white !important; margin: 0; font-size: 14px;">
        ⚡ Powered by YouTube Data API v3 • 🎯 Real-time Search • 🚀 Instant Results
    </p>
</div>
""", unsafe_allow_html=True)
