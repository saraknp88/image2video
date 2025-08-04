import lovable as lv
import replicate
import requests
from PIL import Image
import io
import base64
import os

# Initialize clients and API keys
client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))
imgbb_key = os.getenv("IMGBB_API_KEY")

def upload_to_imgbb(image_file):
    """Upload image to ImgBB and return the URL"""
    try:
        if not imgbb_key:
            return None
            
        # Process image with PIL
        image = Image.open(image_file)
        image = image.convert('RGB')
        
        # Save to bytes buffer
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='JPEG', quality=95)
        image_bytes = img_buffer.getvalue()
        
        # Encode to base64
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        # Upload to ImgBB
        url = "https://api.imgbb.com/1/upload"
        data = {
            "key": imgbb_key,
            "image": image_base64,
            "name": "uploaded_image"
        }
        
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            result = response.json()
            image_url = result['data']['url']
            
            # Test if URL is accessible
            try:
                requests.head(image_url, timeout=5)
                return image_url
            except:
                return result['data']['display_url']
        else:
            return None
            
    except Exception as e:
        return None

def generate_video(image_url, prompt):
    """Generate video using Replicate API"""
    try:
        # Test if image URL is accessible
        try:
            requests.head(image_url, timeout=5)
        except:
            return None
            
        output = client.run(
            "minimax/hailuo-02-fast",
            input={
                "image": image_url,
                "prompt": prompt,
                "num_frames": 16,
                "fps": 8
            }
        )
        
        if output and len(output) > 0:
            return output[0]
        return None
        
    except Exception as e:
        return None

def download_video(video_url):
    """Download video and return file path and bytes"""
    try:
        response = requests.get(video_url)
        if response.status_code == 200:
            video_bytes = response.content
            
            # Generate filename with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_video_{timestamp}.mp4"
            
            return filename, video_bytes
        return None, None
        
    except Exception as e:
        return None, None

# Create Lovable app
app = lv.App(
    title="🎬 Image to Video Generator",
    description="Transform your images into animated videos using AI",
    theme="light"
)

# Main interface
with app.page("Generate Video"):
    
    # Header
    lv.header("🎬 Image to Video Generator", size="large")
    lv.text("Transform your images into animated videos using AI", color="gray")
    
    # Upload section
    with lv.section("📤 Upload Your Image"):
        uploaded_file = lv.file_upload(
            label="Choose an image file",
            accept=["image/png", "image/jpg", "image/jpeg", "image/gif"],
            help="Upload the image you want to animate"
        )
    
    # Prompt section
    with lv.section("✍️ Describe Your Vision"):
        prompt = lv.text_area(
            label="Enter your prompt:",
            placeholder="Describe the changes you want to see in the video...",
            value="an elephant turns blue and raises its trunk",
            rows=4,
            help="Describe what should happen in the video"
        )
    
    # Generate button
    generate_btn = lv.button(
        "🎬 Generate Video",
        variant="primary",
        size="large",
        disabled=not uploaded_file or not prompt
    )
    
    # Processing section
    if generate_btn.clicked and uploaded_file and prompt:
        with lv.section("🔄 Processing"):
            progress = lv.progress(value=0, max=100)
            
            # Step 1: Upload image
            progress.value = 20
            lv.text("📤 Uploading image...")
            image_url = upload_to_imgbb(uploaded_file)
            
            if image_url:
                progress.value = 40
                lv.text("✅ Image uploaded successfully!")
                
                # Step 2: Generate video
                progress.value = 60
                lv.text("🎬 Generating video... This may take 2-5 minutes.")
                video_url = generate_video(image_url, prompt)
                
                if video_url:
                    progress.value = 80
                    lv.text("✅ Video generated successfully!")
                    
                    # Step 3: Download video
                    progress.value = 90
                    lv.text("📥 Preparing video for download...")
                    video_path, video_bytes = download_video(video_url)
                    
                    if video_path and video_bytes:
                        progress.value = 100
                        lv.text("🎉 Video ready!", color="success")
                        
                        # Results section
                        with lv.section("🎥 Before & After Comparison"):
                            
                            # Create two columns
                            with lv.columns(2):
                                # Original image
                                with lv.column():
                                    lv.subheader("📸 Original Image")
                                    if uploaded_file:
                                        image = Image.open(uploaded_file)
                                        lv.image(image, caption="Original Image")
                                
                                # Generated video
                                with lv.column():
                                    lv.subheader("🎬 Generated Video")
                                    lv.video(video_url, controls=True)
                                    
                                    # Action buttons
                                    with lv.row():
                                        lv.download_button(
                                            "📥 Download",
                                            data=video_bytes,
                                            filename=video_path,
                                            mime="video/mp4",
                                            variant="primary"
                                        )
                                        
                                        share_btn = lv.button("📤 Share", variant="secondary")
                                        
                                        if share_btn.clicked:
                                            with lv.modal("Share Video"):
                                                lv.subheader("📤 Share Your Video")
                                                
                                                with lv.columns(2):
                                                    lv.button("🐦 Twitter/X", variant="outline")
                                                    lv.button("📘 Facebook", variant="outline")
                                                    lv.button("💼 LinkedIn", variant="outline")
                                                    lv.button("🔗 Copy Link", variant="outline")
                    else:
                        lv.text("❌ Error downloading video", color="error")
                else:
                    lv.text("❌ Error generating video", color="error")
            else:
                lv.text("❌ Error uploading image", color="error")

# Run the app
if __name__ == "__main__":
    app.run() 
