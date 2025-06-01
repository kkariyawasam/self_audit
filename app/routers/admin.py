from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.audit import AuditSession, AuditQuestion

router = APIRouter()

# View all audit sessions
@router.get("/admin/sessions")
def get_all_sessions(db: Session = Depends(get_db)):
    return db.query(AuditSession).all()

# View session details
@router.get("/admin/sessions/{session_id}")
def get_session_detail(session_id: int, db: Session = Depends(get_db)):
    session = db.query(AuditSession).filter_by(id=session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

# Add feedback or approve
@router.post("/admin/sessions/{session_id}/feedback")
def post_admin_feedback(
    session_id: int,
    feedback: str,
    approved: bool,
    db: Session = Depends(get_db),
):
    session = db.query(AuditSession).filter_by(id=session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Save feedback
    cert = Certification(
        audit_session_id=session_id,
        feedback=feedback,
        status="Approved" if approved else "Changes Required",
    )
    db.add(cert)
    db.commit()
    return {"status": "Feedback saved", "approved": approved}
