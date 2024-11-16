import streamlit as st

# Initialize session state for uploaded files
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "results" not in st.session_state:
    st.session_state.results = []

# Function to add new files only once
def add_uploaded_files(new_files):
    existing_files = {file.name for file in st.session_state.uploaded_files}
    for file in new_files:
        if file.name not in existing_files:
            st.session_state.uploaded_files.append(file)

# Function to display a single video
def display_video(file, width=320, height=240):
    st.video(file, format="video/mp4", start_time=0)

def main():
    st.title("Video Scoring System Expert #1")

    # File uploader widget to allow uploading multiple video files
    new_uploaded_files = st.file_uploader("Upload videos", type=["mp4"], accept_multiple_files=True)
    if new_uploaded_files:
        add_uploaded_files(new_uploaded_files)

    if not st.session_state.uploaded_files:
        st.warning("No videos uploaded. Please upload MP4 video files.")
        return

    # Display all uploaded videos with ratings
    for i, uploaded_file in enumerate(st.session_state.uploaded_files):
        st.write(f"### Video {i + 1}: {uploaded_file.name}")
        display_video(uploaded_file, width=320, height=240)

        # Rating controls for each video
        visual = st.selectbox(
            f"Visual (1-5) for {uploaded_file.name}:",
            [5, 4, 3, 2, 1],  # 1 (low), 5 (high)
            key=f"visual_{uploaded_file.name}"
        )
        
        audio = st.selectbox(
            f"Audio (1-5) for {uploaded_file.name}:",
            [5, 4, 3, 2, 1],  # 1 (low), 5 (high)
            key=f"audio_{uploaded_file.name}"
        )
        
        general_impression = st.selectbox(
            f"General impression (1-5) for {uploaded_file.name}:",
            [5, 4, 3, 2, 1],  # 1 (low), 5 (high)
            key=f"general_{uploaded_file.name}"
        )
        
        recommendation = st.selectbox(
            f"Recommendation for {uploaded_file.name}:",
            ["Forgetful", "Universal", "Heavy"],
            key=f"recommend_{uploaded_file.name}"
        )
        
        comment = st.text_area(
            f"Short Comment for {uploaded_file.name}:",
            placeholder="Write a brief comment about this video...",
            key=f"comment_{uploaded_file.name}"
        )

        # Save rating for each video
        if st.button(f"Save Rating for {uploaded_file.name}"):
            result = {
                "file_name": uploaded_file.name,
                "visual": visual,
                "audio": audio,
                "general_impression": general_impression,
                "recommendation": recommendation,
                "comment": comment
            }
            st.session_state.results.append(result)
            st.success(f"Rating for {uploaded_file.name} saved!")

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
