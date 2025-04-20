# 🍽️ Food Customer Chatbot

An AI-powered customer support chatbot designed for food service businesses. This project integrates a FastAPI backend, Streamlit frontend, and PostgreSQL database (with pgvector) — all containerized using Docker.

## 🚀 Features

- ✅ Instant responses to common food-related FAQs
- 🔍 Semantic search using vector embeddings (pgvector)
- 💬 Multiple response tones: Concise, Friendly, Professional, Engaging, Reassuring
- 📦 Dockerized backend, frontend, and database
- 📄 Automatically populates the database with questions and answers on startup
- 🌐 Easy local or cloud deployment
## 🧱 Project Structure

```text
├── backend/
│   ├── main.py                    # FastAPI app
│   ├── db.py                      # db connection
│   ├── dockerfile                 # Dockerfile for backend
│   ├── fetchresponse.py           # Core chatbot logic
│   ├── dbconnection.env           # DB credentials( Not uploaded,You have to create on your own)
│   └── requirements.txt
├── frontend/
│   ├── chatbot_ui.py              # Streamlit frontend
│   ├── get_chatbot_response.py    # Streamlit frontend
│   ├── dockerfile                 # Dockerfile for frontend
│   ├── .streamlit                 # streamlit customization
│   └── requirements.txt
├── init.sql                       # SQL to auto-create tables and insert data
├── entry.py                       # Python script to insert data into respective tables in database
├── Chatbot_data.json              # Sample data
├── docker-compose.yml             # Docker multi-container setup
└── README.md

## ⚙️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Database**: PostgreSQL with pgvector
- **NLP**: BERT (sentence-transformers)
- **Containerization**: Docker & Docker Compose

## 🐳 Running Locally with Docker

```bash
git clone https://github.com/akasssshhhhh/Food_customer_support_chatbot.git
cd Food_customer_support_chatbot
docker-compose up --build

## 📚 What I Learned & Challenges Faced

- I initially tried deploying on Render but faced issues due to limited Docker Compose support.
- I experimented with multiple platforms like Railway and Fly.io, but ended up using ngrok for its simplicity.
- Managing `.env` secrets during deployment was tricky — I learned how important it is to keep credentials out of public repos.
- Database initialization on cloud platforms was a pain, so I automated it using Docker and an `init.sql` file.
- My original plan was to enhance the chatbot with real FAQs from platforms like Domino’s, Swiggy, and Zomato using web scraping. But I avoided that due to potential legal issues.
- I also tried integrating OpenAI’s API for fallback answers, but the cost made it impractical for this project.
- Overall, this project helped me understand full-stack architecture and deployment, especially using Docker and container orchestration.
