# Crypto Market Dashboard 🚀

A FastAPI-powered cryptocurrency market dashboard that fetches real-time data from CoinGecko API with caching functionality.

![Dashboard Screenshot]((https://imgur.com/a/IMxBBiN))

## Features ✨

- Real-time cryptocurrency market data
- Responsive UI with interactive charts
- Intelligent caching for better performance
- Search and filter functionality
- Multiple currency support
- Paginated results

## Tech Stack 🛠️

- **Backend**: FastAPI, Python
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js
- **Caching**: CacheTools
- **API**: CoinGecko API

## Prerequisites 📋

- Python 3.7+
- fastAPI
- pytest

## 🚀 Project Setup
Follow the steps below to set up and run this project locally.

### 1. Clone the Repository

```
bash
git clone https://github.com/agrawal-raj/coinapi.git
cd coinapi
```

### 2. Install Dependencies
Make sure you have Python 3.7+ installed, then install the required packages:
```
bash:
pip install fastapi uvicorn httpx python-dotenv cachetools
```

### 3. Run the Application
Use the following command to start the FastAPI server:
```
bash:
uvicorn app.main:app --reload
```

This will start the development server at:
📍 http://127.0.0.1:8000

You can access the interactive API docs at:
🔍 http://127.0.0.1:8000/docs
