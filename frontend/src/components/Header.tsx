import React from 'react';
import { Link } from 'react-router-dom';
import { MapIcon } from '@heroicons/react/24/outline';

export const Header: React.FC = () => {
  return (
    <header className="header">
      <Link to="/" className="logo">
        <div className="flex items-center space-x-2">
          <div className="p-2 bg-blue-100 rounded-lg">
            <MapIcon className="w-6 h-6 text-blue-600" />
          </div>
          <h1>Trip Planner</h1>
        </div>
      </Link>
      <nav>
        <ul className="nav-links">
          <li>
            <Link to="/">Главная</Link>
          </li>
          <li>
            <Link to="/trips">Поездки</Link>
          </li>
        </ul>
      </nav>
    </header>
  );
};
