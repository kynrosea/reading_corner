import type { User } from '../types/user.ts';
import { createContext, useState, useEffect, ReactNode } from 'react';

interface UserContextType {
	// either a valid user obj or no user
	user: User | null;
	// updates selected user
	// accepts a user or null and returns nothing useful
	setUser: (user: User | null) => void;
}

interface UserProviderProps {
	children: ReactNode,
}

// <> tells tsx that this context will eventually contain usercontexttype object, but the default is null
export const UserContext = createContext<UserContextType | null>(null)

// children represents whatever components placed inside UserProvider
// value prop determines what other components can access through this context
// the outer braces mean eval this JS expression inside JSX
// the inner braces create a JS object containing user and setUser
export function UserProvider({ children }: UserProviderProps) {

	// () => {...} is a lazy initializer
	const [user, setUser] = useState<User | null>(() => {
		// check whether we've previously stored a user
		const savedUser = sessionStorage.getItem('user');
		// converts JSON string back into JS object
		return savedUser ? JSON.parse(savedUser) as User : null;
	});

	// runs whenever user changes
	useEffect(() => {
		if (user) {
			sessionStorage.setItem('user', JSON.stringify(user));
		} else {
			sessionStorage.removeItem('user');
		}
	}, [user]);

	return (
		<UserContext.Provider value={{ user, setUser }}>
			{children}
		</UserContext.Provider>
	);
}
