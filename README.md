# 🎬 Image to Video Generator

Transform your static images into dynamic animated videos using AI! This application uses Replicate's Minimax Hailuo model to generate stunning video content from images and text prompts.

![App Screenshot](https://via.placeholder.com/800x400/667eea/ffffff?text=Image+to+Video+Generator)

## ✨ Features

- 🖼️ **Drag & Drop Upload** - Easy image uploading with preview
- 🎨 **Beautiful UI** - Modern gradient design with smooth animations
- 🤖 **AI-Powered** - Uses Minimax Hailuo-02-fast model via Replicate
- 📱 **Responsive** - Works perfectly on desktop and mobile
- ⚡ **Real-time Progress** - Live updates during video generation
- 📥 **Easy Download** - One-click video download
- 🔒 **Secure** - API tokens handled securely

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Replicate API account and token
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/image-to-video-generator.git
   cd image-to-video-generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501`

5. **Get your Replicate API token**
   - Sign up at [Replicate](https://replicate.com)
   - Go to your account settings
   - Copy your API token
   - Enter it in the app's sidebar

## 🎯 How to Use

1. **Enter API Token** - Add your Replicate API token in the sidebar
2. **Upload Image** - Drag and drop or click to upload an image (PNG, JPG, JPEG, GIF)
3. **Write Prompt** - Describe what should happen in the video
4. **Generate** - Click the "Generate Video" button
5. **Wait** - Processing takes 2-5 minutes
6. **Download** - Save your generated video

## 🎨 Example Prompts

- "A cat starts dancing and spinning around"
- "The flowers bloom and petals fall like snow"
- "The person waves hello and smiles"
- "The car drives away into the sunset"
- "The bird spreads its wings and takes flight"

## 🛠️ Tech Stack

- **Frontend/Backend**: Streamlit
- **AI Model**: Minimax Hailuo-02-fast (via Replicate)
- **Image Hosting**: PostImage API
- **Styling**: Custom CSS with gradient animations
- **File Handling**: PIL, Requests

## 📁 Project Structure

```
image-to-video-generator/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── .gitignore            # Git ignore rules
├── LICENSE               # MIT License
└── assets/               # Screenshots and demo files
    └── demo.gif
```

## 🔧 Configuration

### Environment Variables (Optional)

Create a `.env` file:
```bash
REPLICATE_API_TOKEN=your_token_here
```

### Supported Image Formats

- PNG
- JPG/JPEG
- GIF

### Video Output

- Format: MP4
- Quality: HD
- Duration: ~5-10 seconds
- Processing Time: 2-5 minutes

## 🚀 Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click!

### Deploy to Heroku

1. Create a `Procfile`:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Deploy to Railway

1. Connect your GitHub repository
2. Railway will auto-detect and deploy

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Important Notes

- You need a Replicate API account to use this application
- Video generation costs vary based on usage (check Replicate pricing)
- Processing time depends on server load (typically 2-5 minutes)
- Keep your API token secure and never commit it to version control

## 🐛 Troubleshooting

**Common Issues:**

1. **"Invalid API token"**
   - Double-check your Replicate API token
   - Ensure you have sufficient credits

2. **"Upload failed"**
   - Check your internet connection
   - Try a smaller image file
   - Ensure image format is supported

3. **"Generation timeout"**
   - This is normal during high server load
   - Try again in a few minutes

## 📞 Support

If you encounter any issues or have questions:

- 🐛 [Report a Bug](https://github.com/yourusername/image-to-video-generator/issues)
- 💡 [Request a Feature](https://github.com/yourusername/image-to-video-generator/issues)
- 📧 Email: your.email@example.com

## 🌟 Show Your Support

Give a ⭐️ if this project helped you!

## 📸 Screenshots

![Upload Interface](https://via.placeholder.com/600x300/764ba2/ffffff?text=Upload+Interface)
![Processing](https://via.placeholder.com/600x300/f093fb/ffffff?text=Processing+Steps)
![Results](https://via.placeholder.com/600x300/667eea/ffffff?text=Video+Results)

---

**Made with ❤️ and powered by AI**
