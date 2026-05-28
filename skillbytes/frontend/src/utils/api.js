import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({ baseURL: API_BASE });

// Exams
export const getExams = () => api.get('/exams/');
export const getExam = (id) => api.get(`/exams/${id}`);

// Subjects
export const getSubjects = (examId) => api.get('/subjects/', { params: { exam_id: examId } });

// Chapters
export const getChapters = (subjectId) => api.get('/chapters/', { params: { subject_id: subjectId } });

// Quiz
export const startQuiz = (data) => api.post('/quiz/start', data);
export const getSession = (sessionId) => api.get(`/quiz/session/${sessionId}`);
export const getCurrentQuestion = (sessionId) => api.get(`/quiz/session/${sessionId}/question`);
export const submitAnswer = (data) => api.post('/quiz/answer', data);
export const completeQuiz = (data) => api.post('/quiz/complete', data);
export const abandonQuiz = (sessionId, userId) => api.post(`/quiz/abandon/${sessionId}`, null, { params: { user_id: userId } });
export const getUserHistory = (userId) => api.get(`/quiz/history/${userId}`);

// Analytics
export const getDashboard = () => api.get('/analytics/dashboard');

// Seed
export const seedDatabase = () => api.post('/seed/');
export const getUsers = () => api.get('/seed/users');

export default api;
