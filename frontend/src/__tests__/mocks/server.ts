import { setupServer } from 'msw/node';
import { rest, RestRequest, RestContext, ResponseComposition } from 'msw';

// Mock data
const mockUsers = [
  { id: 1, email: 'test@example.com', username: 'testuser', created_time: '2024-01-01T00:00:00Z' },
  { id: 2, email: 'user2@example.com', username: 'user2', created_time: '2024-01-02T00:00:00Z' }
];

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

export const handlers = [
  // Users endpoints
  rest.get('http://localhost:8000/api/users/', (req: RestRequest, res: ResponseComposition, ctx: RestContext) => {
    return res(ctx.status(200), ctx.json(mockUsers));
  }),
  
  rest.post('http://localhost:8000/api/users/', (req: RestRequest, res: ResponseComposition, ctx: RestContext) => {
    return res(ctx.status(200), ctx.json(mockUsers[0]));
  }),
  
  rest.get('http://localhost:8000/api/users/:id', (req: RestRequest, res: ResponseComposition, ctx: RestContext) => {
    const { id } = req.params;
    const user = mockUsers.find(u => u.id === Number(id));
    if (user) {
      return res(ctx.status(200), ctx.json(user));
    }
    return res(ctx.status(404), ctx.json({ detail: 'User not found' }));
  }),

  // Trips endpoints
  rest.get('http://localhost:8000/api/trips/', (req: RestRequest, res: ResponseComposition, ctx: RestContext) => {
    return res(ctx.status(200), ctx.json(mockTrips));
  }),
  
  rest.post('http://localhost:8000/api/trips/', (req: RestRequest, res: ResponseComposition, ctx: RestContext) => {
    return res(ctx.status(200), ctx.json(mockTrips[0]));
  }),
  
  rest.get('http://localhost:8000/api/trips/:id', (req: RestRequest, res: ResponseComposition, ctx: RestContext) => {
    const { id } = req.params;
    const trip = mockTrips.find(t => t.id === Number(id));
    if (trip) {
      return res(ctx.status(200), ctx.json(trip));
    }
    return res(ctx.status(404), ctx.json({ detail: 'Trip not found' }));
  }),

  // Places endpoints
  rest.get('http://localhost:8000/api/places/', (req: RestRequest, res: ResponseComposition, ctx: RestContext) => {
    return res(ctx.status(200), ctx.json(mockPlaces));
  }),
  
  rest.post('http://localhost:8000/api/places/', (req: RestRequest, res: ResponseComposition, ctx: RestContext) => {
    return res(ctx.status(200), ctx.json(mockPlaces[0]));
  }),
  
  rest.get('http://localhost:8000/api/places/:id', (req: RestRequest, res: ResponseComposition, ctx: RestContext) => {
    const { id } = req.params;
    const place = mockPlaces.find(p => p.id === Number(id));
    if (place) {
      return res(ctx.status(200), ctx.json(place));
    }
    return res(ctx.status(404), ctx.json({ detail: 'Place not found' }));
  }),

  // Health check
  rest.get('http://localhost:8000/health', (req: RestRequest, res: ResponseComposition, ctx: RestContext) => {
    return res(ctx.status(200), ctx.json({ status: 'ok' }));
  }),
];

export const server = setupServer(...handlers);
