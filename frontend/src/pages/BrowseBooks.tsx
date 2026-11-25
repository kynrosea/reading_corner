import { useEffect, useState, useContext } from 'react';
import { UserContext } from '../context/UserContext';
import { Link, useNavigate } from 'react-router';
import type { Book } from '../types/book.ts';
import './BrowseBooks.css';


function BrowseBooks() {

	//const [title, setTitle] = useState('');
	//const [author, setAuthor] = useState('');
	const userContext = useContext(UserContext);
	if (!userContext) {
		throw new Error('BrowseBooks must be used within UserProvider');
	}

	const navigate = useNavigate();
 
	// we want an array of book objects
	// the initial value is an empty array
	const [books, setBooks] = useState<Book[]>([]);
	const [showBooks, setShowBooks] = useState(false);
	const [message, setMessage] = useState('');
	
	const [libraryInfo, setLibraryInfo] = useState<Book[]>([]);

	const { user } = userContext;

	async function getBooks() {

		try {
			const response = await fetch('/books/');

			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(errorData.error);

			}

			const data: Book[] = await response.json();

			//console.log(data);
			
			setBooks(data);
			setShowBooks(true);
		} catch (error) {
			console.error(error)
			alert(error.message);
		}

	}

	async function getLibraryInfo() {
		try {
			const response = await fetch(
				`/library/${encodeURIComponent(user.username)}`
			)

			if (!response.ok) {
				const errorData = await response.json();
				let errorMessage = 'Could not load user\'s library info';
				throw new Error(errorData.error || errorMessage)
			}

			const data: Book[] = await response.json();
			//console.log(data);
			setLibraryInfo(data);
		} catch (error) {
			console.error(error);
			alert(error.message);
		}
	}

	function hasBook(title, author) {
		if (libraryInfo.some(book => (book.title===title, book.author===author))) {
			return true;
		} else {
			return false;
		}
	}

	async function addLibraryBook(title, author) {
		try {

			const status='tbr';
			const response = await fetch(
				`/library/${encodeURIComponent(user.username)}/${encodeURIComponent(author)}/${encodeURIComponent(title)}`,
				{
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify({status})
				}
			)

			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(errorData.error);
			}

			navigate('/my-library');
		} catch (error) {
			console.error(error);
			alert(error.message);
		}
	}

	// () => {} is the setup param
	// [] tells react that the effect doesn't depend on any changing props or state values
	useEffect(() => {
		if (!user) return;
		getBooks();
		getLibraryInfo();

	}, [user]);

	async function handleSearch(e) {
		e.preventDefault();
		const form = e.target;
		const formData = new FormData(form);
		const title = formData.get('title');
		const author = formData.get('author');

		try {
			const response = await fetch(`/books/browse?title=${title}&author=${author}`);

			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(errorData.error);
			}

			const data: Book[] = await response.json();
			//console.log(data)
			if (data.length === 0) {
				setMessage('No results match query!');
			} else {
				setMessage('');
			}	
		
			setBooks(data);
			setShowBooks(true);

		} catch (error) {

			console.error(error);
			alert(error.message);
		}
	}

	async function handleFilter() {

		if (user.preferences == null) {
			alert('Your preferences have not been defined. Edit in your profile settings!');
			return;
		} else if (user.preferences.length <= 0) {
			alert('Your preferences have not been defined. Edit in your profile settings!');
			return;
		}
		
		try {
			if (!user) {
				alert('Must be logged in to filter by preferences!');
				return;
			}
			const response = await fetch(
				`/books/filter/${encodeURIComponent(user.username)}`
			);

			if (!response.ok) {
				const errorData = await response.json()
				throw new Error(errorData.error);
			}

			const data: Book[] = await response.json();
			if (data === []) {
				return;
			}
			setBooks(data);
			setShowBooks(true);
			console.log(data);
			console.log('Preferences: ', user.preferences);
			
		} catch(error) {
			console.error(error);
			alert(error.message);
		}
	}

	return (
		<main className='browse-container'>
			<h1>Browse Books</h1>
			<div className='browse-search'>
				<h2>Search</h2>
				<form className='search-form' onSubmit={handleSearch}>
					<div className='search-field'>
						<label htmlFor='title'>Title: </label>
						<input type='text' id='title' name='title' />
					</div>
					<div className='search-field'>
						<label htmlFor='author'>Author: </label>
						<input type='text' id='author' name='author' />
					</div>
					<div className='search-actions'>
						<input type='submit' value='Submit' />
						<button type='reset' onClick={getBooks}>Reset</button>
						<button onClick={handleFilter} type='button'>Filter By Your Preferences!</button>
					</div>
				</form>
				
			</div>
			<div className='browse-add-book'>
				<section>
					<h2>Can't find a book?</h2>
					<p>Add a new book to the collection!</p>
				</section>
				<Link to='/add-book'>
					<button>Add Book</button>
				</Link>
					
			</div>
			<div className='message'>
				{message && (
					<h3>{message}</h3>
				)}
			</div>
			
			
			<div className='books-grid'>
				{books.map((book) => (
					<div className='book-card' key={book.book_id}>
						<div>
							<h3>{book.title}</h3>
							<p>{book.author}</p>
						</div>
						{!hasBook(book.title, book.author) &&
							<div>
								<button onClick={() => addLibraryBook(book.title, book.author)}>Add Book to Library</button>
							</div>
						}
						
					</div>
				))}
			</div>
		</main>
	);

}

export default BrowseBooks;
