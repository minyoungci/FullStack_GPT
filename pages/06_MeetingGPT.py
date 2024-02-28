import streamlit as st
import subprocess
import math
from pydub import AudioSegment
import glob
import os

# 현재 스크립트의 절대 경로를 기준으로 .cache 디렉토리 설정
base_dir = os.path.dirname(os.path.abspath(__file__))
cache_dir = os.path.join(base_dir, '.cache')
chunks_dir = os.path.join(cache_dir, 'chunks')

# .cache 및 chunks 디렉토리가 없으면 생성
os.makedirs(chunks_dir, exist_ok=True)

# 파일 존재 여부 확인
has_transcript = os.path.exists(os.path.join(cache_dir, "podcast.txt")) # transcript가 존재하는지 확인. 생성 비용이 비싸므로 있으면 다시 실행하지 않도록 !

@st.cache_data()
def transcribe_chunks(chunk_folder, destination):
    if has_transcript: #  생성 비용이 비싸므로 있으면 다시 실행하지 않도록 !
        return
    files = glob.glob(f"{chunk_folder}/*.mp3")
    files.sort()
    for file in files:
        with open(file, "rb") as audio_file, open(destination, "a") as text_file:
            # OpenAI API 호출 예시 (실제 사용 시 적절히 수정 필요)
            transcript = {"text": "sample transcript"}  # 예시 응답
            text_file.write(transcript["text"])

@st.cache_data()
def extract_audio_from_video(video_path):
    if has_transcript:
        return
    audio_path = video_path.replace("mp4", "mp3")
    command = [
        "ffmpeg",
        "-y",
        "-i",
        video_path,
        "-vn",
        audio_path,
    ]
    subprocess.run(command, check=True)

@st.cache_data()
def cut_audio_in_chunks(audio_path, chunk_size, chunks_folder):
    if has_transcript:
        return
    track = AudioSegment.from_mp3(audio_path)
    chunk_len = chunk_size * 60 * 1000  # milliseconds
    chunks = math.ceil(len(track) / chunk_len)
    for i in range(chunks):
        start_time = i * chunk_len
        end_time = (i + 1) * chunk_len
        chunk = track[start_time:end_time]
        chunk.export(
            os.path.join(chunks_folder, f"chunk_{i}.mp3"),
            format="mp3",
        )

st.set_page_config(page_title="MeetingGPT", page_icon="💼")

st.markdown("""
# MeetingGPT
            
Welcome to MeetingGPT, upload a video and I will give you a transcript, a summary and a chat bot to ask any questions about it.

Get started by uploading a video file in the sidebar.
""")

with st.sidebar:
    video = st.file_uploader("Video", type=["mp4", "avi", "mkv", "mov"])

if video:
    with st.status("Loading video..."):
        video_content = video.read()
        video_path = os.path.join(cache_dir, video.name)
        audio_path = video_path.replace(".mp4", ".mp3")
        transcript_path = video_path.replace(".mp4", ".txt")
        with open(video_path, "wb") as f:
            f.write(video_content)
    with st.status("Extracting audio..."):
        extract_audio_from_video(video_path)
    with st.status("Cutting audio segments..."):
        cut_audio_in_chunks(audio_path, 10, chunks_dir)
    with st.status("Transcribing audio..."):
        transcribe_chunks(chunks_dir, transcript_path)
