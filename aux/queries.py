from aux.db import Db
from aux.func import format_phone_number
from aux.mod import User, Question, token_limit_default

db = Db()

def insert_user(user: User):
    user_query = f"INSERT INTO users (name, telephone, email, token_limit, token_used, OTP) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;"
    values = (user.name, format_phone_number(user.telefone), user.email, token_limit_default, 0, 'sdf645')
    return db.query_insert(user_query, values)

def verify_user(email: str) -> User:
    select_user = f"SELECT * FROM users WHERE email = '{email}';"
    ret = db.query_select(select_user)
    if len(ret) > 0:
        return ret[0]
    return

def insert_question(question: Question):
    user_query = f"INSERT INTO questions (user_id, session_id, question, answer, feedback, used_tokens) VALUES () RETURNING id;"
    values = (question.user_id, question.session_id, question.question, question.answer, question.feedback, question.used_tokens)
    return db.query_insert(user_query, values)

def update_feedback(feedback: bool, question_id: int):
    user_query = f"UPDATE questions SET feedback = %s WHERE id = %s;"
    values = (feedback, question_id)
    db.query_insert(user_query, values)
