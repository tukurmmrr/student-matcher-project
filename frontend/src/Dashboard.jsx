// frontend/src/components/Dashboard.jsx

import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'https://tukur-student-matcher-project.onrender.com';

function MatchList({ title, description, matches, badgeClass }) {
  return (
    <div className="card shadow-sm mb-4">
        <div className="card-body">
            <h3 className="card-title">{title}</h3>
            <p className="card-text text-muted">{description}</p>
            {matches.length > 0 ? (
                <ul className="list-group">
                {matches.map((match, index) => (
                    <li key={index} className="list-group-item d-flex justify-content-between align-items-center">
                        {/* This is the new, cleaner text display */}
                        {match.student1.name} ↔ {match.student2.name}
                        <span className={`badge ${badgeClass} rounded-pill`}>{match.score}</span>
                    </li>
                ))}
                </ul>
            ) : (
                <p>No matches found. Register more students to see results.</p>
            )}
        </div>
    </div>
  );
}

function Dashboard() {
  const [jaccardMatches, setJaccardMatches] = useState([]);
  const [cosineMatches, setCosineMatches] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMatches = async () => {
      setLoading(true);
      try {
        const jaccardRes = await axios.get(`${API_URL}/matches/jaccard`);
        const cosineRes = await axios.get(`${API_URL}/matches/cosine`);
        setJaccardMatches(jaccardRes.data);
        setCosineMatches(cosineRes.data);
      } catch (error) {
        console.error("Failed to fetch matches:", error);
      }
      setLoading(false);
    };

    fetchMatches();
  }, []);

  if (loading) {
    return <div className="text-center"><h4>Loading matches...</h4></div>;
  }

  return (
    <div>
      <h2 className="text-center mb-4">Matching Algorithm Comparison</h2>
      <a href="/frontend/public" className="btn btn-secondary mb-4">Register Another Student</a>
      <div className="row">
        <div className="col-lg-6">
          <MatchList
            title="Algorithm 1: Jaccard Similarity"
            description="Measures simple overlap and course."
            matches={jaccardMatches}
            badgeClass="bg-primary"
          />
        </div>
        <div className="col-lg-6">
          <MatchList
            title="Algorithm 2: Cosine Similarity (TF-IDF)"
            description="Finds similar taste by weighing rare interests and course."
            matches={cosineMatches}
            badgeClass="bg-success"
          />
        </div>
      </div>
    </div>
  );
}

export default Dashboard;