import streamlit as st

st.set_page_config(page_title="Music Recommendation System")

st.title("🎵 Intelligent Music Recommendation System")

st.write("Welcome to my MCA Final Year Project")

name = st.text_input("Enter your name")

if st.button("Submit"):
    if name:
        st.success(f"Hello {name}! The system is running successfully 🚀")
    else:
        st.warning("Please enter your name")
