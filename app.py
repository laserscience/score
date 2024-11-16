import os
import streamlit as st

# Initialize session state for video navigation
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "results" not in st.session_state:
    st.session_state.results = []

# Function to fetch video files from a folder
def get_video_files(folder_path="videos"):
    try:
        # Ensure folder exists
        if not os.path.exists(folder_path):
            st.error(f"Folder '{folder_path}' does not exist.")
            return []
        # Get all MP4 files
        return [f for f in os.listdir(folder_path) if f.endswith(".mp4")]
    except Exception as e:
        st.error(f"Error reading folder: {str(e)}")
        return []

# Function to move to the next video
def next_video():
    if st.session_state.current_index < len(st.session_state.video_files) - 1:
        st.session_state.current_index += 1

# Function to move to the previous video
def prev_video():
    if st.session_state.current_index > 0:
        st.session_state.current_index -= 1

def main():
    st.title("Video Scoring System Expert #1")

    # Load video files
    video_folder = "videos"  # Path to your video folder
    st.session_state.video_files = get_video_files(video_folder)

    if not st.session_state.video_files:
        st.warning("No videos found in the folder.")
        return

    # Display list of videos
    st.write("### List of Videos")
    for i, file in enumerate(st.session_state.video_files):
        if i == st.session_state.current_index:
            st.write(f"**➡️ {i + 1}. {file}**")  # Highlight the current video
        else:
            st.write(f"{i + 1}. {file}")

    # Get the current video file
    current_video = st.session_state.video_files[st.session_state.current_index]
    current_video_path = os.path.join(video_folder, current_video)

    # Display the current video
    st.write(f"### Now Playing: {current_video}")
    st.video(current_video_path)

    # Video rating controls
    st.write("### Rate the video")
    visual = st.selectbox(
        "Visual (1-5):",
        [5, 4, 3, 2, 1],  # 1 (low), 5 (high)
        key=f"visual_{current_video}"
    )
    
    audio = st.selectbox(
        "Audio (1-5):",
        [5, 4, 3, 2, 1],  # 1 (low), 5 (high)
        key=f"audio_{current_video}"
    )
    
    general_impression = st.selectbox(
        "General impression (1-5):",
        [5, 4, 3, 2, 1],  # 1 (low), 5 (high)
        key=f"general_{current_video}"
    )
    
    recommendation = st.selectbox(
        "Recommendation:",
        ["Forgetful", "Universal", "Heavy"],
        key=f"recommend_{current_video}"
    )
    
    comment = st.text_area(
        f"Short Comment for {current_video}:",
        placeholder="Write a brief comment about this video...",
        key=f"comment_{current_video}"
    )
    
    # Save button
    if st.button("Save Rating"):
        result = {
            "file_name": current_video,
            "visual": visual,
            "audio": audio,
            "general_impression": general_impression,
            "recommendation": recommendation,
            "comment": comment
        }
        st.session_state.results.append(result)
        st.success(f"Rating for {current_video} saved!")

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        st.button("Previous", on_click=prev_video, disabled=(st.session_state.current_index == 0))
    with col2:
        st.button("Next", on_click=next_video, disabled=(st.session_state.current_index == len(st.session_state.video_files) - 1))

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
