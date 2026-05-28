import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getChapters, getExam, getSubjects, startQuiz } from '../utils/api';
import { useUser } from '../App';
import toast from 'react-hot-toast';
import './ChaptersPage.css';

export default function ChaptersPage() {
  const { examId, subjectId, chapterId } = useParams();
  const navigate = useNavigate();
  const { currentUser } = useUser();
  const [exam, setExam] = useState(null);
  const [subject, setSubject] = useState(null);
  const [chapter, setChapter] = useState(null);
  const [loading, setLoading] = useState(true);
  const [starting, setStarting] = useState(false);

  useEffect(() => {
    Promise.all([
      getExam(examId),
      getSubjects(examId),
      getChapters(subjectId)
    ]).then(([eRes, sRes, cRes]) => {
      setExam(eRes.data);
      setSubject(sRes.data.find(s => s.id === subjectId));
      setChapter(cRes.data.find(c => c.id === chapterId));
    }).finally(() => setLoading(false));
  }, [examId, subjectId, chapterId]);

  const handleStart = async () => {
    setStarting(true);
    try {
      const res = await startQuiz({
        user_id: currentUser.id,
        exam_id: examId,
        subject_id: subjectId,
        chapter_id: chapterId,
      });
      navigate(`/quiz/${res.data.id}`);
    } catch (err) {
      toast.error('Failed to start quiz. Please try again.');
    } finally {
      setStarting(false);
    }
  };

  if (loading) return <div className="page-loader"><div className="spinner" /></div>;
  if (!chapter) return <div className="page-loader"><p style={{ color: 'var(--text-secondary)' }}>Chapter not found.</p></div>;

  return (
    <div className="chapters-page">
      <div className="breadcrumb">
        <button onClick={() => navigate('/')}>Exams</button>
        <span>›</span>
        <button onClick={() => navigate(`/exam/${examId}`)}>{exam?.title}</button>
        <span>›</span>
        <button onClick={() => navigate(`/exam/${examId}/subject/${subjectId}`)}>{subject?.title}</button>
        <span>›</span>
        <span className="breadcrumb-active">{chapter.title}</span>
      </div>

      <div className="quiz-start-card fade-up">
        <div className="quiz-start-top">
          <div className="quiz-start-icon">📝</div>
          <div className="quiz-start-labels">
            <span className="badge badge-accent">{exam?.title}</span>
            <span className="badge badge-purple">{subject?.title}</span>
          </div>
        </div>

        <h1>{chapter.title}</h1>
        <p className="chapter-desc">{chapter.description}</p>

        <div className="quiz-rules">
          <h3>Quiz Rules</h3>
          <div className="rules-grid">
            <div className="rule-item">
              <span className="rule-icon">☑</span>
              <div>
                <strong>Multiple Choice</strong>
                <p>Each question has one correct answer</p>
              </div>
            </div>
            <div className="rule-item">
              <span className="rule-icon">⏱</span>
              <div>
                <strong>Time Tracked</strong>
                <p>Response time is recorded per question</p>
              </div>
            </div>
            <div className="rule-item">
              <span className="rule-icon">✓</span>
              <div>
                <strong>No Negative Marking</strong>
                <p>Wrong answers don't deduct points</p>
              </div>
            </div>
            <div className="rule-item">
              <span className="rule-icon">◎</span>
              <div>
                <strong>One by One</strong>
                <p>Questions appear sequentially</p>
              </div>
            </div>
          </div>
        </div>

        <div className="quiz-start-actions">
          <button
            className="btn btn-primary btn-lg"
            onClick={handleStart}
            disabled={starting}
          >
            {starting ? (
              <><span className="btn-spinner" />Starting…</>
            ) : (
              <>⚡ Start Quiz</>
            )}
          </button>
          <button
            className="btn btn-ghost"
            onClick={() => navigate(`/exam/${examId}/subject/${subjectId}`)}
          >
            Go Back
          </button>
        </div>
      </div>
    </div>
  );
}
