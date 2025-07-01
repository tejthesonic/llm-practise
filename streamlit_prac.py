#this is to test and understand the stream lit
import streamlit as st

st.title("The Lexicon", width="content")
st.header("Story Writing Assistant", width="content")

text = st.text_input("Describe your story")
st.write(text)


st.sidebar.selectbox(
    "Category 1: Classification by Length (Word Count)",
    ("Flash Fiction", "Short Story", "Novelette", "Novella", "Novel", "Large Novel", "Epic")
)

st.sidebar.selectbox(
    "Category 2: Classification by Genre",
    ("Fantasy", "Science Fiction", "Adventure", "Mystery", "Thriller/Suspense", "Horror", "Romance", "Historical Fiction", "Literary Fiction")
)

st.sidebar.selectbox(
    "Category 3: Classification by Tone",
    ("Comedic", "Tragic", "Dramatic", "Satirical")
)

st.sidebar.selectbox(
    "Category 4: Classification by Target Audience",
    ("Children's", "Young Adult", "Adult")
)   

