from flask import Flask , render_template , request , send_file , jsonify
from google.cloud import texttospeech , speech , language_v1
import io
import os
import base64
import uuid
import json

app = Flask(__name__)

# Ensure the GOOGLE_APPLICATION_CREDENTIALS environment variable is set
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "brave-monitor-436720-p1-0bb03ab6d5ac.json"

# Initialize clients
tts_client = texttospeech.TextToSpeechClient()
speech_client = speech.SpeechClient()
language_client = language_v1.LanguageServiceClient()

# Create a directory to store results if it doesn't exist
RESULTS_DIR = "sentiment_results"
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)


def analyze_sentiment(text_content):
    document = language_v1.Document(content=text_content , type_=language_v1.Document.Type.PLAIN_TEXT)
    response = language_client.analyze_sentiment(request={'document': document})
    return response


def interpret_sentiment(score):
    if score > 0.25:
        return "Positive"
    elif score < -0.25:
        return "Negative"
    else:
        return "Neutral"


def save_result(text , sentiment , score , magnitude , audio_filename=None):
    result_id = str(uuid.uuid4())
    result = {
        "id": result_id ,
        "text": text ,
        "sentiment": sentiment ,
        "score": score ,
        "magnitude": magnitude ,
        "audio_filename": audio_filename
    }

    filename = os.path.join(RESULTS_DIR , f"{result_id}.json")
    with open(filename , 'w') as f:
        json.dump(result , f)

    return result_id


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze-text' , methods=['POST'])
def analyze_text():
    input_text = request.form['text']
    if not input_text:
        return jsonify({"error": "No text provided"}) , 400

    try:
        response = analyze_sentiment(input_text)
        sentiment = interpret_sentiment(response.document_sentiment.score)

        result_id = save_result(
            input_text ,
            sentiment ,
            response.document_sentiment.score ,
            response.document_sentiment.magnitude
        )

        return jsonify({
            "sentiment": sentiment ,
            "score": response.document_sentiment.score ,
            "magnitude": response.document_sentiment.magnitude ,
            "result_id": result_id
        })
    except Exception as e:
        return jsonify({"error": str(e)}) , 500


@app.route('/text-to-speech' , methods=['POST'])
def text_to_speech():
    input_text = request.form['text']
    if not input_text:
        return jsonify({"error": "No text provided"}) , 400

    try:
        synthesis_input = texttospeech.SynthesisInput(text=input_text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US" ,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

        response = tts_client.synthesize_speech(
            input=synthesis_input , voice=voice , audio_config=audio_config
        )

        # Convert audio content to base64
        audio_base64 = base64.b64encode(response.audio_content).decode('utf-8')
        return jsonify({"audio": audio_base64})
    except Exception as e:
        return jsonify({"error": str(e)}) , 500


@app.route('/speech-to-text' , methods=['POST'])
def speech_to_text():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}) , 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}) , 400

    try:
        audio_content = file.read()
        audio = speech.RecognitionAudio(content=audio_content)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS ,
            sample_rate_hertz=48000 ,
            language_code="en-US"
        )

        response = speech_client.recognize(config=config , audio=audio)

        if response.results:
            transcript = response.results[0].alternatives[0].transcript

            # Save the audio file
            audio_filename = f"{str(uuid.uuid4())}.webm"
            with open(os.path.join(RESULTS_DIR , audio_filename) , 'wb') as f:
                f.write(audio_content)

            return jsonify({
                "transcript": transcript ,
                "audio_filename": audio_filename
            })
        else:
            return jsonify({"error": "No speech detected"}) , 400
    except Exception as e:
        return jsonify({"error": str(e)}) , 500


@app.route('/analyze-speech' , methods=['POST'])
def analyze_speech():
    transcript = request.json.get('transcript')
    audio_filename = request.json.get('audio_filename')
    if not transcript:
        return jsonify({"error": "No transcript provided"}) , 400

    try:
        sentiment_response = analyze_sentiment(transcript)
        sentiment = interpret_sentiment(sentiment_response.document_sentiment.score)

        result_id = save_result(
            transcript ,
            sentiment ,
            sentiment_response.document_sentiment.score ,
            sentiment_response.document_sentiment.magnitude ,
            audio_filename
        )

        return jsonify({
            "sentiment": sentiment ,
            "score": sentiment_response.document_sentiment.score ,
            "magnitude": sentiment_response.document_sentiment.magnitude ,
            "result_id": result_id
        })
    except Exception as e:
        return jsonify({"error": str(e)}) , 500


@app.route('/get-result/<result_id>' , methods=['GET'])
def get_result(result_id):
    try:
        with open(os.path.join(RESULTS_DIR , f"{result_id}.json") , 'r') as f:
            result = json.load(f)
        return jsonify(result)
    except FileNotFoundError:
        return jsonify({"error": "Result not found"}) , 404
    except Exception as e:
        return jsonify({"error": str(e)}) , 500


if __name__ == '__main__':
    app.run(debug=True)