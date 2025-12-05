# YouTube Search App with Transcript Filter

A simple Streamlit web application that searches YouTube videos in real-time and filters results by English transcript availability.

## Features

- 🔍 **Real-time YouTube Search** - Search across ALL YouTube videos, not just one channel
- 📝 **Transcript Filter** - Option to show only videos with English transcripts
- 🎬 **Embedded Player** - Watch videos directly in the app
- 📊 **Auto & Manual Captions** - Detects both manual and auto-generated English transcripts
- 🎯 **Popular Topics** - Quick access buttons for TED, Khan Academy, Crash Course, and more

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up API Key**
   - Copy `.env.example` to `.env`
   - Add your YouTube Data API v3 key to `.env`:
     ```
     YOUTUBE_API_KEY=your_api_key_here
     ```

3. **Run the App**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Open in Browser**
   - The app will automatically open at `http://localhost:8501`

## Getting a YouTube API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the "YouTube Data API v3"
4. Create credentials (API key)
5. Copy the API key to your `.env` file

## Project Structure

```
INFOSYS/
├── streamlit_app.py              # Main Streamlit application
├── src/
│   └── milestone1/
│       └── search_youtube.py     # YouTube API search functionality
├── .env                          # Your API key (not in repo)
├── .env.example                  # Template for API key
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Popular Topics

The app includes quick search buttons for:
- TED Talks
- Khan Academy
- Crash Course
- Kurzgesagt
- freeCodeCamp
- National Geographic
- MIT OpenCourseWare
- Stanford Online

## Troubleshooting

**"No videos with English transcripts found"**
- Many videos have captions visible on YouTube but block API access
- Try different search terms or disable the transcript filter

**API Quota Exceeded**
- YouTube API has daily quota limits (10,000 units/day)
- Each search costs 100 units
- Wait 24 hours or create a new API key

**Module Not Found Error**
- Make sure you installed dependencies: `pip install -r requirements.txt`

## Technologies Used

- **Streamlit** - Web framework
- **YouTube Data API v3** - Video search
- **youtube-transcript-api** - Caption extraction

## License

MIT License - See LICENSE file for details
