import type { Preference } from './preference.ts';

// interface for user object
export interface User {
	user_id: number,
	username: string,
	email: string,
	first_name: string,
	last_name: string,
	leaf_balance: number,
	profile_visibility: string,
	birth_date: string,
	preferences: Preference[]
}
