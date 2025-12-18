export interface Member {
  id: number;
  name: string;
  contact: string;
  address?: string;
  family?: string;
  status: string;
}

export interface Event {
  id: number;
  name: string;
  description?: string;
  date: string;
  created_at: string;
}

export interface Sacrament {
  id: number;
  member_id: number;
  member_name?: string;
  type: string;
  date?: string;
  certificate_path?: string;
}

export interface Attendance {
  id: number;
  event_id: number;
  event_name?: string;
  member_id: number;
  member_name?: string;
  status: string;
  created_at: string;
}

export interface Donation {
  id: number;
  member_id: number;
  member_name?: string;
  amount: number;
  type: string;
  date?: string;
  created_at: string;
}
