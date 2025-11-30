import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import TrendingPage from './pages/TrendingPage';
import SearchPage from './pages/SearchPage';
import LogPage from './pages/Logpage';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <Routes>
          <Route path="/" element={<TrendingPage />} />
          <Route path="/search" element={<SearchPage />} />
          <Route path="/log" element={<LogPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;