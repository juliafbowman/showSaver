import React, { useState } from 'react';
import { X, Star } from 'lucide-react';
import './Ratingmodal.css';

const RatingModal = ({ isOpen, onClose, onSubmit, item }) => {
  const [rating, setRating] = useState(item?.user_rating || 0);
  const [hoverRating, setHoverRating] = useState(0);
  const [reviewText, setReviewText] = useState('');

  if (!isOpen) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    if (rating > 0) {
      onSubmit(rating, reviewText);
      setRating(0);
      setReviewText('');
    }
  };

  const handleClose = () => {
    setRating(item?.user_rating || 0);
    setReviewText('');
    onClose();
  };

  return (
    <div className="modal-overlay" onClick={handleClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={handleClose}>
          <X size={24} />
        </button>

        <h2 className="modal-title">Rate "{item?.title_name}"</h2>

        <form onSubmit={handleSubmit}>
          {/* Star Rating */}
          <div className="rating-section">
            <label className="rating-label">Your Rating</label>
            <div className="stars-container">
              {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((star) => (
                <button
                  key={star}
                  type="button"
                  className={`star-button ${
                    star <= (hoverRating || rating) ? 'active' : ''
                  }`}
                  onMouseEnter={() => setHoverRating(star)}
                  onMouseLeave={() => setHoverRating(0)}
                  onClick={() => setRating(star)}
                >
                  <Star
                    size={32}
                    fill={star <= (hoverRating || rating) ? 'currentColor' : 'none'}
                  />
                </button>
              ))}
            </div>
            <p className="rating-value">
              {rating > 0 ? `${rating}/10` : 'Click to rate'}
            </p>
          </div>

          {/* Review Text (Optional) */}
          <div className="review-section">
            <label className="review-label">Review (Optional)</label>
            <textarea
              className="review-textarea"
              placeholder="Share your thoughts about this movie..."
              value={reviewText}
              onChange={(e) => setReviewText(e.target.value)}
              rows={4}
            />
          </div>

          {/* Buttons */}
          <div className="modal-buttons">
            <button
              type="button"
              className="cancel-button"
              onClick={handleClose}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="submit-button"
              disabled={rating === 0}
            >
              {item?.user_rating ? 'Update Rating' : 'Add Rating'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RatingModal;