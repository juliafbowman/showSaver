import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Film, Search, BookMarked } from 'lucide-react';
import './Header.css';

const Header = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/search?query=${encodeURIComponent(searchQuery)}`);
      setSearchQuery(''); // Clear search after submitting
    }
  };

  const handleLogoClick = () => {
    navigate('/');
  };

  const handleLogClick = () => {
    navigate('/log');
  };

  return (
    <header className="app-header">
      <div className="header-container">
        {/* Logo/Brand */}
        <div className="header-logo" onClick={handleLogoClick}>
          <Film size={32} className="logo-icon" />
          <h1 className="logo-text">Show Saver</h1>
        </div>

        {/* Search Bar */}
        <form className="search-form" onSubmit={handleSearchSubmit}>
          <div className="search-wrapper">
            <Search size={20} className="search-icon" />
            <input
              type="text"
              className="search-input"
              placeholder="Search movies & TV shows..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button type="submit" className="search-button">
              Search
            </button>
          </div>
        </form>

        {/* Log Link */}
        <button className="log-link" onClick={handleLogClick}>
          <BookMarked size={20} />
          <span>My Log</span>
        </button>
      </div>
    </header>
  );
};

export default Header;