import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { 
  HeartIcon, 
  MapPinIcon, 
  StarIcon,
  CalendarIcon,
  UserGroupIcon
} from '@heroicons/react/24/outline';
import { HeartIcon as HeartSolidIcon } from '@heroicons/react/24/solid';

interface TripCardProps {
  id: string;
  title: string;
  location: string;
  description: string;
  imageUrl: string;
  rating: number;
  reviews: number;
  price: number;
  duration: string;
  groupSize: number;
  dates: string;
  isFavorite?: boolean;
  onToggleFavorite?: (id: string) => void;
}

export const TripCard: React.FC<TripCardProps> = ({
  id,
  title,
  location,
  description,
  imageUrl,
  rating,
  reviews,
  price,
  duration,
  groupSize,
  dates,
  isFavorite = false,
  onToggleFavorite,
}) => {
  const [favorite, setFavorite] = useState(isFavorite);
  const [imageError, setImageError] = useState(false);

  const handleFavoriteClick = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setFavorite(!favorite);
    onToggleFavorite?.(id);
  };

  return (
    <Link 
      to={`/trips/${id}`}
      className="booking-card group cursor-pointer transform hover:scale-[1.02] transition-all duration-300"
    >
      <div className="relative">
        {/* Image */}
        <div className="relative h-48 overflow-hidden">
          {!imageError ? (
            <img
              src={imageUrl}
              alt={title}
              className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
              onError={() => setImageError(true)}
            />
          ) : (
            <div className="w-full h-full bg-gray-200 flex items-center justify-center">
              <MapPinIcon className="w-12 h-12 text-gray-400" />
            </div>
          )}
          
          {/* Favorite button */}
          <button
            onClick={handleFavoriteClick}
            className="absolute top-3 right-3 p-2 bg-white rounded-full shadow-lg hover:shadow-xl transition-all duration-200"
          >
            {favorite ? (
              <HeartSolidIcon className="w-5 h-5 text-red-500" />
            ) : (
              <HeartIcon className="w-5 h-5 text-gray-600 hover:text-red-500 transition-colors" />
            )}
          </button>

          {/* Rating badge */}
          <div className="absolute bottom-3 left-3 bg-white px-2 py-1 rounded-lg shadow-md flex items-center space-x-1">
            <StarIcon className="w-4 h-4 text-yellow-500 fill-current" />
            <span className="text-sm font-semibold">{rating}</span>
            <span className="text-xs text-gray-500">({reviews})</span>
          </div>
        </div>

        {/* Content */}
        <div className="p-4">
          {/* Location */}
          <div className="flex items-center text-sm text-gray-600 mb-2">
            <MapPinIcon className="w-4 h-4 mr-1" />
            {location}
          </div>

          {/* Title */}
          <h3 className="font-semibold text-lg text-gray-900 dark:text-white mb-2 line-clamp-2 group-hover:text-primary-600 transition-colors">
            {title}
          </h3>

          {/* Description */}
          <p className="text-sm text-gray-600 dark:text-gray-300 mb-3 line-clamp-2">
            {description}
          </p>

          {/* Trip details */}
          <div className="flex items-center justify-between text-sm text-gray-500 mb-3">
            <div className="flex items-center">
              <CalendarIcon className="w-4 h-4 mr-1" />
              <span>{duration}</span>
            </div>
            <div className="flex items-center">
              <UserGroupIcon className="w-4 h-4 mr-1" />
              <span>{groupSize} человек</span>
            </div>
          </div>

          {/* Dates */}
          <div className="text-xs text-gray-500 mb-3">
            {dates}
          </div>

          {/* Price and CTA */}
          <div className="flex items-center justify-between">
            <div>
              <span className="text-2xl font-bold text-primary-600">{price.toLocaleString()} ₽</span>
              <span className="text-sm text-gray-500"> / человек</span>
            </div>
            <button className="btn-primary text-sm py-2 px-4">
              Посмотреть маршрут
            </button>
          </div>
        </div>
      </div>
    </Link>
  );
};
