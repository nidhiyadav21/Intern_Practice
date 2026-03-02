# This is where your Pydantic models live. They act as a blueprint for your data.
# transaction_schema.py: Defines what a Transaction looks like (e.g., amount must be a float, date must be a datetime).
# base_schema.py: Likely contains a generic response wrapper (like your APIResponse class) so every API response has the same format.