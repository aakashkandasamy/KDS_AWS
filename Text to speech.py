import boto3
import io
import pyaudio
from contextlib import closing
import os

os.environ['AWS_ACCESS_KEY_ID'] = 'AKIAQFHL5JQLK77ASDF3'
os.environ['AWS_SECRET_ACCESS_KEY'] = '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'

polly = boto3.client('polly', region_name='us-east-1')

text = "This testube has green liquid."
voice_id = 'Raveena'
output_format = 'pcm'
response = polly.synthesize_speech(Text=text, VoiceId=voice_id, OutputFormat=output_format)
audio_bytes = response['AudioStream'].read()
pa = pyaudio.PyAudio()

stream = pa.open(format=pyaudio.paInt16, channels=1, rate=15000, output=True)

with closing(stream):
    stream.write(audio_bytes)