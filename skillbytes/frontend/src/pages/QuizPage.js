import React, { useEffect, useState, useRef, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getCurrentQuestion, submitAnswer, completeQuiz, abandonQuiz } from '../utils/api';
import { useUser } from '../App';
import toast from 'react-hot-toast';
import './QuizPage.css';

export default function QuizPage() {
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const { currentUser } = useUser();

  const [questionData, setQuestionData] = useState(null);
  const [selected, setSelected] = useState(null);
  const [submitted, setSubmitted] = useState(false);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [elapsed, setElapsed] = useState(0);
  const [messages, setMessages] = useState([]);

  const shownAtRef = useRef(null);
  const timerRef = useRef(null);

  const loadQuestion = useCallback(async () => {
    setLoading(true);
    setSelected(null);
    setSubmitted(false);
    setResult(null);
    setElapsed(0);
    clearInterval(timerRef.current);
    try {
      const res = await getCurrentQuestion(sessionId);
      if (res.data.status === 'completed') {
        navigate(`/result/${sessionId}`);
        return;
      }
      shownAtRef.current = new Date(res.data.shown_at);
      setQuestionData(res.data);
      // Start timer
      timerRef.current = setInterval(() => {
        setElapsed(e => e + 1);
      }, 1000);
    } catch {
      toast.error('Failed to load question');
    } finally {
      setLoading(false);
    }
  }, [sessionId, navigate]);

  useEffect(() => {
    loadQuestion();
    return () => clearInterval(timerRef.current);
  }, [loadQuestion]);

  const handleSelect = (optionId) => {
    if (submitted) return;
    setSelected(optionId);
  };

  const handleSubmit = async () => {
    if (!selected || submitting) return;
    setSubmitting(true);
    clearInterval(timerRef.current);
    const submittedAt = new Date();
    try {
      const res = await submitAnswer({
        session_id: sessionId,
        question_id: questionData.question.id,
        selected_option_id: selected,
        question_shown_at: shownAtRef.current.toISOString(),
        answer_submitted_at: submittedAt.toISOString(),
      });
      setResult(res.data);
      setSubmitted(true);

      // Add feedback message
      const feedbackMsg = {
        id: Date.now(),
        type: 'feedback',
        isCorrect: res.data.is_correct,
        explanation: res.data.explanation,
        correctId: res.data.correct_option_id,
        duration: res.data.response_duration_seconds,
      };
      setMessages(prev => [...prev, feedbackMsg]);
    } catch {
      toast.error('Failed to submit answer');
    } finally {
      setSubmitting(false);
    }
  };

  const handleNext = async () => {
    const { next_question_index, total_questions } = result;
    if (next_question_index >= total_questions) {
      // Complete the quiz
      try {
        await completeQuiz({
          session_id: sessionId,
          completed_at: new Date().toISOString(),
        });
        navigate(`/result/${sessionId}`);
      } catch {
        toast.error('Failed to complete quiz');
      }
    } else {
      loadQuestion();
    }
  };

  const handleAbandon = async () => {
    if (!window.confirm('Are you sure you want to quit this quiz?')) return;
    try {
      await abandonQuiz(sessionId, currentUser.id);
      navigate('/');
    } catch {
      navigate('/');
    }
  };

  const formatTime = (s) => {
    const m = Math.floor(s / 60);
    const sec = s % 60;
    return m > 0 ? `${m}:${String(sec).padStart(2, '0')}` : `${sec}s`;
  };

  if (loading) return (
    <div className="quiz-loading">
      <div className="spinner" />
      <p>Loading question…</p>
    </div>
  );

  const { question, question_number, total_questions } = questionData || {};
  const progress = ((question_number - 1) / total_questions) * 100;
  const isLast = result && result.next_question_index >= total_questions;

  return (
    <div className="quiz-page">
      {/* Header */}
      <div className="quiz-header">
        <button className="quiz-quit-btn" onClick={handleAbandon}>✕ Quit</button>
        <div className="quiz-progress-area">
          <div className="quiz-progress-label">
            Question {question_number} of {total_questions}
          </div>
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${progress}%` }} />
          </div>
        </div>
        <div className={`quiz-timer ${elapsed > 30 ? 'timer-warn' : ''}`}>
          ⏱ {formatTime(elapsed)}
        </div>
      </div>

      {/* Chat area */}
      <div className="quiz-chat">
        {/* Question bubble */}
        <div className="quiz-q-number">
          <span className="badge badge-accent">Q{question_number}</span>
        </div>

        <div className="chat-bubble chat-bot fade-up">
          <div className="bot-avatar">🤖</div>
          <div className="bubble-content">
            <p className="question-text">{question?.text}</p>
            {question?.difficulty && (
              <span className={`diff-badge diff-${question.difficulty}`}>
                {question.difficulty}
              </span>
            )}
          </div>
        </div>

        {/* Options */}
        <div className="options-area fade-up">
          {question?.options.map((opt) => {
            let cls = 'option-btn';
            if (selected === opt.id) cls += ' option-selected';
            if (submitted) {
              if (opt.id === result?.correct_option_id) cls += ' option-correct';
              else if (opt.id === selected && !result?.is_correct) cls += ' option-wrong';
              else cls += ' option-dim';
            }
            return (
              <button
                key={opt.id}
                className={cls}
                onClick={() => handleSelect(opt.id)}
                disabled={submitted}
              >
                <span className="option-letter">{opt.id.toUpperCase()}</span>
                <span className="option-text">{opt.text}</span>
                {submitted && opt.id === result?.correct_option_id && (
                  <span className="option-check">✓</span>
                )}
                {submitted && opt.id === selected && !result?.is_correct && (
                  <span className="option-x">✗</span>
                )}
              </button>
            );
          })}
        </div>

        {/* Feedback after submission */}
        {submitted && result && (
          <div className={`feedback-bubble fade-up ${result.is_correct ? 'feedback-correct' : 'feedback-wrong'}`}>
            <div className="feedback-header">
              <span className="feedback-icon">{result.is_correct ? '🎉' : '💡'}</span>
              <strong>{result.is_correct ? 'Correct!' : 'Not quite!'}</strong>
              <span className="feedback-time">
                ⏱ {result.response_duration_seconds?.toFixed(1)}s
              </span>
            </div>
            {result.explanation && (
              <p className="feedback-explanation">{result.explanation}</p>
            )}
          </div>
        )}

        {/* Previous feedback messages */}
        {messages.slice(0, -1).map((msg) => (
          <div key={msg.id} className={`feedback-bubble ${msg.isCorrect ? 'feedback-correct' : 'feedback-wrong'} fade-in`}>
            <div className="feedback-header">
              <span className="feedback-icon">{msg.isCorrect ? '✓' : '✗'}</span>
              <strong>{msg.isCorrect ? 'Correct' : 'Incorrect'}</strong>
            </div>
          </div>
        ))}
      </div>

      {/* Action bar */}
      <div className="quiz-action-bar">
        {!submitted ? (
          <button
            className="btn btn-primary"
            style={{ flex: 1, justifyContent: 'center' }}
            onClick={handleSubmit}
            disabled={!selected || submitting}
          >
            {submitting ? 'Submitting…' : 'Submit Answer →'}
          </button>
        ) : (
          <button
            className="btn btn-primary"
            style={{ flex: 1, justifyContent: 'center' }}
            onClick={handleNext}
          >
            {isLast ? '🏁 Finish Quiz' : 'Next Question →'}
          </button>
        )}
      </div>
    </div>
  );
}
