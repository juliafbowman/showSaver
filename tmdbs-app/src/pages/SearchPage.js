import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Film, Search, Plus, Check } from 'lucide-react';
import './SearchPage.css';

const SearchPage = () => {
  const [searchParams] = useSearchParams();
  const query = searchParams.get('query');
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [addedItems, setAddedItems] = useState({}); // Track which items have been added

  const API_KEY = 'ab8ae844d4eb13ff70fb0ae9e0a97226';
  const BASE_URL = 'https://api.themoviedb.org/3';
  const IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500';
  const BACKEND_URL = 'http://127.0.0.1:5000';

  useEffect(() => {
    if (query) {
      searchMoviesAndShows(query);
    }
  }, [query]);

  const searchMoviesAndShows = async (searchQuery) => {
    try {
      setLoading(true);
      
      // Search for movies and TV shows
      const response = await fetch(
        `${BASE_URL}/search/multi?api_key=${API_KEY}&query=${encodeURIComponent(searchQuery)}`
      );
      const data = await response.json();
      
      // Filter to only include movies and TV shows (exclude people)
      const filtered = data.results.filter(
        item => item.media_type === 'movie' || item.media_type === 'tv'
      );
      
      setSearchResults(filtered || []);
      setLoading(false);
    } catch (error) {
      console.error('Error searching:', error);
      setLoading(false);
    }
  };

  // Add item to log via backend
  const handleAddToLog = async (id, type) => {
    // Immediately update UI for better UX
    const itemKey = `${type}-${id}`;
    setAddedItems(prev => ({ ...prev, [itemKey]: true }));
    
    try {
      const response = await fetch(
        `${BACKEND_URL}/api/db/import?id=${id}&type=${type}`
      );
      const data = await response.json();
      
      if (data.status === 'imported') {
        console.log(`Added ${type} with ID ${id} to log`);
      } else {
        // If import failed, revert the UI
        setAddedItems(prev => {
          const newState = { ...prev };
          delete newState[itemKey];
          return newState;
        });
      }
    } catch (error) {
      console.error('Error adding to log:', error);
      // Revert UI on error
      setAddedItems(prev => {
        const newState = { ...prev };
        delete newState[itemKey];
        return newState;
      });
    }
  };

  const ResultCard = ({ item }) => {
    const itemKey = `${item.media_type}-${item.id}`;
    const isAdded = addedItems[itemKey];

    return (
      <div className="result-card">
        <div className="result-poster-container">
          {item.poster_path ? (
            <img
              src={`${IMAGE_BASE_URL}${item.poster_path}`}
              alt={item.title || item.name}
              className="result-poster"
            />
          ) : (
            <div className="result-poster-placeholder">
              <Film size={48} className="placeholder-icon" />
            </div>
          )}
          <div className="result-type-badge">
            {item.media_type === 'movie' ? 'Movie' : 'TV Show'}
          </div>
        </div>
        <div className="result-info">
          <h3 className="result-title">
            {item.title || item.name}
          </h3>
          <p className="result-date">
            {item.media_type === 'movie' ? item.release_date : item.first_air_date}
          </p>
          {item.vote_average > 0 && (
            <p className="result-rating">
              ⭐ {item.vote_average.toFixed(1)}/10
            </p>
          )}
          <p className="result-overview">
            {item.overview || 'No description available.'}
          </p>
        </div>
        
        {/* Add to Log Button */}
        <button
          className={`add-to-log-btn ${isAdded ? 'added' : ''}`}
          onClick={() => handleAddToLog(item.id, item.media_type)}
          disabled={isAdded}
          title={isAdded ? 'Added to log' : 'Add to log'}
        >
          {isAdded ? (
            <>
              <Check size={18} />
              <span>Added</span>
            </>
          ) : (
            <>
              <Plus size={18} />
              <span>Add to Log</span>
            </>
          )}
        </button>
      </div>
    );
  };

  return (
    <div className="search-page-container">
      <main className="search-content">
        <div className="search-header">
          <div className="search-title-section">
            <Search size={32} className="icon-red" />
            <div>
              <h1 className="search-page-title">Search Results</h1>
              {query && (
                <p className="search-query">
                  Showing results for: <span className="query-text">"{query}"</span>
                </p>
              )}
            </div>
          </div>
        </div>

        {loading ? (
          <div className="loading-container">
            <div className="loading-content">
              <div className="loading-spinner"></div>
              <p className="loading-text">Searching...</p>
            </div>
          </div>
        ) : searchResults.length > 0 ? (
          <div className="results-list">
            {searchResults.map((item) => (
              <ResultCard key={`${item.media_type}-${item.id}`} item={item} />
            ))}
          </div>
        ) : query ? (
          <div className="no-results">
            <Film size={64} className="no-results-icon" />
            <h2>No Results Found</h2>
            <p>Try searching with different keywords</p>
          </div>
        ) : (
          <div className="no-results">
            <Search size={64} className="no-results-icon" />
            <h2>Start Searching</h2>
            <p>Use the search bar above to find movies and TV shows</p>
          </div>
        )}
      </main>
    </div>
  );
};

