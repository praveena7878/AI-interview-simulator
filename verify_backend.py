import os
import json
from app.database import init_db, SessionLocal, InterviewSession, InterviewQuestion
from app.rag_engine import rag_engine
from app.report_generator import ReportGenerator

def main():
    print("=== AI Interview Simulator Backend Verification ===")
    
    # 1. Initialize DB
    print("\n1. Initializing Database Schema...")
    init_db()
    print("Database schema successfully created.")

    db = SessionLocal()
    try:
        # 2. Test DB inserts
        print("\n2. Writing mock data to SQLite...")
        session = InterviewSession(
            candidate_name="Alice Smith",
            candidate_email="alice@example.com",
            target_role="AI Engineer",
            skills=json.dumps(["Python", "PyTorch", "Transformers", "SQL"])
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        print(f"Mock session created with ID: {session.id}")

        # 3. Test RAG Engine
        print("\n3. Testing RAG Retrieve...")
        questions = rag_engine.retrieve_questions(
            role="AI Engineer",
            skills=["Python", "PyTorch", "Transformers"],
            category="AI",
            difficulty="Medium",
            limit=2
        )
        print(f"Retrieved {len(questions)} relevant questions:")
        for q in questions:
            print(f"  - [{q['category']} - {q['difficulty']}] {q['question']}")

        # 4. Insert mock questions and answers
        print("\n4. Adding mock Q&A history...")
        q1 = InterviewQuestion(
            session_id=session.id,
            question_text="Explain overfitting and underfitting in Machine Learning. How do you prevent overfitting in deep neural networks?",
            category="AI",
            difficulty="Medium",
            sequence_number=1,
            answer_text="Overfitting happens when a model learns the noise in training data. We can prevent it using dropout layers, regularization like L2, and early stopping.",
            score_correctness=8.5,
            score_completeness=8.0,
            score_communication=9.0,
            score_confidence=8.5,
            feedback="Excellent clear explanation of overfitting and standard regularization tools."
        )
        db.add(q1)
        db.commit()
        db.refresh(q1)
        print("Mock Q&A history added.")

        # 5. Test PDF Report Generation
        print("\n5. Testing PDF Report Generation...")
        session_data = {
            "candidate_name": session.candidate_name,
            "candidate_email": session.candidate_email,
            "target_role": session.target_role,
            "overall_score": 8.5,
            "tech_score": 8.5,
            "comp_score": 8.0,
            "comm_score": 9.0,
            "conf_score": 8.5,
            "feedback_summary": "The candidate has strong fundamentals in deep learning and Python script structures. Communication is crisp.",
            "improvement_plan": "1. Focus on understanding custom transformer scaling mechanisms.\n2. Study SQL index locks.",
            "date": "2026-06-18 16:30"
        }
        
        questions_list = [
            {
                "sequence_number": q1.sequence_number,
                "category": q1.category,
                "difficulty": q1.difficulty,
                "question_text": q1.question_text,
                "answer_text": q1.answer_text,
                "score_correctness": q1.score_correctness,
                "score_completeness": q1.score_completeness,
                "score_communication": q1.score_communication,
                "score_confidence": q1.score_confidence,
                "feedback": q1.feedback
            }
        ]

        report_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "reports")
        os.makedirs(report_dir, exist_ok=True)
        report_path = os.path.join(report_dir, "test_report.pdf")
        
        ReportGenerator.generate_pdf_report(session_data, questions_list, report_path)
        print(f"Mock PDF report successfully compiled at: {report_path}")
        print(f"File size: {os.path.getsize(report_path)} bytes")

    finally:
        db.close()
        
    print("\n=== All local modules successfully verified! ===")

if __name__ == "__main__":
    main()
