import os
import shutil
import openai
from dotenv import load_dotenv
from pytube import YouTube
from flask import Flask, render_template, request, redirect, url_for
import aspose.slides as slides
# from whisper import convert_link_to_audio

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# os.remove(newfile)


def ppt_to_pdf(ppt_name, pdf_name):
    # Load presentation
    pres = slides.Presentation(ppt_name)

    # Convert PPTX to PDF
    pres.save(pdf_name, slides.export.SaveFormat.PDF)


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         input_text = request.form['input_text']
#         store_input(input_text)
#         output = convert_link_to_audio(input_text.strip())
#         print(output)
#         return redirect(url_for('index'))

#     return render_template('index.html')

# Endpoints

@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        return {'message': 'Welcome to QuizForge API'}
    if request.method == 'POST':
        request_data = request.get_json()
        text = request_data['text']
        return {'message': f'Welcome to QuizForge API and here\'s your text: {text}'}


@app.route('/clear', methods=['GET'])
def clear_cache(folder=None):
    if request.method == 'GET':
        if folder is None:
            folder = request.args.get('folder')
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        return {'message': f'{folder} cleared'}


@app.route('/transcribe', methods=['GET'])
def convert_link_to_audio():
    if request.method == 'GET':
        url = request.args.get('url')
        yt = YouTube(url)
        # Downloads the audiofile as mp4
        audio_file = yt.streams.filter(only_audio=True).first()
        audio_file.download(output_path='cache/', filename='audio.mp4')

        og_file = "cache/audio.mp4"
        newfile = og_file.replace('.mp4', '.mp3')

        try:
            os.rename(og_file, newfile)
        except FileExistsError:
            print(f"{newfile} already exists. Using the existing file.")

        # audio_file = open(newfile, "rb")
        # transcript = openai.Audio.transcribe("whisper-1", audio_file)
        # return transcript
        return {'message': 'Success'}


if __name__ == '__main__':
    app.run(debug=True, port=8000)
