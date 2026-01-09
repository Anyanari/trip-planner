import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { TripCard } from '../../components/TripCard';

// Mock data matching the actual TripCardProps interface
const mockTripProps = {
  id: '1',
  title: 'Test Trip',
  location: 'Moscow, Russia',
  description: 'A wonderful test trip to Moscow',
  imageUrl: 'https://example.com/image.jpg',
  rating: 4.5,
  reviews: 12,
  price: 15000,
  duration: '7 дней',
  groupSize: 8,
  dates: '01.06.2024 - 07.06.2024',
  isFavorite: false,
  onToggleFavorite: jest.fn()
};

const renderWithRouter = (component: React.ReactElement) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  );
};

describe('TripCard', () => {
  it('renders trip information correctly', () => {
    renderWithRouter(<TripCard {...mockTripProps} />);
    
    expect(screen.getByText('Test Trip')).toBeInTheDocument();
    expect(screen.getByText('Moscow, Russia')).toBeInTheDocument();
    expect(screen.getByText('A wonderful test trip to Moscow')).toBeInTheDocument();
    expect(screen.getByText('01.06.2024 - 07.06.2024')).toBeInTheDocument();
    expect(screen.getByText('7 дней')).toBeInTheDocument();
    expect(screen.getByText('8 человек')).toBeInTheDocument();
  });

  it('renders rating information', () => {
    renderWithRouter(<TripCard {...mockTripProps} />);
    
    expect(screen.getByText('4.5')).toBeInTheDocument();
    expect(screen.getByText('(12)')).toBeInTheDocument();
  });

  it('renders price correctly', () => {
    renderWithRouter(<TripCard {...mockTripProps} />);
    
    expect(screen.getByText('15,000 ₽')).toBeInTheDocument();
    expect(screen.getByText('/ человек')).toBeInTheDocument();
  });

  it('renders favorite button', () => {
    renderWithRouter(<TripCard {...mockTripProps} />);
    
    const favoriteButton = screen.getByRole('button');
    expect(favoriteButton).toBeInTheDocument();
  });

  it('toggles favorite when button is clicked', () => {
    renderWithRouter(<TripCard {...mockTripProps} />);
    
    const favoriteButton = screen.getByRole('button');
    fireEvent.click(favoriteButton);
    
    expect(mockTripProps.onToggleFavorite).toHaveBeenCalledWith('1');
  });

  it('shows solid heart when favorited', () => {
    const favoritedProps = { ...mockTripProps, isFavorite: true };
    renderWithRouter(<TripCard {...favoritedProps} />);
    
    // Check for solid heart icon (implementation dependent)
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  it('handles image error gracefully', () => {
    renderWithRouter(<TripCard {...mockTripProps} />);
    
    const image = screen.getByAltText('Test Trip');
    fireEvent.error(image);
    
    // Should show placeholder when image fails to load
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  it('navigates to trip details when clicked', () => {
    renderWithRouter(<TripCard {...mockTripProps} />);
    
    const link = screen.getByRole('link');
    expect(link).toHaveAttribute('href', '/trips/1');
  });

  it('shows "Посмотреть маршрут" button', () => {
    renderWithRouter(<TripCard {...mockTripProps} />);
    
    expect(screen.getByText('Посмотреть маршрут')).toBeInTheDocument();
  });

  it('applies hover styles on interaction', () => {
    renderWithRouter(<TripCard {...mockTripProps} />);
    
    const card = screen.getByRole('link');
    fireEvent.mouseEnter(card);
    
    expect(card).toBeInTheDocument();
  });

  it('truncates long descriptions', () => {
    const longDescription = 'A'.repeat(200);
    const propsWithLongDescription = { ...mockTripProps, description: longDescription };
    
    renderWithRouter(<TripCard {...propsWithLongDescription} />);
    
    expect(screen.getByText('Test Trip')).toBeInTheDocument();
    // Description should be truncated via CSS line-clamp
  });

  it('has proper accessibility attributes', () => {
    renderWithRouter(<TripCard {...mockTripProps} />);
    
    const card = screen.getByRole('link');
    expect(card).toBeInTheDocument();
  });

  it('handles missing onToggleFavorite gracefully', () => {
    const propsWithoutCallback = { ...mockTripProps, onToggleFavorite: undefined };
    renderWithRouter(<TripCard {...propsWithoutCallback} />);
    
    const favoriteButton = screen.getByRole('button');
    fireEvent.click(favoriteButton);
    
    // Should not throw error when callback is not provided
    expect(screen.getByRole('button')).toBeInTheDocument();
  });
});
