import streamlit as st

# Initialize session state for uploaded files
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "results" not in st.session_state:
    st.session_state.results = []

# Function to move to the next video
def next_video():
    if st.session_state.current_index < len(st.session_state.uploaded_files) - 1:
        st.session_state.current_index += 1

# Function to move to the previous video
def prev_video():
    if st.session_state.current_index > 0:
        st.session_state.current_index -= 1

def main():
    st.title("Video Scoring System Expert #1")

    # File uploader widget to allow uploading multiple video files
    new_uploaded_files = st.file_uploader("Upload videos", type=["mp4"], accept_multiple_files=True)
    if new_uploaded_files:
        st.session_state.uploaded_files.extend(new_uploaded_files)
    
    if not st.session_state.uploaded_files:
        st.warning("No videos uploaded. Please upload MP4 video files.")
        return

    # Current video index
    current_video = st.session_state.uploaded_files[st.session_state.current_index]

    # Display list of uploaded videos
    st.write("### List of Uploaded Videos")
    for i, file in enumerate(st.session_state.uploaded_files):
        if i == st.session_state.current_index:
            st.write(f"**➡️ {i + 1}. {file.name}**")  # Highlight the current video
        else:
            st.write(f"{i + 1}. {file.name}")

    # Display the current video
    st.write(f"### Now Playing: {current_video.name}")
    st.video(current_video)

    # Video rating controls
    st.write("### Rate the video")
    visual = st.selectbox(
        "Visual (1-5):",
        [5, 4, 3, 2, 1],  # 1 (low), 5 (high)
        key=f"visual_{current_video.name}"
    )
    
    audio = st.selectbox(
        "Audio (1-5):",
        [5, 4, 3, 2, 1],  # 1 (low), 5 (high)
        key=f"audio_{current_video.name}"
    )
    
    general_impression = st.selectbox(
        "General impression (1-5):",
        [5, 4, 3, 2, 1],  # 1 (low), 5 (high)
        key=f"general_{current_video.name}"
    )
    
    recommendation = st.selectbox(
        "Recommendation:",
        ["Forgetful", "Universal", "Heavy"],
        key=f"recommend_{current_video.name}"
    )
    
    comment = st.text_area(
        f"Short Comment for {current_video.name}:",
        placeholder="Write a brief comment about this video...",
        key=f"comment_{current_video.name}"
    )
    
    # Save button
    if st.button("Save Rating"):
        result = {
            "file_name": current_video.name,
            "visual": visual,
            "audio": audio,
            "general_impression": general_impression,
            "recommendation": recommendation,
            "comment": comment
        }
        st.session_state.results.append(result)
        st.success(f"Rating for {current_video.name} saved!")

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        st.button("Previous", on_click=prev_video, disabled=(st.session_state.current_index == 0))
    with col2:
        st.button("Next", on_click=next_video, disabled=(st.session_state.current_index == len(st.session_state.uploaded_files) - 1))

    # Download results
    if st.session_state.results:
        result_text = "Title: Video Scoring System Expert #1\n\n" + "\n".join(
            f"File: {r['file_name']}, "
            f"Visual: {r['visual']}, "
            f"Audio: {r['audio']}, "
            f"General: {r['general_impression']}, "
            f"Recommendation: {r['recommendation']}, "
            f"Comment: {r['comment']}"
            for r in st.session_state.results
        )
        st.download_button(
            "Download All Results",
            result_text,
            file_name="video_ratings.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()
