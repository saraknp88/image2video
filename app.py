import streamlit as st
import replicate
import requests
import tempfile
import os
from datetime import datetime
from PIL import Image
import io

# Configure Streamlit page
st.set_page_config(
    page_title="Image to Video Generator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with the complete beautiful UI design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Main App Background with animated gradient */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
        background-size: 400% 400%;
        animation: gradientShift 20s ease infinite;
        min-height: 100vh;
        position: relative;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        z-index: -1;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        color: #2d3436;
        line-height: 1.6;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        font-size: 2.8rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        margin-bottom: 0.5rem;
        position: relative;
    }
    
    .main-header h1::after {
        content: '';
        position: absolute;
        bottom: -8px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        border-radius: 2px;
    }
    
    .main-header p {
        font-size: 1.2rem;
        color: #2d3436;
        font-weight: 600;
        opacity: 0.8;
    }
    
    /* Card containers */
    .upload-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 24px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.1), 0 8px 32px rgba(118, 75, 162, 0.08);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1);
    }
    
    .upload-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        background-size: 200% 100%;
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    .upload-container:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 25px 80px rgba(102, 126, 234, 0.15), 0 12px 40px rgba(118, 75, 162, 0.12);
    }
    
    /* Section headers */
    h2, h3 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% 200%;
        animation: gradientMove 4s ease infinite;
        color: white !important;
        border: none;
        padding: 1.2rem 2rem;
        border-radius: 20px;
        font-size: 1.1rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.3);
        width: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:disabled {
        background: linear-gradient(135deg, #e0e7ff 0%, #f3e8ff 100%) !important;
        cursor: not-allowed;
        opacity: 0.6;
        transform: none;
        box-shadow: none;
        animation: none;
    }
    
    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Text inputs and textareas */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        border: 2px solid rgba(118, 75, 162, 0.2) !important;
        border-radius: 16px !important;
        background: rgba(255, 255, 255, 0.95) !important;
        color: #2d3436 !important;
        font-weight: 500;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.320, 1);
        box-shadow: 0 4px 20px rgba(118, 75, 162, 0.05);
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1), 0 8px 25px rgba(102, 126, 234, 0.15) !important;
        transform: translateY(-2px);
    }
    
    /* File uploader */
    .stFileUploader > div > div {
        background: rgba(255, 255, 255, 0.95);
        border: 3px dashed #764ba2;
        border-radius: 20px;
        padding: 2rem;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1);
        position: relative;
        overflow: hidden;
    }
    
    .stFileUploader > div > div:hover {
        border-color: #667eea;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        transform: scale(1.02);
        box-shadow: 0 10px 30px rgba(118, 75, 162, 0.2);
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        border-radius: 10px;
    }
    
    /* Status messages */
    .success-message {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
        border: 2px solid rgba(102, 126, 234, 0.4);
        border-radius: 12px;
        padding: 1.2rem;
        margin: 1rem 0;
        color: #2d3436;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.15);
    }
    
    .error-message {
        background: linear-gradient(135deg, rgba(245, 87, 108, 0.15) 0%, rgba(240, 147, 251, 0.15) 100%);
        border: 2px solid rgba(245, 87, 108, 0.4);
        border-radius: 12px;
        padding: 1.2rem;
        margin: 1rem 0;
        color: #2d3436;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 4px 20px rgba(245, 87, 108, 0.15);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #667eea 100%);
        background-size: 200% 200%;
        animation: gradientMove 4s ease infinite;
        color: white !important;
        border: none;
        padding: 1rem 2rem;
        border-radius: 16px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1);
        box-shadow: 0 8px 30px rgba(240, 147, 251, 0.3);
        width: 100%;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 12px 40px rgba(240, 147, 251, 0.4);
    }
    
    /* Video player */
    video {
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        max-width: 100%;
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
        animation: spin 1s linear infinite, colorShift 3s ease-in-out infinite;
    }
    
    @keyframes colorShift {
        0% { border-top-color: #667eea; }
        33% { border-top-color: #764ba2; }
        66% { border-top-color: #f093fb; }
        100% { border-top-color: #667eea; }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .upload-container {
            padding: 1rem;
            margin: 0.5rem 0;
        }
    }
</style>
""", unsafe_allow_html=True)

# App header
st.markdown("""
<div class="main-header">
    <h1>🎬 Image to Video Generator</h1>
    <p>Transform your images into animated videos with AI magic</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'video_generated' not in st.session_state:
    st.session_state.video_generated = False
if 'video_path' not in st.session_state:
    st.session_state.video_path = None
if 'processing' not in st.session_state:
    st.session_state.processing = False

# Configuration in sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    api_token = st.text_input(
        "Replicate API Token",
        type="password",
        help="Enter your Replicate API token",
        placeholder="r8_..."
    )
    
    st.markdown("---")
    st.markdown("### 📝 How to Use")
    st.markdown("""
    1. Enter your Replicate API token
    2. Upload an image
    3. Describe what should happen in the video
    4. Click 'Generate Video'
    5. Wait 2-5 minutes for processing
    6. Download your video!
    """)

def upload_to_postimage(image_file):
    """Upload image to PostImage and return the URL"""
    try:
        # Convert to bytes if it's a PIL image or file-like object
        if hasattr(image_file, 'read'):
            image_bytes = image_file.read()
            image_file.seek(0)  # Reset file pointer
        else:
            # Convert PIL image to bytes
            img_byte_arr = io.BytesIO()
            image_file.save(img_byte_arr, format='PNG')
            image_bytes = img_byte_arr.getvalue()
        
        # PostImage API endpoint
        url = "https://postimg.cc/json"
        
        # Prepare the file for upload
        files = {
            'upload': ('image.png', image_bytes, 'image/png')
        }
        
        # Upload to PostImage
        response = requests.post(url, files=files, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'OK':
                return result['url']
            else:
                st.error(f"PostImage upload failed: {result.get('error', 'Unknown error')}")
                return None
        else:
            st.error(f"Upload failed with status code: {response.status_code}")
            return None
            
    except Exception as e:
        st.error(f"Error uploading image: {str(e)}")
        return None

def generate_video(image_url, prompt, api_token):
    """Generate video using Replicate API"""
    try:
        # Initialize Replicate client
        client = replicate.Client(api_token=api_token)
        
        # Call the model
        output_url = client.run(
            "minimax/hailuo-02-fast",
            input={
                "prompt": prompt,
                "first_frame_image": image_url
            }
        )
        
        return output_url
        
    except Exception as e:
        st.error(f"Error generating video: {str(e)}")
        return None

def download_video(video_url):
    """Download video from URL and save locally"""
    try:
        response = requests.get(video_url, timeout=120)
        
        if response.status_code == 200:
            # Create a unique filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_video_{timestamp}.mp4"
            
            # Save the video
            with open(filename, "wb") as f:
                f.write(response.content)
            
            return filename, response.content
        else:
            st.error(f"Failed to download video: {response.status_code}")
            return None, None
            
    except Exception as e:
        st.error(f"Error downloading video: {str(e)}")
        return None, None

# Main interface
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="upload-container">', unsafe_allow_html=True)
    st.subheader("📤 Upload Your Image")
    
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['png', 'jpg', 'jpeg', 'gif'],
        help="Upload the image you want to animate"
    )
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="upload-container">', unsafe_allow_html=True)
    st.subheader("✍️ Describe Your Vision")
    
    prompt = st.text_area(
        "Enter your prompt:",
        value="an elephant turns blue and raises its trunk",
        height=150,
        help="Describe what should happen in the video",
        placeholder="Describe the changes you want to see in the video..."
    )
    
    # Generate button
    can_generate = (uploaded_file is not None and 
                   prompt.strip() and 
                   api_token.strip() and 
                   not st.session_state.processing)
    
    if st.button("🎬 Generate Video", disabled=not can_generate):
        if not api_token.strip():
            st.error("Please enter your Replicate API token in the sidebar!")
        elif not uploaded_file:
            st.error("Please upload an image!")
        elif not prompt.strip():
            st.error("Please enter a prompt!")
        else:
            st.session_state.processing = True
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Processing section
if st.session_state.processing and uploaded_file and prompt.strip() and api_token.strip():
    st.markdown("---")
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_container = st.container()
    
    with status_container:
        # Step 1: Upload image
        st.markdown('<div class="success-message">🔄 Step 1: Uploading image to PostImage...</div>', unsafe_allow_html=True)
        progress_bar.progress(20)
        
        image_url = upload_to_postimage(uploaded_file)
        
        if image_url:
            st.markdown('<div class="success-message">✅ Step 1 Complete: Image uploaded successfully!</div>', unsafe_allow_html=True)
            st.info(f"Image URL: {image_url}")
            progress_bar.progress(40)
            
            # Step 2: Generate video
            st.markdown('<div class="success-message">🔄 Step 2: Generating video... This may take 2-5 minutes.</div>', unsafe_allow_html=True)
            progress_bar.progress(60)
            
            video_url = generate_video(image_url, prompt, api_token)
            
            if video_url:
                st.markdown('<div class="success-message">✅ Step 2 Complete: Video generated successfully!</div>', unsafe_allow_html=True)
                progress_bar.progress(80)
                
                # Step 3: Download video
                st.markdown('<div class="success-message">🔄 Step 3: Downloading video...</div>', unsafe_allow_html=True)
                
                video_path, video_bytes = download_video(video_url)
                
                if video_path and video_bytes:
                    progress_bar.progress(100)
                    st.markdown('<div class="success-message">✅ All Steps Complete: Video ready!</div>', unsafe_allow_html=True)
                    
                    # Store in session state
                    st.session_state.video_generated = True
                    st.session_state.video_path = video_path
                    st.session_state.video_bytes = video_bytes
                    st.session_state.processing = False
                    
                    st.rerun()
                else:
                    st.session_state.processing = False
            else:
                st.session_state.processing = False
        else:
            st.session_state.processing = False

# Display video result
if st.session_state.video_generated and hasattr(st.session_state, 'video_bytes'):
    st.markdown("---")
    st.subheader("🎥 Your Generated Video")
    
    # Display video
    st.video(st.session_state.video_bytes)
    
    # Download button
    st.download_button(
        label="📥 Download Video",
        data=st.session_state.video_bytes,
        file_name=st.session_state.video_path,
        mime="video/mp4",
        use_container_width=True
    )
    
    # Success message
    st.success(f"🎉 Video generated successfully! File saved as: {st.session_state.video_path}")
    
    # Reset button
    if st.button("🔄 Generate Another Video"):
        st.session_state.video_generated = False
        st.session_state.video_path = None
        if hasattr(st.session_state, 'video_bytes'):
            delattr(st.session_state, 'video_bytes')
        st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #2d3436; font-weight: 600; padding: 1rem;'>
        🎬 Made with ❤️ using Streamlit and Replicate API
    </div>
    """,
    unsafe_allow_html=True
)
