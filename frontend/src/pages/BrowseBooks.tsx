import { useEffect, useState } from 'react';
import { Link } from 'react-router';
import type { Book } from '../types/book.ts';


function BrowseBooks() {

	//const [title, setTitle] = useState('');
	//const [author, setAuthor] = useState('');

	// we want an array of book objects
	// the initial value is an empty array
	const [books, setBooks] = useState<Book[]>([]);
	const [showBooks, setShowBooks] = useState(false);
	const [error, setError] = useState('');

	async function getBooks() {

		try {
			const response = await fetch('/books/');

			if (!response.ok) {
				throw new Error('Failed to retrieve books');

			}

			const data: Book[] = await response.json();

			console.log(data);
			setBooks(data);
			setShowBooks(true);
			setError('');
		} catch (error) {
			console.error(error)
			setError('Could not load books.');
		}

	}

	// () => {} is the setup param
	// [] tells react that the effect doesn't depend on any changing props or state values
	useEffect(() => {
		getBooks();

	}, []);

	async function handleSearch(e) {
		e.preventDefault();
		const form = e.target;
		const formData = new FormData(form);
		const title = formData.get('title');
		const author = formData.get('author');

		try {
			const response = await fetch(`/books/browse?title=${title}&author=${author}`);

			if (!response.ok) {
				throw new Error('Failed to query books');
			}

			const data: Book[] = await response.json();
			console.log(data)
			setBooks(data);
			setShowBooks(true);
			setError('');

		} catch (error) {

			console.error(error)
			setError('Could not search books');
		}
	}

	return (
		<main>
			<h1>Browse Books</h1>
			<div>
				<h2>Search</h2>
				<form onSubmit={handleSearch}>
					<label htmlFor='title'>Title: </label>
					<input type='text' id='title' name='title' />
					<br />
					<label htmlFor='author'>Author: </label>
					<input type='text' id='author' name='author' />
					<br />
					<input type='submit' value='Submit' />
					<button type='reset' onClick={getBooks}>Reset</button>
				</form>
				<br />
				<h2>Can't find a book? Click below to add it!</h2>
				<Link to='/add-book'>
					<button>Add Book</button>
				</Link>
			</div>
			<div>
				{books.map((book) => (
					<div key={book.book_id}>
						<h3>{book.title}</h3>
						<p>{book.author}</p>
					</div>
				))}
			</div>
		</main>
	);

}

export default BrowseBooks;
