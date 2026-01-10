import axios from 'axios';
import { 
  getUsers, 
  createUser, 
  getUser, 
  getTrips, 
  createTrip, 
  getTrip,
  getPlaces,
  createPlace,
  getPlace
} from '../../services/api';

// Mock axios
jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('API Service', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('User API', () => {
    it('should get users', async () => {
      const mockUsers = [
        { id: 1, email: 'test@example.com', username: 'testuser', created_time: '2024-01-01T00:00:00Z' }
      ];
      
      mockedAxios.get.mockResolvedValue({ data: mockUsers });
      
      const result = await getUsers();
      
      expect(mockedAxios.get).toHaveBeenCalledWith('/api/users/');
      expect(result).toEqual(mockUsers);
    });

    it('should create user', async () => {
      const userData = { email: 'test@example.com', username: 'testuser' };
      const mockUser = { id: 1, ...userData, created_time: '2024-01-01T00:00:00Z' };
      
      mockedAxios.post.mockResolvedValue({ data: mockUser });
      
      const result = await createUser(userData);
      
      expect(mockedAxios.post).toHaveBeenCalledWith('/api/users/', userData);
      expect(result).toEqual(mockUser);
    });

    it('should get user by ID', async () => {
      const mockUser = { id: 1, email: 'test@example.com', username: 'testuser', created_time: '2024-01-01T00:00:00Z' };
      
      mockedAxios.get.mockResolvedValue({ data: mockUser });
      
      const result = await getUser(1);
      
      expect(mockedAxios.get).toHaveBeenCalledWith('/api/users/1');
      expect(result).toEqual(mockUser);
    });

    it('should handle API errors when getting users', async () => {
      const errorMessage = 'Network Error';
      mockedAxios.get.mockRejectedValue(new Error(errorMessage));
      
      await expect(getUsers()).rejects.toThrow(errorMessage);
    });

    it('should handle API errors when creating user', async () => {
      const userData = { email: 'test@example.com', username: 'testuser' };
      const errorMessage = 'Email already registered';
      
      mockedAxios.post.mockRejectedValue(new Error(errorMessage));
      
      await expect(createUser(userData)).rejects.toThrow(errorMessage);
    });
  });

  describe('Trip API', () => {
    it('should get trips', async () => {
      const mockTrips = [
        {
          id: 1,
          title: 'Test Trip',
          description: 'A test trip',
          start_date: '2024-06-01',
          end_date: '2024-06-07',
          admin: 1,
          created_time: '2024-01-01T00:00:00Z',
          is_active: true
        }
      ];
      
      mockedAxios.get.mockResolvedValue({ data: mockTrips });
      
      const result = await getTrips();
      
      expect(mockedAxios.get).toHaveBeenCalledWith('/api/trips/');
      expect(result).toEqual(mockTrips);
    });

    it('should create trip', async () => {
      const tripData = {
        title: 'Test Trip',
        description: 'A test trip',
        start_date: '2024-06-01',
        end_date: '2024-06-07',
        admin: 1
      };
      const mockTrip = { id: 1, ...tripData, created_time: '2024-01-01T00:00:00Z', is_active: true };
      
      mockedAxios.post.mockResolvedValue({ data: mockTrip });
      
      const result = await createTrip(tripData);
      
      expect(mockedAxios.post).toHaveBeenCalledWith('/api/trips/', tripData);
      expect(result).toEqual(mockTrip);
    });

    it('should get trip by ID', async () => {
      const mockTrip = {
        id: 1,
        title: 'Test Trip',
        description: 'A test trip',
        start_date: '2024-06-01',
        end_date: '2024-06-07',
        admin: 1,
        created_time: '2024-01-01T00:00:00Z',
        is_active: true
      };
      
      mockedAxios.get.mockResolvedValue({ data: mockTrip });
      
      const result = await getTrip(1);
      
      expect(mockedAxios.get).toHaveBeenCalledWith('/api/trips/1');
      expect(result).toEqual(mockTrip);
    });

    it('should handle API errors when getting trips', async () => {
      const errorMessage = 'Network Error';
      mockedAxios.get.mockRejectedValue(new Error(errorMessage));
      
      await expect(getTrips()).rejects.toThrow(errorMessage);
    });
  });

  describe('Place API', () => {
    it('should get places', async () => {
      const mockPlaces = [
        {
          id: 1,
          name: 'Test Place',
          lat: 55.7558,
          lng: 37.6173,
          osm_id: 'node/123456',
          address: 'Test Address',
          created_at: '2024-01-01T00:00:00Z'
        }
      ];
      
      mockedAxios.get.mockResolvedValue({ data: mockPlaces });
      
      const result = await getPlaces();
      
      expect(mockedAxios.get).toHaveBeenCalledWith('/api/places/');
      expect(result).toEqual(mockPlaces);
    });

    it('should create place', async () => {
      const placeData = {
        name: 'Test Place',
        lat: 55.7558,
        lng: 37.6173,
        osm_id: 'node/123456',
        address: 'Test Address'
      };
      const mockPlace = { id: 1, ...placeData, created_at: '2024-01-01T00:00:00Z' };
      
      mockedAxios.post.mockResolvedValue({ data: mockPlace });
      
      const result = await createPlace(placeData);
      
      expect(mockedAxios.post).toHaveBeenCalledWith('/api/places/', placeData);
      expect(result).toEqual(mockPlace);
    });

    it('should get place by ID', async () => {
      const mockPlace = {
        id: 1,
        name: 'Test Place',
        lat: 55.7558,
        lng: 37.6173,
        osm_id: 'node/123456',
        address: 'Test Address',
        created_at: '2024-01-01T00:00:00Z'
      };
      
      mockedAxios.get.mockResolvedValue({ data: mockPlace });
      
      const result = await getPlace(1);
      
      expect(mockedAxios.get).toHaveBeenCalledWith('/api/places/1');
      expect(result).toEqual(mockPlace);
    });

    it('should handle API errors when getting places', async () => {
      const errorMessage = 'Network Error';
      mockedAxios.get.mockRejectedValue(new Error(errorMessage));
      
      await expect(getPlaces()).rejects.toThrow(errorMessage);
    });
  });

  describe('API Configuration', () => {
    it('should have correct base URL', () => {
      expect(mockedAxios.create).toHaveBeenCalledWith({
        baseURL: 'http://localhost:8000',
        headers: {
          'Content-Type': 'application/json',
        },
      });
    });

    it('should have default headers', () => {
      // This test verifies that the API instance is configured correctly
      // The actual configuration happens in the api.ts file
      expect(axios.defaults.headers.common['Content-Type']).toBe('application/json');
    });
  });

  describe('Error Handling', () => {
    it('should handle 404 errors', async () => {
      const error = {
        response: {
          status: 404,
          data: { detail: 'Not found' }
        }
      };
      
      mockedAxios.get.mockRejectedValue(error);
      
      try {
        await getUser(999);
      } catch (err: any) {
        expect(err.response.status).toBe(404);
        expect(err.response.data.detail).toBe('Not found');
      }
    });

    it('should handle 500 errors', async () => {
      const error = {
        response: {
          status: 500,
          data: { detail: 'Internal server error' }
        }
      };
      
      mockedAxios.get.mockRejectedValue(error);
      
      try {
        await getUsers();
      } catch (err: any) {
        expect(err.response.status).toBe(500);
        expect(err.response.data.detail).toBe('Internal server error');
      }
    });

    it('should handle network errors', async () => {
      const networkError = new Error('Network Error');
      mockedAxios.get.mockRejectedValue(networkError);
      
      await expect(getUsers()).rejects.toThrow('Network Error');
    });
  });
});
