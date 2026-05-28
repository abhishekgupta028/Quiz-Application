import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getExams } from '../utils/api';
import { useUser } from '../App';
import './HomePage.css';

export default function HomePage() {
  const [exams, setExams] = useState([]);
  const [loading, setLoading] = useState(true);
  const { currentUser } = useUser();
  const navigate = useNavigate();

  useEffect(() => {
    getExams()
      .then(r => setExams(r.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) return (
    <div className="page-loader">
      <div className="spinner" />
    </div>
  );

  return (
    <div className="home-page">
      <div className="home-hero">
        <div className="hero-text">
          <span className="badge badge-accent">Welcome back</span>
          <h1>Hi, {currentUser?.name?.split(' ')[0]} 👋</h1>
          <p>Choose an exam to start practicing. Each quiz tracks your progress and time.</p>
        </div>
        <div className="hero-stats">
          <div className="hero-stat">
            <div className="hero-stat-val">{exams.length}</div>
            <div className="hero-stat-label">Exams</div>
          </div>
          <div className="hero-stat-divider" />
          <div className="hero-stat">
            <div className="hero-stat-val">∞</div>
            <div className="hero-stat-label">Questions</div>
          </div>
        </div>
      </div>

      <div className="section-header">
        <h2>Available Exams</h2>
        <span className="badge badge-accent">{exams.length} total</span>
      </div>

      <div className="exams-grid">
        {exams.map((exam, i) => (
          <div
            key={exam.id}
            className="exam-card card card-hover fade-up"
            style={{ animationDelay: `${i * 0.08}s`, '--card-color': exam.color }}
            onClick={() => navigate(`/exam/${exam.id}`)}
          >
            <div className="exam-card-icon">{exam.icon}</div>
            <div className="exam-card-body">
              <h3>{exam.title}</h3>
              <p>{exam.description}</p>
            </div>
            <div className="exam-card-arrow">→</div>
            <div className="exam-card-glow" />
          </div>
        ))}
      </div>
    </div>
  );
}
