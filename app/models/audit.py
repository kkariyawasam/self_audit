from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base
from app.models.certificate import Certification


class AuditSession(Base):
    __tablename__ = "audit_sessions"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id"))
    framework = Column(String, default="ISO 27001")
    created_at = Column(DateTime, default=datetime.utcnow)
    admin_status = Column(String, default="Pending") 
    admin_feedback = Column(Text, nullable=True)
    reviewed_at = Column(DateTime, nullable=True)

    questions = relationship(
        "AuditQuestion",
        back_populates="audit_session",
        cascade="all, delete-orphan"
    )
    
    certification = relationship("Certification", back_populates="audit_session", uselist=False)



class AuditQuestion(Base):
    __tablename__ = "audit_questions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("audit_sessions.id"))

    control_id = Column(String)
    question = Column(Text)
    ai_response = Column(Text, default="")
    client_clarification = Column(Text, default="")
    evidence_link = Column(Text, default="")
    clarification_text = Column(Text, nullable=True)
    evidence_files = Column(Text, nullable=True)  
    status = Column(String(20), default="pending") 

    audit_session = relationship(
        "AuditSession",
        back_populates="questions"
    )
   
