# 🚀 Deploy Image to Video Generator with Lovable

## 📋 Prerequisites

1. **Python 3.8+** installed
2. **API Keys** ready:
   - Replicate API Token
   - ImgBB API Key

## 🛠️ Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements_lovable.txt
```

### 2. Set Environment Variables
Create a `.env` file in your project directory:
```bash
REPLICATE_API_TOKEN=your_replicate_token_here
IMGBB_API_KEY=your_imgbb_key_here
```

### 3. Run Locally
```bash
python app_lovable.py
```

## 🌐 Deploy to Production

### Option 1: Deploy to Lovable Cloud
```bash
# Install Lovable CLI
pip install lovable-cli

# Deploy
lovable deploy app_lovable.py
```

### Option 2: Deploy to Hugging Face Spaces
1. Create a new Space on Hugging Face
2. Upload your `app_lovable.py` and `requirements_lovable.txt`
3. Set environment variables in Space settings

### Option 3: Deploy to Railway
1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically

## 🎨 Lovable Advantages

- ✅ **Better UI**: More flexible and customizable than Streamlit
- ✅ **Modern Design**: Built-in beautiful components
- ✅ **Easy Deployment**: One-click deployment options
- ✅ **Better UX**: Professional, responsive interface
- ✅ **Custom Styling**: More control over appearance

## 🔧 Customization

The Lovable version includes:
- Modern file upload with preview
- Better progress indicators
- Responsive layout with columns
- Modal dialogs for sharing
- Professional button styling
- Error handling with colored messages

## 📱 Features

- **Image Upload**: Drag & drop or click to upload
- **Prompt Input**: Large text area for descriptions
- **Progress Tracking**: Real-time progress updates
- **Video Generation**: AI-powered video creation
- **Download**: Direct video download
- **Sharing**: Social media sharing options
- **Responsive**: Works on desktop and mobile

## 🚀 Next Steps

1. Test the app locally
2. Set up your API keys
3. Deploy to your preferred platform
4. Share your deployed app!

---

**Note**: Keep your original `app.py` (Streamlit version) for comparison or as a backup. 