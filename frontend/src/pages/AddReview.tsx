import { useState, useEffect, useContext } from 'react';
import type { Book } from '../types/book.ts';
import { UserContext } from '../context/UserContext';
import { useNavigate } from 'react-router';
import './AddReview.css';

function AddReview() {
	const navigate = useNavigate();
	const userContext = useContext(UserContext);
	if (!userContext) {
		throw new Error('Library must be used within UserProvider');
	}

	const [books, setBooks] = useState<Book[]>([]);
	const [addMessage, setAddMessage] = useState('');

	const { user } = userContext;
	
	async function getBooks() {

		try {
			const response = await fetch(`/library/${encodeURIComponent(user.username)}`);

			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(errorData.error);

			}

			const data: Book[] = await response.json();

			console.log(data);
			
			setBooks(data);
		} catch (error) {
			console.error(error);
			alert(error.message);
		}

	}


	async function addReview(e) {
		e.preventDefault();
		const form = e.target;
		const formData = new FormData(form);
		const book_id = formData.get('book_id');
		const rating = formData.get('rating');
		const visibility = formData.get('visibility');
		const now: Date = new Date();
		const creation_date: string = now.toLocaleDateString('en-CA');

		const reviewData = {
			book_id,
			rating,
			visibility,
			creation_date,
		}

		try {
			const response = await fetch (
				`/reviews/user/${encodeURIComponent(user.username)}`, {
					method: 'POST',
					headers: {
						'Content-Type' : 'application/json',
					},
					body: JSON.stringify(reviewData),
				}
				
			);

			if (!response.ok) {
				const errorData = await response.json();
				let errorMessage = `Request failed with status ${response.status}`;
				throw new Error(errorData.error || errorMessage);
			}

			console.log('Review added successfully!');
			setAddMessage('Review added successfully!');
			navigate('/my-reviews');
		} catch (error) {
			console.error(error);
			alert(error.message);
		}
		
	}

	useEffect(() => {
		if (!user) return;
		getBooks();
	}, [user]);

	return (
		<main className='add-review'>
			<h1>Add Review for a book here!</h1>
			<form onSubmit={addReview}>
				<div className='form-field'>
					<label htmlFor='book_id'>Book: </label>
					<select name='book_id' required>
						{books.map((book) => (
							<option key={book.book_id} value={book.book_id}>
								{book.title} by {book.author}
							</option>
						))}
					</select>
				</div>

				<div className='form-field'>
					<label htmlFor='rating'>Rating: </label>
					<input type='range' id='rating' name='rating' min='1' max='5' />
				</div>
				<div className='form-field'>
					<label htmlFor='visibility'>Visibility: </label>
					<select id='visibility' name='visibility'>
						<option value='public'>Public</option>
						<option value='private'>Private</option>
					</select>
				</div>
				<div>
					<input className='basic-button' type='submit' value='Submit' />
				</div>
			</form>
			<p>{addMessage}</p>
		</main>
	);
		
}

export default AddReview;
