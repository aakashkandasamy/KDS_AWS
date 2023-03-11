import streamlit as st

st.set_page_config(page_title='Image Uploader', page_icon=':camera:')

st.title('Image Uploader')

file = st.file_uploader('Choose an image file', type=['jpg', 'jpeg', 'png'])

if file is not None:
    st.image(file, caption='Uploaded Image')
