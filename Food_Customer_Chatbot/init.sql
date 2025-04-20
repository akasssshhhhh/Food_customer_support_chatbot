
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS public.faq (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    intent TEXT,
    embedding vector(384)
);

CREATE TABLE IF NOT EXISTS public.faq_response (
    id SERIAL PRIMARY KEY,
    faq_id INTEGER REFERENCES public.faq(id) ON DELETE CASCADE,
    tone TEXT,
    response TEXT
);

CREATE TABLE user_queries (
    id SERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    embedding VECTOR(384), 
    response TEXT NOT NULL,
    source TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
