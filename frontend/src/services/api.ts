import axios from 'axios';
import { User, Trip, Place, Suggestion, Route, Expense, Balance, OSMPlace } from '../types';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Users
export const getUsers = async (): Promise<User[]> => {
  const response = await api.get('/api/users/');
  return response.data;
};

export const createUser = async (userData: { email: string; username: string }): Promise<User> => {
  const response = await api.post('/api/users/', userData);
  return response.data;
};

export const getUser = async (userId: number): Promise<User> => {
  const response = await api.get(`/api/users/${userId}`);
  return response.data;
};

// Trips
export const getTrips = async (): Promise<Trip[]> => {
  const response = await api.get('/api/trips/');
  return response.data;
};

export const createTrip = async (tripData: any): Promise<Trip> => {
  const response = await api.post('/api/trips/', tripData);
  return response.data;
};

export const getTrip = async (tripId: number): Promise<Trip> => {
  const response = await api.get(`/api/trips/${tripId}`);
  return response.data;
};

export const updateTrip = async (tripId: number, tripData: any): Promise<Trip> => {
  const response = await api.patch(`/api/trips/${tripId}`, tripData);
  return response.data;
};

export const deleteTrip = async (tripId: number): Promise<void> => {
  await api.delete(`/api/trips/${tripId}`);
};

export const addTripMember = async (tripId: number, memberData: any): Promise<any> => {
  const response = await api.post(`/api/trips/${tripId}/members`, memberData);
  return response.data;
};

export const getTripMembers = async (tripId: number): Promise<any[]> => {
  const response = await api.get(`/api/trips/${tripId}/members`);
  return response.data;
};

// Places
export const searchPlaces = async (query: string, limit: number = 10): Promise<OSMPlace[]> => {
  const response = await api.get(`/api/places/search?query=${encodeURIComponent(query)}&limit=${limit}`);
  return response.data.places;
};

export const createPlace = async (placeData: any): Promise<Place> => {
  const response = await api.post('/api/places/', placeData);
  return response.data;
};

export const getPlaces = async (): Promise<Place[]> => {
  const response = await api.get('/api/places/');
  return response.data;
};

export const getPlace = async (placeId: number): Promise<Place> => {
  const response = await api.get(`/api/places/${placeId}`);
  return response.data;
};

// Suggestions
export const getSuggestions = async (tripId: number): Promise<Suggestion[]> => {
  const response = await api.get(`/api/suggestions/trip/${tripId}`);
  return response.data;
};

export const createSuggestion = async (tripId: number, placeId: number, suggestedBy: number): Promise<Suggestion> => {
  const response = await api.post(`/api/suggestions/trip/${tripId}?place_id=${placeId}&suggested_by=${suggestedBy}`);
  return response.data;
};

export const voteOnSuggestion = async (suggestionId: number, userId: number, vote: boolean): Promise<any> => {
  const response = await api.post(`/api/suggestions/${suggestionId}/vote?user_id=${userId}`, { vote });
  return response.data;
};

export const updateSuggestionStatus = async (suggestionId: number, status: string): Promise<any> => {
  const response = await api.patch(`/api/suggestions/${suggestionId}/status?status=${status}`);
  return response.data;
};

// Routes
export const getTripRoutes = async (tripId: number): Promise<Route[]> => {
  const response = await api.get(`/api/routes/trip/${tripId}`);
  return response.data;
};

export const createRoute = async (routeData: any): Promise<Route> => {
  const response = await api.post('/api/routes/', routeData);
  return response.data;
};

export const updateRoute = async (routeId: number, routeData: any): Promise<Route> => {
  const response = await api.patch(`/api/routes/${routeId}`, routeData);
  return response.data;
};

export const deleteRoute = async (routeId: number): Promise<void> => {
  await api.delete(`/api/routes/${routeId}`);
};

// Expenses
export const getTripExpenses = async (tripId: number): Promise<Expense[]> => {
  const response = await api.get(`/api/expenses/trip/${tripId}`);
  return response.data;
};

export const createExpense = async (expenseData: any): Promise<Expense> => {
  const response = await api.post('/api/expenses/', expenseData);
  return response.data;
};

export const deleteExpense = async (expenseId: number): Promise<void> => {
  await api.delete(`/api/expenses/${expenseId}`);
};

export const getTripBalances = async (tripId: number): Promise<Balance[]> => {
  const response = await api.get(`/api/expenses/trip/${tripId}/balances`);
  return response.data;
};
