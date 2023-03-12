import streamlit as st
import boto3
import io
from contextlib import closing
import os
from pydub import AudioSegment
from pydub.playback import play

os.environ['AWS_ACCESS_KEY_ID'] = 'AKIAQFHL5JQLK77ASDF3'
os.environ['AWS_SECRET_ACCESS_KEY'] = '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'



st.set_page_config(page_title='Image Uploader', page_icon=':camera:')

st.title('Image Uploader')

file = st.file_uploader('Choose an image file', type=['jpg', 'jpeg', 'png'])

if file is not None:
    st.image(file, caption='Uploaded Image')
    polly = boto3.client('polly', region_name='us-east-1')
    text = "Your file has been uploaded!"
    voice_id = 'Raveena'
    output_format = 'pcm'
    response = polly.synthesize_speech(Text=text, VoiceId=voice_id, OutputFormat=output_format)
    audio_bytes = response['AudioStream'].read()
    audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format='raw', sample_width=2, channels=1, frame_rate=16000)
    play(audio_segment)