import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getExam, getSubjects } from '../utils/api';
import './ExamPage.css';

export default function ExamPage() {
  const { examId } = useParams();
  const navigate = useNavigate();
  const [exam, setExam] = useState(null);
  const [subjects, setSubjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getExam(examId), getSubjects(examId)])
      .then(([eRes, sRes]) => {
        setExam(eRes.data);
        setSubjects(sRes.data);
      })
      .finally(() => setLoading(false));
  }, [examId]);

  if (loading) return <div className="page-loader"><div className="spinner" /></div>;

  return (
    <div className="exam-page">
      <button className="back-btn" onClick={() => navigate('/')}>
        ← Back to Exams
      </button>

      <div className="exam-hero fade-up">
        <div className="exam-hero-icon">{exam?.icon}</div>
        <div>
          <h1>{exam?.title}</h1>
          <p>{exam?.description}</p>
        </div>
      </div>

      <div className="section-header">
        <h2>Subjects</h2>
        <span className="badge badge-accent">{subjects.length} subjects</span>
      </div>

      <div className="subjects-grid">
        {subjects.map((subject, i) => (
          <div
            key={subject.id}
            className="subject-card card card-hover fade-up"
            style={{ animationDelay: `${i * 0.07}s` }}
            onClick={() => navigate(`/exam/${examId}/subject/${subject.id}`)}
          >
            <div className="subject-icon">{subject.icon}</div>
            <div className="subject-body">
              <h3>{subject.title}</h3>
              <p>{subject.description}</p>
            </div>
            <div className="subject-arrow">→</div>
          </div>
        ))}
      </div>
    </div>
  );
}
