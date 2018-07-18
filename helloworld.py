from flask import Flask, render_template, request, redirect, url_for
from opentok import OpenTok, MediaModes, OutputModes
from email.utils import formatdate
import os, time

try:
    api_key = os.environ['API_KEY']
    api_secret = os.environ['API_SECRET']
except Exception:
    raise Exception('You must define API_KEY and API_SECRET environment variables')

app = Flask(__name__)
opentok = OpenTok(api_key, api_secret)

session = opentok.create_session(media_mode=MediaModes.routed)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/host')
def host():
	key = api_key
	session_id = session.session_id
	token = opentok.generate_token(session_id)

	return render_template('host.html', api_key=key, session_id=session_id, token=token)


@app.route('/start', methods=['POST'])
def start():
	has_audio = 'hasAudio' in request.form.keys()
	has_video = 'hasVideo' in request.form.keys()
	output_mode = OutputModes[request.form.get('outputMode')]
	archive = opentok.start_archive(session.session_id, name="Python Archiving Sample App",
									has_audio=has_audio, has_video=has_video, output_mode=output_mode)
	return archive.json()

@app.route('participant')
def participant()
	key = api_key
	session_id = session.session_id
	token = opentok.generate_token(session_id)

	return render_template('participant.html', api_key=key, session_id=session_id, token=token)



if __name__=='__main__':
	app.debug = True
	app.run()