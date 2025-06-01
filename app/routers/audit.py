from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.utils.deps import get_current_user
from app.models.audit import AuditSession, AuditQuestion
from app.models.user import User
from app.data.controls import ISO_CONTROLS
from app.models.file import UploadedFile
from app.services.llm import ask_ai_with_context 
from fastapi import Form
import os
from app.utils.ai import evaluate_control_final
from fastapi.responses import StreamingResponse, HTMLResponse
from app.utils.report import generate_audit_report_pdf
from io import BytesIO
from datetime import datetime

from fastapi import File, UploadFile
import shutil
import uuid

router = APIRouter(
    prefix="/audit",
    tags=["Audit"]
)

@router.post("/start", status_code=201)
def start_audit(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Create a new audit session for the current user
    session = AuditSession(client_id=current_user.id)
    db.add(session)
    db.commit()
    db.refresh(session)

    # Add predefined audit questions to the session
    for control in ISO_CONTROLS:
        question = AuditQuestion(
            session_id=session.id,
            control_id=control["control_id"],
            question=control["question"]
        )
        db.add(question)

    db.commit()

    return {
        "message": "Audit session started successfully",
        "session_id": session.id,
        "total_questions": len(ISO_CONTROLS)
    }


@router.get("/next-question/{session_id}")
def get_next_question(session_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    session = db.query(AuditSession).filter_by(id=session_id, client_id=current_user.id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Audit session not found")

    question = (
        db.query(AuditQuestion)
        .filter_by(session_id=session.id, status="pending")
        .order_by(AuditQuestion.id)
        .first()
    )

    if not question:
        return {"message": "All questions answered"}

    files = db.query(UploadedFile).filter_by(owner_id=current_user.id).all()
    file_texts = "\n\n".join([f.filename + ":\n" + f.extracted_text for f in files if f.extracted_text])

    # Ask AI
    ai_answer = ask_ai_with_context(question.question, file_texts)

    # Save the AI response
    question.ai_response = ai_answer
    question.status = "needs_clarification"
    db.commit()

    return {
        "control_id": question.control_id,
        "question": question.question,
        "ai_response": ai_answer,
        "question_id": question.id
    }
    
    
@router.post("/answer/{question_id}")
def answer_question(
    question_id: int,
    clarification_text: str = Form(...),
    files: list[UploadFile] = File([]),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    question = db.query(AuditQuestion).filter_by(id=question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Save clarification
    question.client_clarification = clarification_text

    question_folder = os.path.join("uploads", "evidence", f"question_{question.id}")
    os.makedirs(question_folder, exist_ok=True)


    for upload in files:
        file_ext = upload.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_ext}"
        file_path = os.path.join(question_folder, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload.file, buffer)

    question.evidence_link = question_folder

    final_evaluation = evaluate_control_final(
        question_id=question_id,
        clarification_text=clarification_text,
        evidence_files=question_folder
    )

    # Save evaluation result and status
    question.final_evaluation = final_evaluation
    question.status = "Pass" if final_evaluation["is_compliant"] else "Not Compliant"
    
    
    question.status = "complete"
    db.commit()

    return {
        "message": "Answer, evidence, and final evaluation saved",
        "evaluation_result": final_evaluation
    }

@router.get("/report/{session_id}/pdf")
def get_pdf_report(session_id: int, db: Session = Depends(get_db)):
    session = db.query(AuditSession).filter_by(id=session_id).first()
    questions = db.query(AuditQuestion).filter_by(session_id=session_id).all()
    print(questions)

    if not session or not questions:
        raise HTTPException(status_code=404, detail="Audit session not found")

    pdf = generate_audit_report_pdf(session, questions)
    
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_buffer = BytesIO(pdf_bytes)
    pdf_buffer.seek(0)

    return StreamingResponse(
        pdf_buffer,
        media_type='application/pdf',
        headers={"Content-Disposition": f"attachment; filename=audit_session_{session_id}.pdf"}
    )

@router.post("/session/{session_id}/review")
def review_session(session_id: int, status: str, feedback: str = "", db: Session = Depends(get_db)):
        if status not in ["Accepted", "Rejected"]:
            raise HTTPException(status_code=400, detail="Invalid status")

        print(status)
        print(feedback)
        session = db.query(AuditSession).filter(AuditSession.id == session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Audit session not found")

        session.admin_status = status
        session.admin_feedback = feedback
        session.reviewed_at = datetime.utcnow()
        db.commit()

        return {"message": f"Session {status.lower()} successfully"}