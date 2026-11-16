import { useState } from 'react';
import type { Book } from '../types/book.ts';

function AddBook() {

	const [message, setMessage] = useState('');
	const [error, setError] = useState('');

	async function handleSubmit(e) {
		e.preventDefault();

		const form = e.target;
		const formData = new FormData(form);
		const title = formData.get('title');
		const author = formData.get('author');
		const publication_year = formData.get('publication_year');
		const synopsis = formData.get('synopsis');
		const isbn = formData.get('isbn');
		const page_count = formData.get('page_count');
		const cover = formData.get('cover');

		const bookData = {
			title,
			author,
			publication_year,
			synopsis,
			isbn,
			page_count,
			cover
		}

		try {
			const response = await fetch('/books/book', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify(bookData),
			});

			if (response.status === 400) {
				setError('Check input fields and try again.');
			} else if (!response.ok) {
				throw new Error('Failed to add book');
			}

			console.log('Book insertion success!');
			setMessage('Book added successfully!');
			setError('');
		} catch (error) {
			console.error(error)
			setError('Book could not be added :(');
		}
	}

	async function handleDelete(e) {

		e.preventDefault();
		const form = e.target;
		const formData = new FormData(form);
		const title = formData.get('title');
		const author = formData.get('author');

		try {
			const response = await fetch(`/books/book?title=${title}&author=${author}`, {
				method: 'DELETE',
			});

			if (!response.ok) {
				throw new Error('Failed to delete book');
			}

			console.log('Book delete successful');
			setMessage('Book deleted successfully!');
			setError('');
		} catch (error) {
			console.error(error);
			setError('Book could not be deleted :(');
		}
	}

	return (
		<main>
			<div>
				<h2>Enter details below to add book</h2>
				<form onSubmit={handleSubmit}>
					<label htmlFor='title'>Title: </label>
					<input type='text' id='title' name='title' required />
					<br />
					<label htmlFor='author'>Author: </label>
					<input type='text' id='author' name='author' required />
					<br />
					<label htmlFor='publication_year'>Publication Year: </label>
					<input type='number' id='publication_year' name='publication_year' required />
					<br />
					<label htmlFor='synopsis'>Synopsis: </label>
					<textarea id='synopsis' name='synopsis' rows='5' cols='30' />
					<br />
					<label htmlFor='isbn'>ISBN: </label>
					<input type='text' id='isbn' name='isbn' />
					<br />
					<label htmlFor='page_count'>Pages: </label>
					<input type='number' id='page_count' name='page_count' />
					<br />
					<label htmlFor='cover'>Cover: </label>
					<input type='file' accept='.jpg, .png' id='cover' name='cover' />
					<br />
					<input type='submit' value='Submit' />
					<input type='reset' value='Reset' />
					<br />
					{error && (
						<div className='error-banner' role='alert'>
							{error}
						</div>
					)}

					{message && (
						<div className='message-banner' role='alert'>
							{message}
						</div>
					)}
				</form>
			</div>
			<br />
			<br />
			<div>
				<h2>Enter title and author below to delete book</h2>
				<form onSubmit={handleDelete}>
					<label htmlFor='title'>Title: </label>
					<input type='text' id='title' name='title' required />
					<br />
					<label htmlFor='author'>Author: </label>
					<input type='text' id='author' name='author' required />
					<br />
					<input type='submit' value='DELETE' />
					<br />
					{error && (
						<div className='error-banner' role='alert'>
							{error}
						</div>
					)}
					
					{message && (
						<div className='message-banner' role='alert'>
							{message}
						</div>
					)}
				</form>
			</div>
		</main>
	);
}

export default AddBook;
