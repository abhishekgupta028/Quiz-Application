import React, { useState, useEffect, createContext, useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import './styles/global.css';

import Layout from './components/layout/Layout';
import HomePage from './pages/HomePage';
import ExamPage from './pages/ExamPage';
import SubjectsPage from './pages/SubjectsPage';
import ChaptersPage from './pages/ChaptersPage';
import QuizPage from './pages/QuizPage';
import ResultPage from './pages/ResultPage';
import AnalyticsPage from './pages/AnalyticsPage';
import UserSelectPage from './pages/UserSelectPage';

export const UserContext = createContext(null);
export const useUser = () => useContext(UserContext);

function App() {
  const [currentUser, setCurrentUser] = useState(() => {
    const saved = localStorage.getItem('skillbytes_user');
    return saved ? JSON.parse(saved) : null;
  });

  const setUser = (user) => {
    setCurrentUser(user);
    if (user) localStorage.setItem('skillbytes_user', JSON.stringify(user));
    else localStorage.removeItem('skillbytes_user');
  };

  return (
    <UserContext.Provider value={{ currentUser, setUser }}>
      <Router>
        <Toaster
          position="top-right"
          toastOptions={{
            style: {
              background: '#111827',
              color: '#f0f4ff',
              border: '1px solid #1f2d42',
              fontFamily: "'DM Sans', sans-serif",
            },
            success: { iconTheme: { primary: '#00d9a6', secondary: '#0a0e1a' } },
            error: { iconTheme: { primary: '#f43f5e', secondary: '#0a0e1a' } },
          }}
        />
        <Routes>
          <Route path="/select-user" element={<UserSelectPage />} />
          <Route
            path="/*"
            element={
              currentUser ? (
                <Layout>
                  <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/exams" element={<HomePage />} />
                    <Route path="/exam/:examId" element={<ExamPage />} />
                    <Route path="/exam/:examId/subject/:subjectId" element={<SubjectsPage />} />
                    <Route path="/exam/:examId/subject/:subjectId/chapter/:chapterId" element={<ChaptersPage />} />
                    <Route path="/quiz/:sessionId" element={<QuizPage />} />
                    <Route path="/result/:sessionId" element={<ResultPage />} />
                    <Route path="/analytics" element={<AnalyticsPage />} />
                    <Route path="*" element={<Navigate to="/" />} />
                  </Routes>
                </Layout>
              ) : (
                <Navigate to="/select-user" replace />
              )
            }
          />
        </Routes>
      </Router>
    </UserContext.Provider>
  );
}

export default App;
