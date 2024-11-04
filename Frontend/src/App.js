// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CreateContest from './pages/CreateContest';
import ContestChallenges from './pages/ContestChallenges';
import ContestPage from './pages/ContestPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ContestPage />} />
        <Route path="/contest-challenges" element={<ContestChallenges />} />
        <Route path="/contest" element={<ContestPage />} />
      </Routes>
    </Router>
  );
}

export default App;
