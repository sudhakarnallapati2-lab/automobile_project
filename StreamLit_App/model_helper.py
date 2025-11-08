import streamlit as st
import requests
from PIL import Image

API_URL = "http://fastapi:10000/predict"  # docker-compose name

st.title("🚗 Car Damage Detection & Cost Estimation")

uploaded_file = st.file_uploader("Upload car image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Analyze Damage"):
        with st.spinner("Processing..."):
            files = {"file": uploaded_file.getvalue()}
            response = requests.post(API_URL, files={"file": ("image.jpg", uploaded_file.getvalue())})

        if response.status_code == 200:
            result = response.json()
            st.success(f"Damage Type: {result['damage']}")
            st.write(f"Confidence: ✅ {result['confidence']}")
            st.write(f"Estimated Cost: 💰 {result['estimated_cost']}")
        else:
            st.error("API Error")
            st.write(response.text)
