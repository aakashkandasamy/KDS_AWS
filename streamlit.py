import streamlit as st
import tensorflow as tf
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np
import boto3
import io
import pyaudio
from contextlib import closing
import os

@st.cache(allow_output_mutation=True)
def load_model():
    h5_loaded_model = tf.keras.models.load_model('best_model.h5')
    return h5_loaded_model

@st.cache(allow_output_mutation=True)
def load_model_prop():
    h5_loaded_model_prop = tf.keras.models.load_model('best_model_glass_props.h5')
    return h5_loaded_model_prop



list_y = [[], ['Filled'], ['Foam'], ['Foam', 'Filled'], 
['Foam', 'Solid', 'Filled'], 
['Foam', 'Solid', 'Granular', 'Powder', 'Filled'], 
['Foam', 'Solid', 'Powder'], ['Foam', 'Solid', 'Powder', 'Filled'], 
['Liquid'], ['Liquid', 'Filled'], ['Liquid', 'Filled', 'Solid'], 
['Liquid', 'Foam', 'Filled'], 
['Liquid', 'Foam', 'Gel', 'Solid', 'Filled'], 
['Liquid', 'Foam', 'Solid', 'Filled'], 
['Liquid', 'Foam', 'Solid', 'Granular', 'Filled'], 
['Liquid', 'Foam', 'Solid', 'Powder', 'Filled'], ['Liquid', 'Foam', 'Vapor'], 
['Liquid', 'Gel', 'Filled'], ['Liquid', 'Gel', 'Solid'], 
['Liquid', 'Gel', 'Solid', 'Filled'], 
['Liquid', 'Gel', 'Solid', 'SolidLargChunk', 'Filled'], 
['Liquid', 'Granular', 'Filled'], ['Liquid', 'Solid'], 
['Liquid', 'Solid', 'Filled'], 
['Liquid', 'Solid', 'Granular', 'Filled'], 
['Liquid', 'Solid', 'Other Material', 'Filled'], 
['Liquid', 'Solid', 'Powder', 'Filled'], 
['Liquid', 'Solid', 'SolidLargChunk', 'Filled'], ['Liquid', 'Suspension'], 
['Liquid', 'Suspension', 'Filled'], 
['Liquid', 'Suspension', 'Foam', 'Filled'], 
['Liquid', 'Suspension', 'Foam', 'Gel', 'Filled'], 
['Liquid', 'Suspension', 'Foam', 'Solid', 'Filled'], 
['Liquid', 'Suspension', 'Foam', 'Solid', 'Powder', 'Filled'], 
['Liquid', 'Suspension', 'Gel', 'Filled'], 
['Liquid', 'Suspension', 'Gel', 'Solid', 'Filled'], 
['Liquid', 'Suspension', 'Gel', 'Solid', 'Powder'], 
['Liquid', 'Suspension', 'Gel', 'Solid', 'Powder', 'Filled'], 
['Liquid', 'Suspension', 'Solid'], ['Liquid', 'Suspension', 'Solid', 'Filled'], 
['Liquid', 'Suspension', 'Solid', 'Granular', 'Filled'], 
['Liquid', 'Suspension', 'Solid', 'Granular', 'Powder', 'Filled'], 
['Liquid', 'Suspension', 'Solid', 'Powder'], 
['Liquid', 'Suspension', 'Solid', 'Powder', 'Filled'], 
['Liquid', 'Suspension', 'Solid', 'Powder', 'Other Material', 'Filled'], 
['Liquid', 'Suspension', 'Solid', 'Powder', 'SolidLargChunk', 'Filled'], 
['Liquid', 'Suspension', 'Solid', 'SolidLargChunk', 'Filled'], 
['Liquid', 'Suspension', 'Vapor'], ['Liquid', 'Vapor'], 
['Solid'], ['Solid', 'Filled'], ['Solid', 'Granular'], 
['Solid', 'Granular', 'Filled'], 
['Solid', 'Granular', 'Powder', 'Filled'], 
['Solid', 'Granular', 'SolidLargChunk', 'Filled'], 
['Solid', 'Other Material', 'Filled'], ['Solid', 'Powder'], 
['Solid', 'Powder', 'Filled'],
['Solid', 'Powder', 'SolidLargChunk', 'Filled'],
['Solid', 'SolidLargChunk', 'Filled'], 
['Solid', 'SolidLargChunk', 'Filled'],
['Solid', 'SolidLargChunk', 'Other Material', 'Filled'],
['Vapor']]

list_y_prop = [[], ['Opaque'], ['SemiTrans'],['SemiTrans', 'Opaque'] ,['Transparent'] ,['Transparent', 'DisturbeView'],['VesselInsideVessel', 'Opaque'],['VesselInsideVessel', 'SemiTrans'],['VesselInsideVessel', 'Transparent']]

def predictions(uploaded_file, h5_loaded_model, h5_loaded_model_prop):
    pred = np.nan
    pred_prop = np.nan
    st.image(uploaded_file, caption='Uploaded Image')
    img = tf.keras.preprocessing.image.load_img(uploaded_file, target_size=(224, 224))
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = img / 255.0
    img = img.reshape(1, 224, 224, 3)

    pred = h5_loaded_model.predict(img)
    pred = (pred > 0.2).astype(int)
    mlb = MultiLabelBinarizer()
    mlb.fit(list_y)

    pred_prop = h5_loaded_model_prop.predict(img)
    # print(pred_prop)
    # st.write(pred_prop)
    pred_prop = (pred_prop > 0.3).astype(int)
    mlb_prop = MultiLabelBinarizer()
    mlb_prop.fit(list_y_prop)

    text_labels = mlb.inverse_transform(pred) 
    text_labels_prop = mlb_prop.inverse_transform(pred_prop)
    if len(text_labels[0]) == 0 and len(text_labels_prop[0]) == 0:
        st.write('No labels found')
    for label in text_labels[0]:
        st.write(f'- {label}')
    for label in text_labels_prop[0]:
        st.write(f'- {label}')

    polly = boto3.client('polly', region_name='us-east-1')
    text = "Your file has been uploaded!"
    voice_id = 'Raveena'
    output_format = 'pcm'
    response = polly.synthesize_speech(Text=text, VoiceId=voice_id, OutputFormat=output_format)
    audio_bytes = response['AudioStream'].read()
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, output=True)
    with closing(stream):
        stream.write(audio_bytes)

def main():
    st.set_page_config(page_title='Image Uploader', page_icon=':camera:')

    st.title('Image Uploader')

    uploaded_file = st.file_uploader('Choose an image file', type=['jpg', 'jpeg', 'png'])
    h5_loaded_model =  load_model()
    h5_loaded_model_prop = load_model_prop()
    # load_model()

    if h5_loaded_model and h5_loaded_model_prop and uploaded_file is not None:
        predictions(uploaded_file, h5_loaded_model, h5_loaded_model_prop)
        

if __name__ == '__main__':
    main()