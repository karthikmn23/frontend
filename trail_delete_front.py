import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import base64

# Placeholder for your actual Flask API endpoint URL
API_URL = "http://localhost:8888/process_request"

st.title("Database Chatbot")
st.write("Ask questions related to the database content.")

user_query = st.text_input("Enter your query:")

if user_query:
    def call_backend_api(query):
        try:
            headers = {"Content-Type": "application/json"}
            data = {"user_query": query, "request_id": "123"}
            response = requests.post(API_URL, headers=headers, json=data)
            response.raise_for_status()  # Raise exception for non-2xx status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred while communicating with the backend: {e}")
            return None

    response = call_backend_api(user_query)

    if response:
        st.write(f"Response: {response['answer']}")

        # Display the plot image
        if 'base64_img' in response and response['base64_img']:
            try:
                image_data = base64.b64decode(response['base64_img'])
                image = Image.open(BytesIO(image_data))
                st.image(image, caption='Generated Plot', use_column_width=True)
            except Exception as e:
                st.error(f"An error occurred while displaying the image: {e}")
        else:
            st.warning("No plot image received from the backend.")
    else:
        st.warning("No response received from the backend.")
