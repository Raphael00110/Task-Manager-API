from typing import Optional
from Database.connection import get_connection
from psycopg.rows import dict_row # Added this soo fastapi can communicate properly with SQL in the Dict Format




def create_user(user: dict):
          query = ("""
                    INSERT INTO users (username, email, password)
                    VALUES(%(username)s, %(email)s, %(password)s)
                    RETURNING id, username, email;

                    """)
          with get_connection() as connection:
                 with connection.cursor(row_factory=dict_row) as cursor:
                        cursor.execute(query, user)
                        result = cursor.fetchone()
                        connection.commit()
                        return result
def get_user_by_username(username: str):
       query = ("SELECT id, username, email FROM users WHERE username = %s;")
       with get_connection() as connection:
              with connection.cursor(row_factory=dict_row) as cursor:
                     cursor.execute(query, (username,))
                     return cursor.fetchone()

def get_user_by_email(email: str):
       query = ("SELECT id, username, email FROM users WHERE email = %s;")
       with get_connection() as connection:
              with connection.cursor(row_factory=dict_row) as cursor:
                     cursor.execute(query,(email,))
                     return cursor.fetchone()


def get_user_credentials(username: str):
       query = ("""SELECT id, username, email, password FROM users
                   WHERE username = %s""")
       with get_connection() as connection:
              with connection.cursor(row_factory=dict_row) as cursor:
                     cursor.execute(query,(username,))
                     return cursor.fetchone()
