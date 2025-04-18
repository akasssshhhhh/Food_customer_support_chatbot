import json
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection
def connect_db():
    return psycopg2.connect(
        dbname='chatbot',
        user='postgres',
        password='root',
        host='localhost',
        port='5432'
    )

# Function to insert a question into the `faq` table, including the embedding
def insert_question(cursor, question, intent, embedding):
    query = "INSERT INTO faq (question, intent, embedding) VALUES (%s, %s, %s) RETURNING id;"
    cursor.execute(query, (question, intent, embedding))
    return cursor.fetchone()['id']

# Function to insert a response into the `faq_response` table
def insert_response(cursor, faq_id, tone, response):
    query = "INSERT INTO faq_response (faq_id, tone, response) VALUES (%s, %s, %s);"
    cursor.execute(query, (faq_id, tone, response))

# Function to process the JSON data and insert it into the database
def insert_data_from_json(json_data):
    conn = connect_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Iterate over each question in the JSON data
        for item in json_data:
            question = item['question']
            intent = item['intent']
            responses = item['responses']
            embedding = item['embedding']  # Use the existing embedding from the JSON data

            # Insert the question along with the embedding and get the returned question ID
            faq_id = insert_question(cursor, question, intent, embedding)

            # Insert all responses for the question
            for response_item in responses:
                tone = response_item['tone']
                response = response_item['response']
                insert_response(cursor, faq_id, tone, response)
        
        # Commit the changes
        conn.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# Main function to load JSON file and insert data into the database
def main():
    with open('C:/Users/Akash/chatbot_data.json', 'r',encoding='utf-8') as file:
        json_data = json.load(file)
    insert_data_from_json(json_data)

if __name__ == "__main__":
    main()
