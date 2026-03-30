from langchain_mongodb import MongoDBChatMessageHistory
from config import MONGO_URI, DB_NAME, COLLECTION_NAME, SESSION_ID

# 1. Long-term memory (MongoDB)
# This connects directly to your DB
history = MongoDBChatMessageHistory(
    connection_string=MONGO_URI,
    session_id=SESSION_ID,
    database_name=DB_NAME,
    collection_name=COLLECTION_NAME
)

def get_history():
    """
    Returns only the last 4 messages (Short-term memory)
    from the full history stored in MongoDB.
    """
    all_messages = history.messages
    # This replaces ConversationBufferWindowMemory(k=4)
    return all_messages[-4:] if all_messages else []

def save_message(user_input, ai_output):
    """
    Saves the conversation to MongoDB (Long-term).
    """
    history.add_user_message(user_input)
    history.add_ai_message(ai_output)
