# self_audit

An AI-driven self-audit platform for clients to perform compliance assessments

This project is a secure, AI-driven self-auditing platform designed to help organizations assess and prepare for certifications like ISO 27001. Users can upload relevant documents, answer AI-generated questions, and generate a complete audit report for admin review.

# Features

- User Registration & Authentication
- ISO Certification Selection
- AI-Generated Audit Questions
- Client Clarification Upload
- Evidence File Upload
- Full Audit Report (PDF/Web)
- Admin Review & Feedback
- Final Evaluation Status (Accepted/Rejected)

# Tech Stack

- Backend: FastAPI
- Database: MySQL
- ORM: SQLAlchemy
- AI Integration: OpenAI (ChatGPT)
- PDF Generation: FPDF

# Postman Response After File Upload

Below is a sample API response after successfully uploading and parsing a PDF document:
<img width="671" alt="image" src="https://github.com/user-attachments/assets/70291fdc-1a80-4280-889d-a50a73cabd13" />

Below is a sample API response after successfully retrive AI-generated guidance to evaluate documentation against ISO 27001 compliance controls:
<img width="719" alt="image" src="https://github.com/user-attachments/assets/a0aff35e-b586-4ebd-b860-f7eaa2feff1a" />

Below is a sample API response after successfully retrieving the AI-generated validation for the user-uploaded evidence:
<img width="671" alt="image" src="https://github.com/user-attachments/assets/bd00d68f-7c74-4ed1-88de-9ec807263e11" />

