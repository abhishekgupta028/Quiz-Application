import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getSession } from '../utils/api';
import './ResultPage.css';

export default function ResultPage() {
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getSession(sessionId)
      .then(r => setSession(r.data))
      .finally(() => setLoading(false));
  }, [sessionId]);

  if (loading) return <div className="page-loader"><div className="spinner" /></div>;
  if (!session) return <div className="page-loader"><p>Session not found.</p></div>;

  const score = session.score ?? 0;
  const correct = session.correct_answers ?? 0;
  const total = session.total_questions ?? 0;
  const avgTime = session.avg_response_time ?? 0;
  const answers = session.answers ?? [];

  const getScoreEmoji = (s) => {
    if (s >= 80) return '🏆';
    if (s >= 60) return '🎯';
    if (s >= 40) return '📚';
    return '💪';
  };
  const getScoreLabel = (s) => {
    if (s >= 80) return 'Excellent!';
    if (s >= 60) return 'Good Job!';
    if (s >= 40) return 'Keep Practicing!';
    return "Don't Give Up!";
  };
  const getScoreColor = (s) => {
    if (s >= 80) return 'var(--accent)';
    if (s >= 60) return '#00b4d8';
    if (s >= 40) return 'var(--amber)';
    return 'var(--rose)';
  };

  const circumference = 2 * Math.PI * 54;
  const dashOffset = circumference - (score / 100) * circumference;

  return (
    <div className="result-page">
      <div className="result-container fade-up">
        {/* Score card */}
        <div className="score-card">
          <div className="score-emoji">{getScoreEmoji(score)}</div>
          <h1 className="score-label">{getScoreLabel(score)}</h1>

          <div className="score-ring-wrapper">
            <svg className="score-ring" viewBox="0 0 120 120">
              <circle cx="60" cy="60" r="54" fill="none" stroke="var(--bg-elevated)" strokeWidth="8" />
              <circle
                cx="60" cy="60" r="54" fill="none"
                stroke={getScoreColor(score)} strokeWidth="8"
                strokeLinecap="round"
                strokeDasharray={circumference}
                strokeDashoffset={dashOffset}
                style={{ transform: 'rotate(-90deg)', transformOrigin: '50% 50%', transition: 'stroke-dashoffset 1s ease' }}
              />
            </svg>
            <div className="score-ring-text">
              <span className="score-pct" style={{ color: getScoreColor(score) }}>
                {Math.round(score)}%
              </span>
            </div>
          </div>

          <div className="score-stats">
            <div className="score-stat">
              <div className="score-stat-val" style={{ color: 'var(--accent)' }}>{correct}/{total}</div>
              <div className="score-stat-lbl">Correct</div>
            </div>
            <div className="score-stat-sep" />
            <div className="score-stat">
              <div className="score-stat-val">{(total - correct)}</div>
              <div className="score-stat-lbl">Wrong</div>
            </div>
            <div className="score-stat-sep" />
            <div className="score-stat">
              <div className="score-stat-val">{avgTime.toFixed(1)}s</div>
              <div className="score-stat-lbl">Avg Time</div>
            </div>
          </div>
        </div>

        {/* Answer review */}
        {answers.length > 0 && (
          <div className="review-section">
            <h2>Answer Review</h2>
            <div className="review-list">
              {answers.map((ans, i) => (
                <div key={i} className={`review-item ${ans.is_correct ? 'rev-correct' : 'rev-wrong'}`}>
                  <div className="review-num">Q{i + 1}</div>
                  <div className="review-indicator">
                    {ans.is_correct ? '✓' : '✗'}
                  </div>
                  <div className="review-time">
                    {ans.response_duration_seconds?.toFixed(1)}s
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="result-actions">
          <button
            className="btn btn-primary btn-lg"
            onClick={() => navigate('/')}
          >
            ⊞ Back to Exams
          </button>
          <button
            className="btn btn-secondary"
            onClick={() => navigate('/analytics')}
          >
            ◈ View Analytics
          </button>
        </div>
      </div>
    </div>
  );
}
