"""
Small integration test for quiz generation and submission (requires OPENAI key to generate questions or will fallback).
Run: python test_quiz_flow.py
"""
import asyncio
from fin_ai.database import SessionLocal
from fin_ai.models.models import Quiz, QuizQuestion, QuizInstance
from fin_ai.routes.learning import generate_quiz, start_quiz, submit_quiz
from fin_ai.schemas.schemas import QuizCreate, QuizSubmitRequest, QuizAnswerSubmit
from fin_ai.models.models import User

# This script simulates calling the routes directly (bypassing HTTP)

def run_test():
    # Ensure DB schema is up-to-date for test run
    from fin_ai.database import engine
    from fin_ai.models import models as m
    m.Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    # Use a demo module id
    module_id = "demo-module-1"
    payload = QuizCreate(module_id=module_id, title="Intro to Stocks", difficulty="beginner", question_count=3)
    # Use a fake user: find the first user
    user = db.query(User).first()
    if not user:
        print('No users found; create a user via auth endpoints first.')
        return
    
    # Generate quiz
    quiz = generate_quiz(module_id, payload, current_user=user, db=db)
    print('Generated quiz:', quiz.id, quiz.title)
    
    # Start quiz (simulate)
    start = start_quiz(quiz.id, current_user=user, db=db)
    instance_id = start['instance_id']
    print('Started instance:', instance_id)
    
    # Fetch questions
    questions = db.query(QuizQuestion).filter(QuizQuestion.quiz_id == quiz.id).all()
    answers = []
    for q in questions:
        answers.append(QuizAnswerSubmit(question_id=q.id, answer=(q.correct_answer or 'A key concept')))
    submit_payload = QuizSubmitRequest(answers=answers)
    result = submit_quiz(instance_id, submit_payload, current_user=user, db=db)
    print('Submission result:', result.score, 'completed=', result.completed)

if __name__ == '__main__':
    run_test()
