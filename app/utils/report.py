from fpdf import FPDF

def generate_audit_report_pdf(audit_session, questions):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"Audit Report: Session #{audit_session.id}", ln=True, align='C')

    for q in questions:
        pdf.ln(10)
        pdf.multi_cell(0, 10, txt=f"Control: {q.control_id}")
        pdf.multi_cell(0, 10, txt=f"Initial Evaluation: {q.question}")
        pdf.multi_cell(0, 10, txt=f"Clarification: {q.ai_response}")
        pdf.multi_cell(0, 10, txt=f"Evidenytce Files: {q.evidence_link}")
        pdf.multi_cell(0, 10, txt=f"Final Evaluation: {q.final_ai_evaluation}")
        pdf.cell(0, 10, txt=f"Status: {q.status}", ln=True)

    return pdf
