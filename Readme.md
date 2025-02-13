# Crypto Dashboard - Flask API & Streamlit UI

This project provides a **real-time cryptocurrency dashboard** that fetches data from the **CoinMarketCap API** and stores it in **MongoDB**. The **Flask API** serves the data, while **Streamlit** provides an interactive UI.

## **Features**
Fetch **live cryptocurrency data** every 5 minutes  
Store cryptocurrency data in **MongoDB Atlas**  
API with **Swagger documentation** (`/apidocs`)  
Interactive **Streamlit Dashboard**  
**Manual & Auto Data Refresh**  
**Deployed on Render**

---

## **Tech Stack**
- **Backend**: Flask, Flask-PyMongo, Flask-CORS, Flask-Swagger
- **Database**: MongoDB Atlas
- **Frontend**: Streamlit
- **Deployment**: Render

---

## **Setup Instructions**
### **Clone the Repository**
```bash
git clone https://github.com/shouryamanekar/crypto_api.git
cd crypto-dashboard
```

### **Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### **Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Set Up Environment Variables**
Create a `.env` file in the project root and update with your credentials:
```ini
# MongoDB Atlas Connection String
MONGO_URI=your_mongodb_url

# CoinMarketCap API Key
CMC_API_KEY=your_coinmarketcap_api_key

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```
Replace `your_mongodb_url` and `your_coinmarketcap_api_key` with actual credentials.

---

## **Running the Project**
### **Start the MongoDB Database**
Ensure **MongoDB Atlas** is set up correctly.

### **Run Flask API & Streamlit Dashboard**
```bash
python crypto_api.py
```
✔ **Flask API runs on:** `http://127.0.0.1:5000/`   
✔ **Swagger API Docs:** `http://127.0.0.1:5000/apidocs`  

---

## **API Documentation**
### **Base URL**
```
http://127.0.0.1:5000/api/
```
### **Endpoints**
| Method | Endpoint         | Description |
|--------|-----------------|-------------|
| `GET`  | `/api/fetch`     | Fetches & stores the latest crypto data in MongoDB |
| `GET`  | `/api/market_data` | Retrieves all stored cryptocurrency data |

### **Example API Response**
```json
[
  {
    "name": "Bitcoin",
    "symbol": "BTC",
    "price": 48000.15,
    "market_cap": 910000000000,
    "volume_24h": 32000000000,
    "percent_change_24h": 2.5
  },
  {
    "name": "Ethereum",
    "symbol": "ETH",
    "price": 3200.50,
    "market_cap": 390000000000,
    "volume_24h": 20000000000,
    "percent_change_24h": 1.8
  }
]
```

---

## **Usage Instructions**
### **Fetch Latest Data Manually**
Click the **"Fetch Latest Data"** button in Streamlit to update immediately.

### **Auto-Refresh Every 5 Minutes**
✔ Data is refreshed automatically in the background.  
✔ **Streamlit updates dynamically** every 5 minutes.

---

## **Deployment Instructions (Render)**
### **Create `render.yaml`**
```yaml
services:
  - type: web
    name: crypto-app
    env: python
    buildCommand: |
      pip install -r requirements.txt
    startCommand: python crypto_api.py
    envVars:
      - key: PORT
        value: 5000
```

### **Push to GitHub**
```bash
git add .
git commit -m "Deploy Flask & Streamlit on Render"
git push origin main
```

### **Deploy on Render**
- **Go to [Render](https://dashboard.render.com/)**.
- Click **New Web Service** → **Connect GitHub Repo**.
- **Set Start Command:** `python crypto_api.py`
- **Deploy!** 🚀

---

**Need help?** Feel free to open an issue.  
