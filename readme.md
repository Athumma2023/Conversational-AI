# Sentiment Analysis Application

## Overview

This web application performs sentiment analysis on text and speech inputs using Google Cloud AI services. It provides an intuitive interface for users to analyze sentiment in written text or spoken words.

## Features

- Text-based sentiment analysis
- Speech-to-text conversion and sentiment analysis
- Text-to-speech conversion
- Storage and retrieval of analysis results

## Technologies Used

- Frontend: HTML5, CSS3, JavaScript (with jQuery)
- Backend: Python with Flask framework
- APIs: Google Cloud Natural Language, Speech-to-Text, and Text-to-Speech

## Prerequisites

- Python 3.7+
- Flask
- Google Cloud account with enabled APIs (Natural Language, Speech-to-Text, Text-to-Speech)
- Google Cloud credentials JSON file

## Setup

1. Clone the repository:
   ```
   git clone [repository-url]
   cd sentiment-analysis-app
   ```

2. Install required Python packages:
   ```
   pip install flask google-cloud-language google-cloud-speech google-cloud-texttospeech
   ```

3. Set up Google Cloud credentials:
   - Place your Google Cloud credentials JSON file in the project directory
   - Set the environment variable:
     ```
     export GOOGLE_APPLICATION_CREDENTIALS="path/to/your-credentials.json"
     ```

4. Create a directory for storing results:
   ```
   mkdir sentiment_results
   ```

## Running the Application

1. Start the Flask server:
   ```
   python app.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`

## Usage

### Text Analysis
1. Enter text in the provided textarea
2. Click "Analyze Text"
3. View the sentiment analysis results

### Speech Analysis
1. Click "Start Recording" and speak
2. Click "Stop Recording" when finished
3. Click "Analyze Speech"
4. View the transcription and sentiment analysis results

### Text-to-Speech
1. Enter text in the textarea
2. Click "Convert to Speech"
3. Listen to the generated audio

### Retrieving Past Results
1. Enter a previously obtained result ID
2. Click "Retrieve Result"
3. View the retrieved analysis

## File Structure

- `app.py`: Flask application (backend)
- `templates/index.html`: Main HTML file (frontend)
- `sentiment_results/`: Directory for storing analysis results

## Notes

- Ensure your Google Cloud account has sufficient quota for API calls
- Large audio files may take longer to process
- The application stores results as JSON files in the `sentiment_results` directory

## Security Considerations

- API credentials are stored as environment variables
- Audio data is processed in-memory and not persistently stored
- Only analysis results are saved, not raw audio files

## Future Improvements

- User authentication
- Support for multiple languages
- Advanced visualization of sentiment trends
- Batch processing capability



