import React, { useState, useEffect } from "react";
import {
  Film,
  Trash2,
  Clock,
  Star,
  Tv,
  Clapperboard,
  ArrowUpDown,
} from "lucide-react";
import RatingModal from "../components/Ratingmodal";
import "./Logpage.css";

const LogPage = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState("title-asc"); // Default sort
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);

  const BACKEND_URL = "http://127.0.0.1:5000";
  const IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500";

  // Fetch all logged items with sorting
  const fetchLogs = async (sort = "title", order = "asc") => {
    try {
      setLoading(true);
      const response = await fetch(
        `${BACKEND_URL}/api/logs/sorted?sort=${sort}&order=${order}`
      );
      const data = await response.json();
      setLogs(data);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching logs:", error);
      setLoading(false);
    }
  };

  // Handle sort change
  const handleSortChange = (e) => {
    const value = e.target.value;
    setSortBy(value);

    // Parse sort value (format: "field-order")
    const [sort, order] = value.split("-");
    fetchLogs(sort, order);
  };

  // Delete a logged item
  const handleDelete = async (titleId) => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/logs/${titleId}`, {
        method: "DELETE",
      });
      const data = await response.json();
      console.log(data.message);

      // Refresh the list after deletion with current sort
      const [sort, order] = sortBy.split("-");
      fetchLogs(sort, order);
    } catch (error) {
      console.error("Error deleting item:", error);
    }
  };

  // Open rating modal
  const handleRateClick = (item) => {
    setSelectedItem(item);
    setIsModalOpen(true);
  };

  // Submit rating
  const handleRatingSubmit = async (rating, reviewText) => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/rating`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          rating: rating,
          title_id: selectedItem.title_id,
          review_text: reviewText,
        }),
      });

      const data = await response.json();
      console.log(data.message);

      // Close modal and refresh logs
      setIsModalOpen(false);
      setSelectedItem(null);
      const [sort, order] = sortBy.split("-");
      fetchLogs(sort, order);
    } catch (error) {
      console.error("Error submitting rating:", error);
    }
  };

  useEffect(() => {
    // Initial fetch with default sort
    const [sort, order] = sortBy.split("-");
    fetchLogs(sort, order);
  }, []);

  const LogCard = ({ item }) => {
    const [poster, setPoster] = useState(null);

    useEffect(() => {
      const fetchPoster = async () => {
        try {
          const endpoint =
            item.content_type === "movie"
              ? `https://api.themoviedb.org/3/movie/${item.title_id}`
              : `https://api.themoviedb.org/3/tv/${item.title_id}`;

          const res = await fetch(
            `${endpoint}?api_key=ab8ae844d4eb13ff70fb0ae9e0a97226`
          );
          const data = await res.json();

          setPoster(data.poster_path);
        } catch (err) {
          console.error("Poster fetch failed", err);
        }
      };

      fetchPoster();
    }, [item.title_id, item.content_type]);

    return (
      <div className="log-card">
        <div className="log-poster-container">
          {poster ? (
            <img
              src={`${IMAGE_BASE_URL}${poster}`}
              alt={item.title_name}
              className="log-poster"
            />
          ) : (
            <div className="log-poster-placeholder">
              <Film size={48} className="placeholder-icon" />
            </div>
          )}
          <div className="log-type-badge">
            {item.content_type === "movie" ? (
              <>
                <Clapperboard size={14} /> Movie
              </>
            ) : (
              <>
                <Tv size={14} /> TV
              </>
            )}
          </div>
        </div>

        <div className="log-info">
          <h3 className="log-title">{item.title_name}</h3>

          <p className="log-year">{item.release_year}</p>

          {item.genres && item.genres.length > 0 && (
            <div className="log-genres">
              {item.genres.map((genre, index) => (
                <span key={index} className="genre-tag">
                  {genre}
                </span>
              ))}
            </div>
          )}

          <div className="log-meta">
            {item.display_duration && (
              <span className="log-runtime">
                <Clock size={14} /> {item.display_duration} min
              </span>
            )}

            {item.tmdb_avg_rating && (
              <span className="log-tmdb-rating">
                <Star size={14} /> TMDB: {item.tmdb_avg_rating.toFixed(1)}/10
              </span>
            )}
          </div>

          {/* User Rating or Rate Button */}
          <div className="user-rating-section">
            {item.user_rating ? (
              <div className="rating-display">
                <button
                  className="edit-rating-button"
                  onClick={() => handleRateClick(item)}
                >
                  <Star size={16} fill="currentColor" className="rating-star" />
                  Your Rating: {item.user_rating}/10
                  <span className="edit-text">Edit</span>
                </button>
                {item.review_text && (
                  <p className="review-text">"{item.review_text}"</p>
                )}
              </div>
            ) : (
              <button
                className="rate-button"
                onClick={() => handleRateClick(item)}
              >
                <Star size={16} />
                Rate This
              </button>
            )}
          </div>

          {item.date_posted && (
            <p className="log-date">
              Added: {new Date(item.date_posted).toLocaleDateString()}
            </p>
          )}
        </div>

        <button
          className="delete-button"
          onClick={() => handleDelete(item.title_id)}
          title="Remove from log"
        >
          <Trash2 size={20} />
        </button>
      </div>
    );
  };

  return (
    <div className="log-page-container">
      <main className="log-content">
        <div className="log-header">
          <div className="log-title-section">
            <Film size={32} className="icon-red" />
            <div>
              <h1 className="log-page-title">My Watch Log</h1>
              <p className="log-subtitle">
                {logs.length} {logs.length === 1 ? "title" : "titles"} logged
              </p>
            </div>
          </div>

          {/* Sort Dropdown */}
          {logs.length > 0 && (
            <div className="sort-container">
              <ArrowUpDown size={18} className="sort-icon" />
              <select
                className="sort-dropdown"
                value={sortBy}
                onChange={handleSortChange}
              >
                <option value="title-asc">Title (A-Z)</option>
                <option value="title-desc">Title (Z-A)</option>
                <option value="year-desc">Year (Newest First)</option>
                <option value="year-asc">Year (Oldest First)</option>
                <option value="rating-desc">Rating (High to Low)</option>
                <option value="rating-asc">Rating (Low to High)</option>
                <option value="runtime-desc">Runtime (Longest First)</option>
                <option value="runtime-asc">Runtime (Shortest First)</option>
                <option value="date-desc">Date Added (Newest)</option>
                <option value="date-asc">Date Added (Oldest)</option>
              </select>
            </div>
          )}
        </div>

        {loading ? (
          <div className="loading-container">
            <div className="loading-content">
              <div className="loading-spinner"></div>
              <p className="loading-text">Loading your log...</p>
            </div>
          </div>
        ) : logs.length > 0 ? (
          <div className="log-list">
            {logs.map((item) => (
              <LogCard key={item.title_id} item={item} />
            ))}
          </div>
        ) : (
          <div className="empty-log">
            <Film size={64} className="empty-icon" />
            <h2>Your log is empty</h2>
            <p>
              Start adding movies and TV shows from the Search or Trending
              pages!
            </p>
          </div>
        )}
      </main>

      {/* Rating Modal */}
      <RatingModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleRatingSubmit}
        item={selectedItem}
      />
    </div>
  );
};

export default LogPage;
