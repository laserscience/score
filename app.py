import streamlit as st

def main():
    st.title("Video Scoring System Expert #1")

    # File uploader widget to allow uploading multiple video files
    uploaded_files = st.file_uploader("Upload videos", type=["mp4"], accept_multiple_files=True)

    # Process and display uploaded videos
    if uploaded_files:
        st.write(f"Uploaded {len(uploaded_files)} videos.")
        
        # Iterate through each uploaded video
        for uploaded_file in uploaded_files:
            st.write(f"### Video: {uploaded_file.name}")
            
            # Display the video with a reduced size (scaled down by 3 times)
            st.video(uploaded_file, format="video/mp4", start_time=0)
            
            # Allow user to score the video
            st.write("### Rate the video")
            visual = st.selectbox(
                "Visual (1-5):",
                [5, 4, 3, 2, 1],  # 1 (low), 5 (high)
                key=f"visual_{uploaded_file.name}"
            )
            
            audio = st.selectbox(
                "Audio (1-5):",
                [5, 4, 3, 2, 1],  # 1 (low), 5 (high)
                key=f"audio_{uploaded_file.name}"
            )
            
            general_impression = st.selectbox(
                "General impression (1-5):",
                [5, 4, 3, 2, 1],  # 1 (low), 5 (high)
                key=f"general_{uploaded_file.name}"
            )
            
            recommendation = st.selectbox(
                "Recommendation:",
                ["Forgetful", "Universal", "Heavy"],
                key=f"recommend_{uploaded_file.name}"
            )
            
            comment = st.text_area(
                f"Short Comment for {uploaded_file.name}:",
                placeholder="Write a brief comment about this video...",
                key=f"comment_{uploaded_file.name}"
            )
            
            # Save the result for each video
            if st.button(f"Save Rating for {uploaded_file.name}", key=f"save_{uploaded_file.name}"):
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
    
    # Initialize results storage in session state
    if "results" not in st.session_state:
        st.session_state.results = []

    # Generate and download results
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
