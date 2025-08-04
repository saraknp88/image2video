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

# Custom CSS to integrate with your beautiful UI
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
        background-size: 400% 400%;
        animation: gradientShift 20s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
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
    }
    
    .main-header p {
        font-size: 1.2rem;
        color: #2d3436;
        font-weight: 600;
        opacity: 0.8;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 20px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .upload-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.1);
        border-top: 4px solid;
        border-image: linear-gradient(90deg, #667eea, #764ba2, #f093fb) 1;
    }
    
    .stTextArea textarea {
        border: 2px solid rgba(118, 75, 162, 0.2);
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.95);
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
    }
    
    .success-message {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        color: #2d3436;
        font-weight: 600;
    }
    
    .error-message {
        background: linear-gradient(135deg, rgba(245, 87, 108, 0.1) 0%, rgba(240, 147, 251, 0.1) 100%);
        border: 2px solid rgba(245, 87, 108, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        color: #2d3436;
        font-weight: 600;
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
