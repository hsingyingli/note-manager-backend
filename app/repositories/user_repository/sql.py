create_user_query = """
    INSERT INTO users (
        username, email, password
    ) VALUES (
        %s, %s, %s
    );
"""


get_user_by_email_query = """
    SELECT id, username, email, password
    FROM users 
    WHERE email = %s 
    LIMIT 1
"""
