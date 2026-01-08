export interface User {
  id: number;
  email: string;
  username: string;
  created_time: string;
}

export interface Trip {
  id: number;
  title: string;
  description?: string;
  start_date: string;
  end_date: string;
  admin?: number;
  created_time: string;
  is_active: boolean;
  admin_user?: User;
  members?: User[];
}

export interface Place {
  id: number;
  name: string;
  lat: number;
  lng: number;
  osm_id?: string;
  address?: string;
  created_at: string;
}

export interface Suggestion {
  id: number;
  trip_id: number;
  place_id: number;
  suggested_by: number;
  suggested_at: string;
  status: 'voting' | 'accepted' | 'rejected';
  votes_for: number;
  votes_against: number;
  place: Place;
  suggested_by_user: User;
}

export interface Vote {
  id: number;
  suggestion_id: number;
  user_id: number;
  vote: boolean;
  voted_at: string;
}

export interface Route {
  id: number;
  trip_id: number;
  place_id: number;
  day_number: number;
  order_in_day: number;
  planned_time?: string;
  estimated_cost?: number;
  notes?: string;
  added_by?: number;
  added_at: string;
  place: Place;
  added_by_user?: User;
}

export interface Expense {
  id: number;
  trip_id: number;
  title: string;
  amount: number;
  currency: string;
  paid_by: number;
  created_at: string;
  paid_by_user: User;
}

export interface ExpenseShare {
  id: number;
  expense_id: number;
  user_id: number;
  share: number;
  user: User;
}

export interface Balance {
  debtor_id: number;
  debtor_name: string;
  creditor_id: number;
  creditor_name: string;
  amount: number;
}

export interface OSMPlace {
  place_id: number;
  licence: string;
  osm_type: string;
  osm_id: number;
  lat: string;
  lon: string;
  display_name: string;
  address: any;
  boundingbox: string[];
}
