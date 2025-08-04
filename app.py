import streamlit as st
import replicate
import requests
import tempfile
import os
from datetime import datetime
from PIL import Image
import io

# Initialize clients and API keys
client = replicate.Client(api_token=st.secrets["REPLICATE_API_TOKEN"])
imgbb_key = st.secrets["IMGBB_API_KEY"]

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
    
    /* Main App Background - Clean white with subtle gradient */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 50%, #f1f5f9 100%);
        min-height: 100vh;
        position: relative;
    }
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        color: #1e293b;
        line-height: 1.7;
        max-width: 1200px;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        font-size: 2.8rem;
        background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 50%, #f59e0b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        margin-bottom: 0.5rem;
        position: relative;
        letter-spacing: -0.02em;
    }
    
    .main-header h1::after {
        content: '';
        position: absolute;
        bottom: -8px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 4px;
        background: linear-gradient(90deg, #8b5cf6, #a855f7, #f59e0b);
        border-radius: 2px;
    }
    
    .main-header p {
        font-size: 1.2rem;
        color: #475569;
        font-weight: 500;
        opacity: 0.9;
        line-height: 1.6;
    }
    
    /* Card containers */
    .upload-container {
        background: transparent;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: none;
        border: none;
        position: relative;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.320, 1);
    }
    
    .upload-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #8b5cf6, #a855f7, #f59e0b);
        background-size: 200% 100%;
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    .upload-container:hover {
        transform: translateY(-4px);
        box-shadow: none;
    }
    
    /* Section headers */
    h2, h3 {
        background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        margin-bottom: 0.5rem;
        margin-top: 0.5rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 50%, #f59e0b 100%);
        background-size: 200% 200%;
        animation: gradientMove 4s ease infinite;
        color: white !important;
        border: none;
        padding: 1rem 2rem;
        border-radius: 16px;
        font-size: 1rem;
        font-weight: 600;
        text-transform: none;
        letter-spacing: 0.5px;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.320, 1);
        box-shadow: 0 4px 20px rgba(139, 92, 246, 0.25);
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
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 30px rgba(139, 92, 246, 0.35);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:disabled {
        background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%) !important;
        cursor: not-allowed;
        opacity: 0.6;
        transform: none;
        box-shadow: none;
        animation: none;
        color: #64748b !important;
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
        border: 2px solid rgba(139, 92, 246, 0.2) !important;
        border-radius: 12px !important;
        background: #ffffff !important;
        color: #1e293b !important;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.320, 1);
        box-shadow: 0 2px 8px rgba(139, 92, 246, 0.05);
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1), 0 4px 16px rgba(139, 92, 246, 0.1) !important;
        transform: translateY(-1px);
    }
    
    /* File uploader */
    .stFileUploader > div > div {
        background: #ffffff;
        border: 2px dashed #8b5cf6;
        border-radius: 16px;
        padding: 2rem;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.320, 1);
        position: relative;
        overflow: hidden;
    }
    
    .stFileUploader > div > div:hover {
        border-color: #a855f7;
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.05) 0%, rgba(168, 85, 247, 0.05) 100%);
        transform: scale(1.01);
        box-shadow: 0 4px 20px rgba(139, 92, 246, 0.15);
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #8b5cf6, #a855f7, #f59e0b);
        border-radius: 12px;
        height: 12px;
        box-shadow: 0 2px 8px rgba(139, 92, 246, 0.2);
    }
    
    .stProgress > div {
        background: rgba(139, 92, 246, 0.1);
        border-radius: 12px;
        height: 12px;
        margin: 1rem 0;
    }
    
    /* Status messages */
    .success-message {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.08) 0%, rgba(168, 85, 247, 0.08) 100%);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        color: #1e293b;
        font-weight: 500;
        font-size: 0.95rem;
        box-shadow: 0 2px 8px rgba(139, 92, 246, 0.08);
    }
    
    .error-message {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.08) 0%, rgba(248, 113, 113, 0.08) 100%);
        border: 1px solid rgba(239, 68, 68, 0.2);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        color: #1e293b;
        font-weight: 500;
        font-size: 0.95rem;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.08);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: #ffffff;
        border-right: 1px solid rgba(139, 92, 246, 0.1);
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #f59e0b 0%, #f97316 50%, #8b5cf6 100%);
        background-size: 200% 200%;
        animation: gradientMove 4s ease infinite;
        color: white !important;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        text-transform: none;
        letter-spacing: 0.5px;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.320, 1);
        box-shadow: 0 4px 20px rgba(245, 158, 11, 0.25);
        width: 100%;
        font-size: 0.9rem;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 30px rgba(245, 158, 11, 0.35);
    }
    
    /* Share button */
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 50%, #f59e0b 100%);
        background-size: 200% 200%;
        animation: gradientMove 4s ease infinite;
        color: white !important;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        text-transform: none;
        letter-spacing: 0.5px;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.320, 1);
        box-shadow: 0 4px 20px rgba(139, 92, 246, 0.25);
        width: 100%;
        font-size: 0.9rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 30px rgba(139, 92, 246, 0.35);
    }
    
    /* Video player */
    video {
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        max-width: 100%;
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-top-color: #8b5cf6 !important;
        animation: spin 1s linear infinite, colorShift 3s ease-in-out infinite;
    }
    
    @keyframes colorShift {
        0% { border-top-color: #8b5cf6; }
        33% { border-top-color: #a855f7; }
        66% { border-top-color: #f59e0b; }
        100% { border-top-color: #8b5cf6; }
    }
    
    /* Labels and text */
    .stTextInput > label,
    .stTextArea > label,
    .stSelectbox > label,
    .stFileUploader > label {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Help text */
    .stTextInput > div > div > div,
    .stTextArea > div > div > div,
    .stSelectbox > div > div > div {
        color: #6b7280 !important;
        font-size: 0.85rem !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .upload-container {
            padding: 1.5rem;
            margin: 0.5rem 0;
        }
        
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
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
    st.info("API keys are configured via Streamlit secrets")
    
    st.markdown("---")
    st.markdown("### 📝 How to Use")
    st.markdown("""
    1. Upload an image
    2. Describe what should happen in the video
    3. Click 'Generate Video'
    4. Wait 2-5 minutes for processing
    5. Download your video!
    """)

def upload_to_imgbb(image_file):
    """Upload image to ImgBB and return the URL"""
    try:
        # Check if API key is available
        if not imgbb_key or imgbb_key == "":
            st.error("ImgBB API key not found. Please check your Streamlit secrets.")
            return None
            
        # Convert image to PIL Image and then to bytes
        image = Image.open(image_file)
        
        # Convert to RGB if necessary (ImgBB prefers standard formats)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Save to bytes buffer
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='JPEG', quality=95)
        image_bytes = img_buffer.getvalue()
        
        # Encode image to base64
        import base64
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        # ImgBB API endpoint
        url = "https://api.imgbb.com/1/upload"
        
        # Prepare the data for upload - using form data as recommended by API docs
        data = {
            'key': imgbb_key,
            'image': image_base64,
            'name': 'uploaded_image'
        }
        
        # Debug: Show some info about the image
        st.info(f"Image size: {len(image_bytes)} bytes")
        st.info(f"Base64 length: {len(image_base64)} characters")
        st.info(f"Image format: JPEG")
        
        # Upload to ImgBB
        response = requests.post(url, data=data, timeout=30)
        
        # Debug information
        st.info(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                # Use the direct URL as recommended by API docs
                image_url = result['data']['url']
                st.info(f"Image uploaded successfully! Direct URL: {image_url}")
                
                # Also show the display URL for reference
                display_url = result['data'].get('display_url', image_url)
                st.info(f"Display URL: {display_url}")
                
                # Test if the URL is publicly accessible
                try:
                    test_response = requests.head(image_url, timeout=10)
                    if test_response.status_code == 200:
                        st.success("✅ Image URL is publicly accessible")
                        return image_url
                    else:
                        st.warning(f"⚠️ Image URL returned status: {test_response.status_code}")
                        # Try display URL as fallback
                        test_response_display = requests.head(display_url, timeout=10)
                        if test_response_display.status_code == 200:
                            st.success("✅ Display URL is accessible, using as fallback")
                            return display_url
                        return image_url  # Still return original URL, might work for Replicate
                except Exception as test_error:
                    st.warning(f"⚠️ Could not test image URL accessibility: {test_error}")
                    return image_url  # Still return it, might work for Replicate
            else:
                error_msg = result.get('error', {}).get('message', 'Unknown error')
                st.error(f"ImgBB upload failed: {error_msg}")
                st.error(f"Full response: {result}")
                return None
        elif response.status_code == 403:
            st.error("403 Forbidden: Check if your ImgBB API key is valid and has upload permissions")
            st.error(f"Response text: {response.text}")
            return None
        elif response.status_code == 400:
            st.error("400 Bad Request: Invalid image format or API key issue")
            st.error(f"Response text: {response.text}")
            return None
        else:
            st.error(f"Upload failed with status code: {response.status_code}")
            st.error(f"Response text: {response.text}")
            return None
            
    except Exception as e:
        st.error(f"Error uploading image: {str(e)}")
        return None

def generate_video(image_url, prompt):
    """Generate video using Replicate API"""
    try:
        # Test if the image URL is accessible
        st.info(f"Testing image URL accessibility: {image_url}")
        test_response = requests.head(image_url, timeout=30)
        if test_response.status_code != 200:
            st.error(f"Image URL not accessible: {test_response.status_code}")
            return None
            
        # Call the model using the global client
        output_url = client.run(
            "minimax/hailuo-02-fast",
            input={
                "prompt": prompt,
                "first_frame_image": image_url
            }
        )
        
        return output_url
        
    except requests.exceptions.Timeout:
        st.error("Timeout accessing image URL. The image might not be publicly accessible.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("Connection error accessing image URL. Please try again.")
        return None
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
    
    # Image will be displayed in the results section after generation
    
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
                   not st.session_state.processing)
    
    if st.button("🎬 Generate Video", disabled=not can_generate):
        if not uploaded_file:
            st.error("Please upload an image!")
        elif not prompt.strip():
            st.error("Please enter a prompt!")
        else:
            st.session_state.processing = True
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Processing section
if st.session_state.processing and uploaded_file and prompt.strip():
    st.markdown("---")
    
    # Progress tracking with better styling
    st.markdown('<div class="success-message">🎬 Starting your video generation journey...</div>', unsafe_allow_html=True)
    progress_bar = st.progress(0)
    status_container = st.container()
    
    with status_container:
        # Step 1: Upload image
        st.markdown('<div class="success-message">📤 Step 1: Preparing your image for AI processing...</div>', unsafe_allow_html=True)
        progress_bar.progress(20)
        
        image_url = upload_to_imgbb(uploaded_file)
        
        if image_url:
            st.markdown('<div class="success-message">✅ Step 1 Complete: Image ready for AI magic!</div>', unsafe_allow_html=True)
            progress_bar.progress(40)
            
            # Step 2: Generate video
            st.markdown('<div class="success-message">🎬 Step 2: AI is creating your animated video... This may take 2-5 minutes.</div>', unsafe_allow_html=True)
            progress_bar.progress(60)
            
            video_url = generate_video(image_url, prompt)
            
            if video_url:
                st.markdown('<div class="success-message">✅ Step 2 Complete: Your video is ready!</div>', unsafe_allow_html=True)
                progress_bar.progress(80)
                
                # Step 3: Download video
                st.markdown('<div class="success-message">📥 Step 3: Preparing your video for download...</div>', unsafe_allow_html=True)
                
                video_path, video_bytes = download_video(video_url)
                
                if video_path and video_bytes:
                    progress_bar.progress(100)
                    st.markdown('<div class="success-message">🎉 All Done! Your animated video is ready to enjoy!</div>', unsafe_allow_html=True)
                    
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
    st.subheader("🎥 Before & After Comparison")
    
    # Create two columns for side-by-side display
    col1_result, col2_result = st.columns(2)
    
    with col1_result:
        st.markdown("**📸 Original Image**")
        # Display the original uploaded image
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Original Image", width=400, use_container_width=True)
    
    with col2_result:
        st.markdown("**🎬 Generated Video**")
        # Display video with consistent size
        st.video(st.session_state.video_bytes, width=400)
        
        # Create compact buttons that align with video width
        button_col1, button_col2 = st.columns(2)
        
        with button_col1:
            # Download button - compact size
            st.download_button(
                label="📥 Download",
                data=st.session_state.video_bytes,
                file_name=st.session_state.video_path,
                mime="video/mp4",
                use_container_width=True
            )
        
        with button_col2:
            # Share button - compact size
            if st.button("📤 Share", use_container_width=True):
                st.session_state.show_share_options = True
    
    # Share options modal
    if hasattr(st.session_state, 'show_share_options') and st.session_state.show_share_options:
        st.markdown("---")
        st.subheader("📤 Share Your Video")
        
        # Create share options
        share_col1, share_col2, share_col3, share_col4 = st.columns(4)
        
        with share_col1:
            # Twitter/X
            twitter_url = f"https://twitter.com/intent/tweet?text=Check out my AI-generated video! 🎬&url=YOUR_VIDEO_URL"
            st.markdown(f'<a href="{twitter_url}" target="_blank" style="text-decoration: none;"><button style="background: #1DA1F2; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; width: 100%;">🐦 Twitter/X</button></a>', unsafe_allow_html=True)
        
        with share_col2:
            # Facebook
            facebook_url = f"https://www.facebook.com/sharer/sharer.php?u=YOUR_VIDEO_URL"
            st.markdown(f'<a href="{facebook_url}" target="_blank" style="text-decoration: none;"><button style="background: #4267B2; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; width: 100%;">📘 Facebook</button></a>', unsafe_allow_html=True)
        
        with share_col3:
            # LinkedIn
            linkedin_url = f"https://www.linkedin.com/sharing/share-offsite/?url=YOUR_VIDEO_URL"
            st.markdown(f'<a href="{linkedin_url}" target="_blank" style="text-decoration: none;"><button style="background: #0077B5; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; width: 100%;">💼 LinkedIn</button></a>', unsafe_allow_html=True)
        
        with share_col4:
            # Copy Link
            if st.button("🔗 Copy Link", use_container_width=True):
                st.success("Link copied to clipboard!")
        
        # Close share options
        if st.button("❌ Close", use_container_width=True):
            st.session_state.show_share_options = False
            st.rerun()
    
    # Success message removed as requested
    
    # Reset button
    if st.button("🔄 Generate Another Video"):
        st.session_state.video_generated = False
        st.session_state.video_path = None
        if hasattr(st.session_state, 'video_bytes'):
            delattr(st.session_state, 'video_bytes')
        if hasattr(st.session_state, 'show_share_options'):
            delattr(st.session_state, 'show_share_options')
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