export default SearchPage;



// import React, { useState, useEffect } from 'react';
// import { useSearchParams } from 'react-router-dom';
// import { Film, Search } from 'lucide-react';
// import './SearchPage.css';

// const SearchPage = () => {
//   const [searchParams] = useSearchParams();
//   const query = searchParams.get('query');
//   const [searchResults, setSearchResults] = useState([]);
//   const [loading, setLoading] = useState(false);

//   const API_KEY = 'ab8ae844d4eb13ff70fb0ae9e0a97226';
//   const BASE_URL = 'https://api.themoviedb.org/3';
//   const IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500';

//   useEffect(() => {
//     if (query) {
//       searchMoviesAndShows(query);
//     }
//   }, [query]);

//   const searchMoviesAndShows = async (searchQuery) => {
//     try {
//       setLoading(true);
      
//       // Search for movies and TV shows
//       const response = await fetch(
//         `${BASE_URL}/search/multi?api_key=${API_KEY}&query=${encodeURIComponent(searchQuery)}`
//       );
//       const data = await response.json();
      
//       // Filter to only include movies and TV shows (exclude people)
//       const filtered = data.results.filter(
//         item => item.media_type === 'movie' || item.media_type === 'tv'
//       );
      
//       setSearchResults(filtered || []);
//       setLoading(false);
//     } catch (error) {
//       console.error('Error searching:', error);
//       setLoading(false);
//     }
//   };

//   const ResultCard = ({ item }) => (
//     <div className="result-card">
//       <div className="result-poster-container">
//         {item.poster_path ? (
//           <img
//             src={`${IMAGE_BASE_URL}${item.poster_path}`}
//             alt={item.title || item.name}
//             className="result-poster"
//           />
//         ) : (
//           <div className="result-poster-placeholder">
//             <Film size={48} className="placeholder-icon" />
//           </div>
//         )}
//         <div className="result-type-badge">
//           {item.media_type === 'movie' ? 'Movie' : 'TV Show'}
//         </div>
//       </div>
//       <div className="result-info">
//         <h3 className="result-title">
//           {item.title || item.name}
//         </h3>
//         <p className="result-date">
//           {item.media_type === 'movie' ? item.release_date : item.first_air_date}
//         </p>
//         {item.vote_average > 0 && (
//           <p className="result-rating">
//             ⭐ {item.vote_average.toFixed(1)}/10
//           </p>
//         )}
//         <p className="result-overview">
//           {item.overview || 'No description available.'}
//         </p>
//       </div>
//     </div>
//   );

//   return (
//     <div className="search-page-container">
//       <main className="search-content">
//         <div className="search-header">
//           <div className="search-title-section">
//             <Search size={32} className="icon-red" />
//             <div>
//               <h1 className="search-page-title">Search Results</h1>
//               {query && (
//                 <p className="search-query">
//                   Showing results for: <span className="query-text">"{query}"</span>
//                 </p>
//               )}
//             </div>
//           </div>
//         </div>

//         {loading ? (
//           <div className="loading-container">
//             <div className="loading-content">
//               <div className="loading-spinner"></div>
//               <p className="loading-text">Searching...</p>
//             </div>
//           </div>
//         ) : searchResults.length > 0 ? (
//           <div className="results-list">
//             {searchResults.map((item) => (
//               <ResultCard key={`${item.media_type}-${item.id}`} item={item} />
//             ))}
//           </div>
//         ) : query ? (
//           <div className="no-results">
//             <Film size={64} className="no-results-icon" />
//             <h2>No Results Found</h2>
//             <p>Try searching with different keywords</p>
//           </div>
//         ) : (
//           <div className="no-results">
//             <Search size={64} className="no-results-icon" />
//             <h2>Start Searching</h2>
//             <p>Use the search bar above to find movies and TV shows</p>
//           </div>
//         )}
//       </main>
//     </div>
//   );
// };

// export default SearchPage;