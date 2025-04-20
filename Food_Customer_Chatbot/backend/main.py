from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from fetchresponse import get_responses_for_query

app = FastAPI()

class UserQuery(BaseModel):
    query: str

@app.post("/get_response/")
def get_response(query: UserQuery, request: Request):
    user_ip = request.client.host
    try:
        result = get_responses_for_query(query.query, source=user_ip)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the query: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
