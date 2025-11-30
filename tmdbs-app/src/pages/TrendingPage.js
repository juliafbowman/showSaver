import React, { useState, useEffect } from 'react';
import { Film, TrendingUp, Star, Plus, Check } from 'lucide-react';
import './TrendingPage.css';

const TrendingPage = () => {
  const [trendingMovies, setTrendingMovies] = useState([]);
  const [trendingShows, setTrendingShows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [addedItems, setAddedItems] = useState({}); // Track which items have been added

  // TMDB API key (v3)
  const API_KEY = 'ab8ae844d4eb13ff70fb0ae9e0a97226';
  const BASE_URL = 'https://api.themoviedb.org/3';
  const IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500';
  const BACKEND_URL = 'http://127.0.0.1:5000';

  useEffect(() => {
    const fetchTrending = async () => {
      try {
        setLoading(true);
        
        // Fetch trending movies
        const moviesResponse = await fetch(
          `${BASE_URL}/trending/movie/week?api_key=${API_KEY}`
        );
        const moviesData = await moviesResponse.json();
        setTrendingMovies(moviesData.results || []);

        // Fetch trending TV shows
        const showsResponse = await fetch(
          `${BASE_URL}/trending/tv/week?api_key=${API_KEY}`
        );
        const showsData = await showsResponse.json();
        setTrendingShows(showsData.results || []);
        
        setLoading(false);
      } catch (error) {
        console.error('Error fetching trending content:', error);
        setLoading(false);
      }
    };

    fetchTrending();
  }, []);

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

  const MediaCard = ({ item, type }) => {
    const itemKey = `${type}-${item.id}`;
    const isAdded = addedItems[itemKey];

    return (
      <div className="media-card">
        <div className="media-poster-container">
          {item.poster_path ? (
            <img
              src={`${IMAGE_BASE_URL}${item.poster_path}`}
              alt={item.title || item.name}
              className="media-poster"
            />
          ) : (
            <div className="media-poster-placeholder">
              <Film size={64} className="placeholder-icon" />
            </div>
          )}
          <div className="media-rating">
            <Star size={16} fill="currentColor" />
            {item.vote_average?.toFixed(1)}
          </div>
          
          {/* Add to Log Button */}
          <button
            className={`add-to-log-button ${isAdded ? 'added' : ''}`}
            onClick={() => handleAddToLog(item.id, type)}
            disabled={isAdded}
            title={isAdded ? 'Added to log' : 'Add to log'}
          >
            {isAdded ? <Check size={20} /> : <Plus size={20} />}
          </button>
        </div>
        <div className="media-info">
          <h3 className="media-title">
            {item.title || item.name}
          </h3>
          <p className="media-date">
            {type === 'movie' ? item.release_date : item.first_air_date}
          </p>
          <p className="media-overview">
            {item.overview}
          </p>
        </div>
      </div>
    );
  };

  return (
    <div className="trending-container">
      {/* Content */}
      <main className="main-content">
        <div className="page-header">
          <div className="header-title-section">
            <TrendingUp size={32} className="icon-red" />
            <h1 className="page-title">Trending Now</h1>
          </div>
          <p className="page-subtitle">
            Discover the hottest movies and TV shows this week
          </p>
        </div>
        {loading ? (
          <div className="loading-container">
            <div className="loading-content">
              <div className="loading-spinner"></div>
              <p className="loading-text">Loading trending content...</p>
            </div>
          </div>
        ) : (
          <>
            {/* Trending Movies Section */}
            <section className="content-section">
              <h2 className="section-title">Trending Movies</h2>
              <div className="media-grid">
                {trendingMovies.slice(0, 8).map((item) => (
                  <MediaCard
                    key={item.id}
                    item={item}
                    type="movie"
                  />
                ))}
              </div>
            </section>

            {/* Trending TV Shows Section */}
            <section className="content-section">
              <h2 className="section-title">Trending TV Shows</h2>
              <div className="media-grid">
                {trendingShows.slice(0, 8).map((item) => (
                  <MediaCard
                    key={item.id}
                    item={item}
                    type="tv"
                  />
                ))}
              </div>
            </section>
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="trending-footer">
        <div className="footer-content">
          <p>Powered by TMDB API</p>
        </div>
      </footer>
    </div>
  );
};

export default TrendingPage;




// import React, { useState, useEffect } from 'react';
// import { Film, TrendingUp, Star } from 'lucide-react';
// import './TrendingPage.css';

// const TrendingPage = () => {
//   const [trendingMovies, setTrendingMovies] = useState([]);
//   const [trendingShows, setTrendingShows] = useState([]);
//   const [loading, setLoading] = useState(true);

//   // TMDB API key 
//   const API_KEY = 'ab8ae844d4eb13ff70fb0ae9e0a97226';
//   const BASE_URL = 'https://api.themoviedb.org/3';
//   const IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500';

//   useEffect(() => {
//     const fetchTrending = async () => {
//       try {
//         setLoading(true);
        
//         // Fetch trending movies
//         const moviesResponse = await fetch(
//           `${BASE_URL}/trending/movie/week?api_key=${API_KEY}`
//         );
//         const moviesData = await moviesResponse.json();
//         setTrendingMovies(moviesData.results || []);

//         // Fetch trending TV shows
//         const showsResponse = await fetch(
//           `${BASE_URL}/trending/tv/week?api_key=${API_KEY}`
//         );
//         const showsData = await showsResponse.json();
//         setTrendingShows(showsData.results || []);
        
//         setLoading(false);
//       } catch (error) {
//         console.error('Error fetching trending content:', error);
//         setLoading(false);
//       }
//     };

//     fetchTrending();
//   }, []);

//   const MediaCard = ({ item, type }) => (
//     <div className="media-card">
//       <div className="media-poster-container">
//         {item.poster_path ? (
//           <img
//             src={`${IMAGE_BASE_URL}${item.poster_path}`}
//             alt={item.title || item.name}
//             className="media-poster"
//           />
//         ) : (
//           <div className="media-poster-placeholder">
//             <Film size={64} className="placeholder-icon" />
//           </div>
//         )}
//         <div className="media-rating">
//           <Star size={16} fill="currentColor" />
//           {item.vote_average?.toFixed(1)}
//         </div>
//       </div>
//       <div className="media-info">
//         <h3 className="media-title">
//           {item.title || item.name}
//         </h3>
//         <p className="media-date">
//           {type === 'movie' ? item.release_date : item.first_air_date}
//         </p>
//         <p className="media-overview">
//           {item.overview}
//         </p>
//       </div>
//     </div>
//   );

//   return (
//     <div className="trending-container">
//       {/* Content */}
//       <main className="main-content">
//         <div className="page-header">
//           <div className="header-title-section">
//             <TrendingUp size={32} className="icon-red" />
//             <h1 className="page-title">Trending Now</h1>
//           </div>
//           <p className="page-subtitle">
//             Discover the hottest movies and TV shows this week
//           </p>
//         </div>
//         {loading ? (
//           <div className="loading-container">
//             <div className="loading-content">
//               <div className="loading-spinner"></div>
//               <p className="loading-text">Loading trending content...</p>
//             </div>
//           </div>
//         ) : (
//           <>
//             {/* Trending Movies Section */}
//             <section className="content-section">
//               <h2 className="section-title">Trending Movies</h2>
//               <div className="media-grid">
//                 {trendingMovies.slice(0, 8).map((item) => (
//                   <MediaCard
//                     key={item.id}
//                     item={item}
//                     type="movie"
//                   />
//                 ))}
//               </div>
//             </section>

//             {/* Trending TV Shows Section */}
//             <section className="content-section">
//               <h2 className="section-title">Trending TV Shows</h2>
//               <div className="media-grid">
//                 {trendingShows.slice(0, 8).map((item) => (
//                   <MediaCard
//                     key={item.id}
//                     item={item}
//                     type="tv"
//                   />
//                 ))}
//               </div>
//             </section>
//           </>
//         )}
//       </main>

//       {/* Footer */}
//       <footer className="trending-footer">
//         <div className="footer-content">
//           <p>Powered by TMDB API</p>
//         </div>
//       </footer>
//     </div>
//   );
// };

// export default TrendingPage;