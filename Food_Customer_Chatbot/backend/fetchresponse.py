from db import execute_commit_query, execute_single_query
from sentence_transformers import SentenceTransformer
import emoji


model = SentenceTransformer("all-MiniLM-L6-v2")


def classify_tone(user_query):
    if emoji.emoji_count(user_query) > 0:
        return "Friendly"
    if len(user_query.split()) < 5:
        return "Concise"
    elif "?" in user_query or "please" in user_query:
        return "Friendly"
    elif "thanks" in user_query or "sir" in user_query:
        return "Professional"
    elif "!" in user_query:
        return "Engaging"
    else:
        return "Reassuring"


def log_user_query(query, embedding, response, source=None):
    insert_query = """
        INSERT INTO user_queries (query, embedding, response, source)
        VALUES (%s, %s, %s, %s);
    """
    try:
        execute_commit_query(insert_query, (query, embedding, response, source))
    except Exception as e:
        print(f"Error logging user query: {e}")


def is_polite_closure(query: str) -> bool:
    polite_phrases = ["thank you", "thanks", "appreciate it", "thx", "ty","tysm", "thank you so much", "thank you very much"]
    return any(phrase in query.lower() for phrase in polite_phrases)


def get_responses_for_query(user_query, source=None, top_k=1, threshold=0.3):
    if is_polite_closure(user_query):
        response_text = "You're welcome! 😊 Let me know if you have any more questions."
        log_user_query(user_query, None, response_text, source)
        return {
            "matched_question": None,
            "intent": "Closure",
            "tone": "Friendly",
            "response": response_text
        }

    embedding = model.encode(user_query).tolist()

    try:
        similarity_query = """
            SELECT id, question, intent, embedding <=> CAST(%s AS vector) AS distance
            FROM faq
            ORDER BY distance
            LIMIT %s;
        """
        result = execute_single_query(similarity_query, (embedding, top_k))
    except Exception as e:
        print(f"Error executing similarity query: {e}")
        result = None

    if result:
        faq_id, matched_question, intent, distance = result
        

        if distance < threshold:
            tone = classify_tone(user_query)

            try:
                response_query = """
                    SELECT response
                    FROM faq_response
                    WHERE faq_id = %s AND tone = %s;
                """
                response_row = execute_single_query(response_query, (faq_id, tone))
                response_text = response_row[0] if response_row else "No response available for this tone."
            except Exception as e:
                print(f"Error fetching response: {e}")
                response_text = "An error occurred while fetching the response."

            log_user_query(user_query, embedding, response_text, source)
            return {
                "matched_question": matched_question,
                "intent": intent,
                "tone": tone,
                "response": response_text
            }

    fallback = "I'm sorry, I couldn't find an exact match. Please ask a different question."
    log_user_query(user_query, embedding, fallback, source)
    
    return {
        "matched_question": user_query,
        "intent": "no_match",
        "tone": "Reassuring",
        "response": fallback
    }
