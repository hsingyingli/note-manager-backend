create_session_query = """ 
    INSERT INTO sessions (
       id, user_id, expired_at, refresh_token
    ) VALUES (
        %s, %s, %s, %s
    ) RETURNING id;
"""


get_session_by_id_query = """
    SELECT id, user_id, refresh_token
    FROM sessions
    WHERE id = %s AND expired_at > %s
    LIMIT 1
"""

expire_session_query = """ 
    UPDATE sessions 
    SET expired_at = %s 
    WHERE id = %s
"""
