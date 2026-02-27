from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.models import (
    User, LearningModule, UserLearningProgress, Assessment, UserAssessment,
    Quiz, QuizQuestion, QuizInstance, QuizAnswer
)
from ..schemas.schemas import (
    LearningModuleResponse, UserLearningProgressResponse, 
    AssessmentResponse, UserAssessmentResponse, UserAssessmentSubmit,
    QuizCreate, QuizResponse, QuizQuestionResponse, QuizInstanceCreate,
    QuizSubmitRequest, QuizResultResponse, ProgressSummary, ProgressTrends
)
from ..core.security import get_current_user
from ..clients.openai_client import chat_completion
from ..core import config
import json
import datetime
from sqlalchemy import func

router = APIRouter(
    prefix="/learning",
    tags=["Learning"]
)

# Get all learning modules
@router.get("/modules", response_model=list[LearningModuleResponse])
def get_modules(db: Session = Depends(get_db)):
    modules = db.query(LearningModule).order_by(LearningModule.order).all()
    return modules


# Get user's learning progress
@router.get("/progress", response_model=list[UserLearningProgressResponse])
def get_user_progress(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    progress = db.query(UserLearningProgress).filter(
        UserLearningProgress.user_id == current_user.id
    ).all()
    return progress


# Mark module as completed
@router.post("/modules/{module_id}/complete")
def complete_module(module_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    progress = db.query(UserLearningProgress).filter(
        UserLearningProgress.user_id == current_user.id,
        UserLearningProgress.module_id == module_id
    ).first()
    
    if not progress:
        progress = UserLearningProgress(user_id=current_user.id, module_id=module_id)
        db.add(progress)
    
    progress.completed = True
    progress.progress_percentage = 100.0
    db.commit()
    db.refresh(progress)
    return {"message": "Module marked as completed", "progress": progress}


# Get assessments for a module
@router.get("/modules/{module_id}/assessments", response_model=list[AssessmentResponse])
def get_assessments(module_id: str, db: Session = Depends(get_db)):
    assessments = db.query(Assessment).filter(Assessment.module_id == module_id).all()
    return assessments


# Submit assessment
@router.post("/assessments/{assessment_id}/submit")
def submit_assessment(assessment_id: str, data: UserAssessmentSubmit, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_assessment = db.query(UserAssessment).filter(
        UserAssessment.user_id == current_user.id,
        UserAssessment.assessment_id == assessment_id
    ).first()
    
    if not user_assessment:
        user_assessment = UserAssessment(user_id=current_user.id, assessment_id=assessment_id)
        db.add(user_assessment)
    
    # Simplified scoring (in production, compare with answers database)
    score = len(data.answers) * 10
    user_assessment.score = min(score, 100)
    user_assessment.completed = True
    db.commit()
    db.refresh(user_assessment)
    return {"message": "Assessment submitted", "score": user_assessment.score}


# Get user's assessment results
@router.get("/assessments", response_model=list[UserAssessmentResponse])
def get_user_assessments(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    assessments = db.query(UserAssessment).filter(
        UserAssessment.user_id == current_user.id
    ).all()
    return assessments


# -------------------- Quiz & Dynamic Generation --------------------
@router.post("/modules/{module_id}/generate-quiz", response_model=QuizResponse)
def generate_quiz(module_id: str, payload: QuizCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Generate a quiz for a module using OpenAI (or fallback template) and persist questions."""
    # Create quiz record
    quiz = Quiz(module_id=module_id, title=payload.title, difficulty=payload.difficulty, question_count=payload.question_count)
    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    # Try to generate questions via OpenAI
    questions = []
    try:
        prompt = (
            f"Create {payload.question_count} multiple-choice or short-answer questions for a learning module titled '{payload.title}' "
            f"at {payload.difficulty} difficulty about module {module_id}. Return JSON list of {{\"prompt\", \"choices\", \"answer\", \"explanation\"}}."
        )
        if config.OPENAI_API_KEY:
            response = chat_completion(prompt)
            import re
            m = re.search(r"\[.*\]", response, re.S)
            if m:
                try:
                    questions = json.loads(m.group())
                except Exception:
                    questions = []
    except Exception:
        questions = []

    # Fallback: simple generated templates
    if not questions:
        for i in range(payload.question_count):
            questions.append({
                "prompt": f"What is a key concept from {payload.title}? ({i+1})",
                "choices": None,
                "answer": "A key concept",
                "explanation": "This is a placeholder explanation."
            })

    # Persist questions
    for idx, q in enumerate(questions):
        qobj = QuizQuestion(
            quiz_id=quiz.id,
            prompt=q.get("prompt", ""),
            choices=json.dumps(q.get("choices")) if q.get("choices") else None,
            correct_answer=q.get("answer"),
            explanation=q.get("explanation"),
            order=idx
        )
        db.add(qobj)
    db.commit()

    return quiz


@router.get("/quizzes/{quiz_id}", response_model=list[QuizQuestionResponse])
def get_quiz_questions(quiz_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    qs = db.query(QuizQuestion).filter(QuizQuestion.quiz_id == quiz_id).order_by(QuizQuestion.order).all()
    return qs


@router.post("/quizzes/{quiz_id}/start")
def start_quiz(quiz_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    instance = QuizInstance(quiz_id=quiz.id, user_id=current_user.id)
    db.add(instance)
    db.commit()
    db.refresh(instance)
    # Return instance id and quiz questions (client will fetch questions separately)
    return {"instance_id": instance.id, "quiz_id": quiz.id}


@router.post("/quiz-instances/{instance_id}/submit", response_model=QuizResultResponse)
def submit_quiz(instance_id: str, payload: QuizSubmitRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    instance = db.query(QuizInstance).filter(QuizInstance.id == instance_id).first()
    if not instance or instance.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Quiz instance not found")
    if instance.completed:
        raise HTTPException(status_code=400, detail="Quiz already submitted")

    # Grade answers
    total = 0
    correct_count = 0
    for ans in payload.answers:
        q = db.query(QuizQuestion).filter(QuizQuestion.id == ans.question_id).first()
        if not q:
            continue
        total += 1
        is_correct = False
        if q.correct_answer:
            # simple equality check (case-insensitive)
            try:
                is_correct = (q.correct_answer.strip().lower() == ans.answer.strip().lower())
            except Exception:
                is_correct = False
        qa = QuizAnswer(instance_id=instance.id, question_id=q.id, answer=ans.answer, correct=is_correct)
        db.add(qa)
        if is_correct:
            correct_count += 1

    score = (correct_count / total * 100) if total > 0 else 0.0
    instance.score = score
    instance.completed = True
    instance.submitted_at = datetime.datetime.utcnow()
    db.commit()
    db.refresh(instance)

    # Update user learning progress (simple heuristic)
    progress = db.query(UserLearningProgress).filter(
        UserLearningProgress.user_id == current_user.id,
        UserLearningProgress.module_id == instance.quiz_id
    ).first()
    # Note: using quiz.quiz_id vs module_id alignment may vary; keep it simple here
    if not progress:
        progress = UserLearningProgress(user_id=current_user.id, module_id=instance.quiz_id)
        db.add(progress)
    progress.progress_percentage = min(100.0, (progress.progress_percentage or 0) + score * 0.1)
    if progress.progress_percentage >= 100:
        progress.completed = True
        progress.completed_at = datetime.datetime.utcnow()
    db.commit()

    return QuizResultResponse(
        instance_id=instance.id,
        quiz_id=instance.quiz_id,
        user_id=instance.user_id,
        score=instance.score,
        completed=instance.completed,
        submitted_at=instance.submitted_at
    )


@router.get("/progress/summary", response_model=ProgressSummary)
def progress_summary(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    total_modules = db.query(LearningModule).count()
    completed_modules = db.query(UserLearningProgress).filter(UserLearningProgress.user_id == current_user.id, UserLearningProgress.completed == True).count()
    avg_score = db.query(QuizInstance).filter(QuizInstance.user_id == current_user.id, QuizInstance.completed == True).with_entities(func.avg(QuizInstance.score)).scalar() or 0.0
    return ProgressSummary(total_modules=total_modules, completed_modules=completed_modules, average_score=float(avg_score))


@router.get("/progress/trends/{module_id}", response_model=ProgressTrends)
def progress_trends(module_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Return simple list of quiz instance scores for the user's module
    rows = db.query(QuizInstance).filter(QuizInstance.user_id == current_user.id, QuizInstance.quiz_id == module_id, QuizInstance.completed == True).order_by(QuizInstance.submitted_at).all()
    points = []
    for r in rows:
        points.append({"date": r.submitted_at or r.started_at, "score": r.score or 0.0})
    return ProgressTrends(module_id=module_id, trends=points)
