import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../App';
import { getUsers, seedDatabase } from '../utils/api';
import toast from 'react-hot-toast';
import './UserSelectPage.css';

export default function UserSelectPage() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [seeding, setSeeding] = useState(false);
  const { setUser } = useUser();
  const navigate = useNavigate();

  useEffect(() => { fetchUsers(); }, []);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const res = await getUsers();
      setUsers(res.data);
    } catch {
      setUsers([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSeed = async () => {
    setSeeding(true);
    try {
      await seedDatabase();
      toast.success('Database seeded with demo data!');
      await fetchUsers();
    } catch {
      toast.error('Failed to seed — is the backend running?');
    } finally {
      setSeeding(false);
    }
  };

  const handleSelect = (user) => {
    setUser(user);
    navigate('/');
  };

  return (
    <div className="user-select-page">
      <div className="user-select-bg" />
      <div className="user-select-container fade-up">
        <div className="user-select-header">
          <div className="brand-mark">⬡</div>
          <h1>SkillBytes</h1>
          <p>Select your profile to continue</p>
        </div>

        {loading ? (
          <div className="centered-loader">
            <div className="spinner" />
            <span>Connecting to backend…</span>
          </div>
        ) : users.length === 0 ? (
          <div className="no-users">
            <div className="no-users-icon">🗄️</div>
            <h3>No users found</h3>
            <p>Seed the database to get started with demo data</p>
            <button
              className="btn btn-primary btn-lg"
              onClick={handleSeed}
              disabled={seeding}
            >
              {seeding ? 'Seeding…' : '✦ Seed Demo Data'}
            </button>
          </div>
        ) : (
          <>
            <div className="users-grid">
              {users.map((user, i) => (
                <button
                  key={user.id}
                  className="user-option fade-up"
                  style={{ animationDelay: `${i * 0.06}s` }}
                  onClick={() => handleSelect(user)}
                >
                  <div className="user-option-avatar">{user.avatar}</div>
                  <div className="user-option-name">{user.name}</div>
                  <div className="user-option-email">{user.email}</div>
                </button>
              ))}
            </div>
            <div className="reseed-row">
              <button className="btn btn-ghost btn-sm" onClick={handleSeed} disabled={seeding}>
                {seeding ? 'Seeding…' : '↻ Reseed Database'}
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
