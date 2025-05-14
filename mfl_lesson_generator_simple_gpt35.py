
import streamlit as st
from openai import OpenAI

# Load API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="MFL Lesson Generator", layout="wide")
st.title("Modern Foreign Languages (MFL) Lesson Generator")

# Sidebar for user inputs
st.sidebar.header("Lesson Settings")
language = st.sidebar.selectbox("Language", ["Spanish", "French", "German"])
year = st.sidebar.selectbox("Year Group", ["7", "8", "9", "10", "11"])
exam_board = st.sidebar.selectbox("Exam Board", ["AQA", "Edexcel", "OCR"])
topic = st.sidebar.text_input("Topic (e.g., Mi casa)", "")
theme = st.sidebar.multiselect("Thematic Focus", ["Vocabulary", "Grammar", "Listening", "Reading", "Writing", "Speaking"])
generate_button = st.sidebar.button("Generate Lesson Pack")

if generate_button and topic and theme:
    with st.spinner("Generating your lesson..."):
        prompt = f"""
        Create a [Full lesson pack] for [{language}], aimed at Year {year} students following the [{exam_board}] curriculum.
        Topic: [{topic}]
        Thematic Focus: [{", ".join(theme)}]
        Please include scaffolded tasks for mixed-ability learners, challenge options, visuals, and interactive elements.
        Make the presentation more complex and age-appropriate for the year group, including an animated vocabulary section, 
        a multi-step starter, and task differentiation. 
        """
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert secondary MFL teacher creating interactive lesson content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        lesson_output = response.choices[0].message.content
        st.subheader("Generated Lesson Content")
        st.markdown(lesson_output)
else:
    st.info("Enter topic and select a focus area, then click 'Generate Lesson Pack'.")
