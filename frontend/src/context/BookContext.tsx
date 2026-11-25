import type { Book } from '../types/book.ts';
import { createContext, useState, useEffect, ReactNode } from 'react';

interface BookContextType {
	// either a valid book obj or no book
	book: Book | null;

	// updates selected book
	// accepts a book or null and returns nothing useful
	setBook: (book: Book | null) => void;
}

interface BookProviderProps {
	children: ReactNode,
}

export const BookContext = createContext<BookContextType | null>(null);

export function BookProvider({ children }: BookProviderProps) {
	const [book, setBook] = useState<Book | null>(() => {
		const savedBook = sessionStorage.getItem('book');
		return savedBook ? JSON.parse(savedBook) as Book : null;
	});

	useEffect(() => {
		if (book) {
			sessionStorage.setItem('book', JSON.stringify(book));
		} else {
			sessionStorage.removeItem('book');
		}
	}, [book]);

	return (
		<BookContext.Provider value={{ book, setBook }}>
			{ children }
		</BookContext.Provider>
	);
}
