import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
genai.configure(api_key=os.getenv("API_KEY"))

def generateContent(transcriptText, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    res = model.generate_content(prompt + transcriptText) 
    return res.text

def extractTranscript(youtubeLink):
    try:
        videoID = youtubeLink.split("=")[-1]
        transcriptText = YouTubeTranscriptApi.get_transcript(videoID)
        transcript = ""
        for i in transcriptText:
            transcript += " " + i["text"]
        return transcript
    except Exception as e:
        raise e

prompt = """You are an expert YouTube video summarizer with a strong focus on clarity and brevity. 
Your task is to thoroughly analyze the provided transcript and distill the content into a well-organized, 
concise summary that captures the core message, key ideas, and essential points from the video. 
Your summary should be structured in bullet points for clarity, 
and each point should succinctly convey the most important aspects of the video's content.

Guidelines:

Conciseness: The summary should not exceed 250 words. Aim for brevity without compromising the clarity of the main ideas.
Key Information: Focus on the most relevant and significant details, including the main topic, major arguments or insights, and any critical data or conclusions.
Coherence: Ensure that the summary flows logically, with each point building on the previous one where applicable.
Tone and Style: Maintain a neutral, informative tone. Avoid subjective opinions or unnecessary elaboration.
Readability: The summary should be easily digestible for someone who hasn’t watched the video, so it should include only the most essential information.
The transcript text is as follows:
"""
st.title("Youtube video summarizer")
youtubeLink = st.text_input("Enter the youtube link: ")
if st.button("Get the summary"):
    transcriptText = extractTranscript(youtubeLink)
    if transcriptText:
        summary = generateContent(transcriptText, prompt)
        st.markdown("## Summary:")
        st.write(summary)


