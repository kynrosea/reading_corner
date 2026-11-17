import { useState } from 'react';
import type { Book } from '../types/book.ts';

function AddBook() {

	const [addMessage, setAddMessage] = useState('');
	const [deleteMessage, setDeleteMessage] = useState('');
	const [addError, setAddError] = useState('');
	const [deleteError, setDeleteError] = useState('');

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

			if (!response.ok) {
				const errorData = await response.json()
				let errorMessage = `Request failed with status ${response.status}`
				throw new Error(errorData.error || errorMessage);
			}

			console.log('Book insertion success!');
			setAddMessage('Book added successfully!');
			setAddError('');
		} catch (addError) {
			console.error(addError.message);
			setAddError(addError.message);
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
			setDeleteMessage('Book deleted successfully!');
			setDeleteError('');
		} catch (deleteError) {
			console.error(deleteError);
			setDeleteError('Book could not be deleted :(');
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
					{addError && (
						<div className='error-banner' role='alert'>
							{addError}
						</div>
					)}

					{addMessage && (
						<div className='message-banner' role='alert'>
							{addMessage}
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
					{deleteError && (
						<div className='error-banner' role='alert'>
							{deleteError}
						</div>
					)}
					
					{deleteMessage && (
						<div className='message-banner' role='alert'>
							{deleteMessage}
						</div>
					)}
				</form>
			</div>
		</main>
	);
}

export default AddBook;
