# Image Upscaler

A beautiful, modern web application that uses Stable Diffusion to upscale and enhance your images.

## Features

- Drag-and-drop image upload
- Optional text prompts to guide the upscaling process
- Modern, responsive UI
- 4x upscaling capability
- Progress indicators and error handling
- Support for various image formats (PNG, JPG, JPEG, GIF)

## Tech Stack

- Backend: Flask (Python)
- Frontend: React with Chakra UI
- ML Model: Stable Diffusion Upscaler (HuggingFace)
- Image Processing: Pillow, Torch

## Prerequisites

- Python 3.8+
- Node.js 14+
- CUDA-capable GPU (recommended)

## Installation

1. Clone the repository
2. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```bash
   cd frontend
   npm install
   ```

## Running the Application

1. Start the backend:
   ```bash
   cd backend
   python app.py
   ```
   The backend will start on http://localhost:8000

2. Start the frontend (in a new terminal):
   ```bash
   cd frontend
   npm start
   ```

3. Open http://localhost:3001 in your browser

## Environment Variables

Create a `.env` file in the backend directory with:
```
SECRET_KEY=your-secret-key
```

## License

MIT
