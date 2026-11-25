import { useState } from 'react';
import { useNavigate } from 'react-router';
import type { Book } from '../types/book.ts';
import './AddBook.css';

function AddBook() {
	const navigate = useNavigate();

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
			alert('Book added successfully!');
			navigate('/browse');
		} catch (error) {
			console.error(error);
			alert(error.message)
		}
	}

	return (
		<main>
			<div className='add-container'>
				<h1>Enter details below to add book</h1>
				<form className='add-block' onSubmit={handleSubmit}>
					<div className='add-form'>
						<div className='input-section'>
							<label htmlFor='title'>Title: </label>
							<input type='text' id='title' name='title' required />
						</div>
						<div className='input-section'>
							<label htmlFor='author'>Author: </label>
							<input type='text' id='author' name='author' required />
						</div>
						<div className='input-section'>
							<label htmlFor='publication_year'>Publication Year: </label>
							<input type='number' id='publication_year' name='publication_year' required />
						</div>
						<div className='input-section'>
							<label htmlFor='synopsis'>Synopsis: </label>
							<textarea id='synopsis' name='synopsis' rows='5' cols='30' />
						</div>
						<div className='input-section'>
							<label htmlFor='isbn'>ISBN: </label>
							<input type='text' id='isbn' name='isbn' />
						</div>
						<div className='input-section'>
							<label htmlFor='page_count'>Pages: </label>
							<input type='number' id='page_count' name='page_count' />
						</div>
						<div className='input-section'>
							<label htmlFor='cover'>Cover: </label>
							<input type='file' accept='.jpg, .png' id='cover' name='cover' />
						</div>
					</div>
					<div className='submit-actions'>
						<input className='basic-button' type='submit' value='Submit' />
						<input className='basic-button' type='reset' value='Reset' />
					</div>

				</form>
			</div>
			
		</main>
	);
}

export default AddBook;
