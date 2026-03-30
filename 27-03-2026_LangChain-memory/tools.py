from langchain_core.tools import tool
@tool
def get_user_info():
    """
        Fetches the profile information for a given user ID.
        Use this tool whenever we need to know a user's name or preferences.
    """
    return "User info tool working"
