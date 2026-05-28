import React, { useEffect, useState } from 'react';
import {
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from 'recharts';
import { getDashboard } from '../utils/api';
import './AnalyticsPage.css';

const COLORS = ['#00d9a6', '#6c63ff', '#f59e0b', '#f43f5e', '#00b4d8'];

const StatCard = ({ label, value, sub, icon, color }) => (
  <div className="stat-card card fade-up">
    <div className="stat-card-top">
      <div className="stat-icon" style={{ color }}>{icon}</div>
      <div className="stat-val" style={{ color }}>{value}</div>
    </div>
    <div className="stat-label">{label}</div>
    {sub && <div className="stat-sub">{sub}</div>}
  </div>
);

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div className="chart-tooltip">
      <div className="tooltip-label">{label}</div>
      {payload.map((p, i) => (
        <div key={i} className="tooltip-item" style={{ color: p.color }}>
          <span>{p.name}:</span> <strong>{typeof p.value === 'number' ? p.value.toLocaleString() : p.value}</strong>
        </div>
      ))}
    </div>
  );
};

export default function AnalyticsPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    getDashboard()
      .then(r => setData(r.data))
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return (
    <div className="analytics-loader">
      <div className="spinner" />
      <p>Loading analytics…</p>
    </div>
  );

  if (error || !data) return (
    <div className="analytics-loader">
      <p style={{ color: 'var(--rose)' }}>Failed to load analytics. Is the backend running?</p>
    </div>
  );

  const dropoffData = [
    { name: 'Started', value: data.total_started || 0 },
    { name: 'Completed', value: data.total_completed || 0 },
    { name: 'Abandoned', value: data.total_abandoned || 0 },
  ];

  const peakData = (data.peak_hours || []).map(h => ({
    hour: `${h.hour}:00`,
    activity: h.count,
  }));

  const dailyData = (data.daily_activity || []).map(d => ({
    date: d.date?.slice(5),
    quizzes: d.quizzes,
  }));

  const scoreData = data.score_distribution || [];

  return (
    <div className="analytics-page">
      <div className="analytics-header">
        <div>
          <h1>Analytics Dashboard</h1>
          <p>Real-time quiz engagement and performance metrics</p>
        </div>
        <span className="badge badge-accent">Live Data</span>
      </div>

      {/* KPI Cards */}
      <div className="stats-grid">
        <StatCard label="Daily Active Users" value={data.dau} icon="👥" color="var(--accent)" />
        <StatCard label="Weekly Active Users" value={data.wau} icon="📅" color="#00b4d8" />
        <StatCard label="Questions Served" value={data.questions_served?.toLocaleString()} icon="❓" color="var(--accent-2)" />
        <StatCard label="Questions Answered" value={data.questions_answered?.toLocaleString()} icon="✅" color="var(--amber)" />
        <StatCard
          label="Avg Response Time"
          value={`${data.avg_response_time?.toFixed(1)}s`}
          icon="⏱"
          color="var(--rose)"
        />
        <StatCard
          label="Completion Rate"
          value={`${data.completion_rate}%`}
          sub={`${data.total_completed} of ${data.total_started} quizzes`}
          icon="🏁"
          color="var(--accent)"
        />
        <StatCard
          label="Avg Questions / Session"
          value={data.avg_questions_per_session}
          icon="📋"
          color="var(--accent-2)"
        />
        <StatCard
          label="Abandoned Quizzes"
          value={data.total_abandoned}
          icon="⚠️"
          color="var(--amber)"
        />
      </div>

      {/* Charts row 1 */}
      <div className="charts-row">
        {/* Daily Activity */}
        <div className="chart-card card">
          <h3>Daily Quiz Activity (Last 14 Days)</h3>
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={dailyData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1f2d42" />
              <XAxis dataKey="date" tick={{ fill: '#8b9bb4', fontSize: 11 }} />
              <YAxis tick={{ fill: '#8b9bb4', fontSize: 11 }} />
              <Tooltip content={<CustomTooltip />} />
              <Line
                type="monotone" dataKey="quizzes" name="Quizzes"
                stroke="#00d9a6" strokeWidth={2.5}
                dot={{ fill: '#00d9a6', r: 3 }}
                activeDot={{ r: 5, fill: '#00d9a6' }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Drop-off */}
        <div className="chart-card card">
          <h3>Quiz Drop-off Analysis</h3>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={dropoffData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1f2d42" />
              <XAxis dataKey="name" tick={{ fill: '#8b9bb4', fontSize: 12 }} />
              <YAxis tick={{ fill: '#8b9bb4', fontSize: 11 }} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="value" name="Sessions" radius={[6, 6, 0, 0]}>
                {dropoffData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Charts row 2 */}
      <div className="charts-row">
        {/* Peak Hours */}
        <div className="chart-card card">
          <h3>Peak Activity Hours</h3>
          {peakData.length === 0 ? (
            <div className="chart-empty">No activity data yet</div>
          ) : (
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={peakData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1f2d42" />
                <XAxis dataKey="hour" tick={{ fill: '#8b9bb4', fontSize: 10 }} interval={2} />
                <YAxis tick={{ fill: '#8b9bb4', fontSize: 11 }} />
                <Tooltip content={<CustomTooltip />} />
                <Bar dataKey="activity" name="Events" fill="#6c63ff" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>

        {/* Score Distribution */}
        <div className="chart-card card">
          <h3>Score Distribution</h3>
          <div className="pie-row">
            <ResponsiveContainer width="55%" height={200}>
              <PieChart>
                <Pie
                  data={scoreData} cx="50%" cy="50%"
                  innerRadius={55} outerRadius={80}
                  paddingAngle={3}
                  dataKey="count" nameKey="range"
                >
                  {scoreData.map((_, i) => (
                    <Cell key={i} fill={COLORS[i % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip content={<CustomTooltip />} />
              </PieChart>
            </ResponsiveContainer>
            <div className="pie-legend">
              {scoreData.map((item, i) => (
                <div key={i} className="pie-legend-item">
                  <div className="pie-legend-dot" style={{ background: COLORS[i % COLORS.length] }} />
                  <span className="pie-legend-label">{item.range}</span>
                  <span className="pie-legend-val">{item.count}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Funnel */}
      <div className="funnel-card card">
        <h3>Quiz Completion Funnel</h3>
        <div className="funnel">
          {dropoffData.map((step, i) => {
            const pct = data.total_started > 0
              ? Math.round((step.value / data.total_started) * 100)
              : 0;
            const w = Math.max(pct, 10);
            return (
              <div key={i} className="funnel-step">
                <div className="funnel-label">{step.name}</div>
                <div className="funnel-bar-wrap">
                  <div
                    className="funnel-bar"
                    style={{ width: `${w}%`, background: COLORS[i] }}
                  />
                </div>
                <div className="funnel-val">{step.value} <span>({pct}%)</span></div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
