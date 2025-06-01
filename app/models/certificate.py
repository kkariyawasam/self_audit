from app.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship


class Certification(Base):
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True, index=True)
    audit_session_id = Column(Integer, ForeignKey("audit_sessions.id"))
    feedback = Column(Text)
    status = Column(String) 

    audit_session = relationship("AuditSession", back_populates="certification")
