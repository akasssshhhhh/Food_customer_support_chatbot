import json
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

def connect_db():
    return psycopg2.connect(
        dbname='chatbot',
        user='postgres',
        password='root',
        host='localhost',
        port='5432'
    )

def insert_question(cursor, question, intent, embedding):
    query = "INSERT INTO faq (question, intent, embedding) VALUES (%s, %s, %s) RETURNING id;"
    cursor.execute(query, (question, intent, embedding))
    return cursor.fetchone()['id']

def insert_response(cursor, faq_id, tone, response):
    query = "INSERT INTO faq_response (faq_id, tone, response) VALUES (%s, %s, %s);"
    cursor.execute(query, (faq_id, tone, response))


def insert_data_from_json(json_data):
    conn = connect_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        for item in json_data:
            question = item['question']
            intent = item['intent']
            responses = item['responses']
            embedding = item['embedding']  
            faq_id = insert_question(cursor, question, intent, embedding)
            for response_item in responses:
                tone = response_item['tone']
                response = response_item['response']
                insert_response(cursor, faq_id, tone, response)
                
        conn.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def main():
    with open('C:/Users/Akash/chatbot_data.json', 'r',encoding='utf-8') as file:
        json_data = json.load(file)
    insert_data_from_json(json_data)

if __name__ == "__main__":
    main()
