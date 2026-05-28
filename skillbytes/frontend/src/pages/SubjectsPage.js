import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getChapters, getSubjects, getExam } from '../utils/api';
import './SubjectsPage.css';

export default function SubjectsPage() {
  const { examId, subjectId } = useParams();
  const navigate = useNavigate();
  const [exam, setExam] = useState(null);
  const [subject, setSubject] = useState(null);
  const [chapters, setChapters] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      getExam(examId),
      getSubjects(examId),
      getChapters(subjectId)
    ]).then(([eRes, sRes, cRes]) => {
      setExam(eRes.data);
      setSubject(sRes.data.find(s => s.id === subjectId));
      setChapters(cRes.data);
    }).finally(() => setLoading(false));
  }, [examId, subjectId]);

  if (loading) return <div className="page-loader"><div className="spinner" /></div>;

  return (
    <div className="subjects-page">
      <div className="breadcrumb">
        <button onClick={() => navigate('/')}>Exams</button>
        <span>›</span>
        <button onClick={() => navigate(`/exam/${examId}`)}>{exam?.title}</button>
        <span>›</span>
        <span className="breadcrumb-active">{subject?.title}</span>
      </div>

      <div className="subject-hero fade-up">
        <div className="subject-hero-icon">{subject?.icon}</div>
        <div>
          <h1>{subject?.title}</h1>
          <p>{subject?.description}</p>
        </div>
      </div>

      <div className="section-header">
        <h2>Chapters</h2>
        <span className="badge badge-purple">{chapters.length} chapters</span>
      </div>

      {chapters.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📂</div>
          <h3>No chapters yet</h3>
          <p>Chapters for this subject haven't been added yet.</p>
        </div>
      ) : (
        <div className="chapters-list">
          {chapters.map((chapter, i) => (
            <div
              key={chapter.id}
              className="chapter-row card card-hover fade-up"
              style={{ animationDelay: `${i * 0.06}s` }}
              onClick={() => navigate(`/exam/${examId}/subject/${subjectId}/chapter/${chapter.id}`)}
            >
              <div className="chapter-order">{String(chapter.order).padStart(2, '0')}</div>
              <div className="chapter-info">
                <h3>{chapter.title}</h3>
                <p>{chapter.description}</p>
              </div>
              <div className="chapter-cta">
                <span className="badge badge-accent">Start Quiz</span>
                <span className="chapter-arrow">→</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
