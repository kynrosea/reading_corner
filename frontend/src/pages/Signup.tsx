import { useEffect, useState, useContext } from 'react';
import { UserContext } from '../context/UserContext';
import { useNavigate } from 'react-router';
import type { User } from '../types/user.ts';

function Signup() {

	const navigate = useNavigate();
	const userContext = useContext(UserContext);

	if (!userContext) {
		throw new Error('UserContext must be used within UserProvider');
	}
	
	const { user, setUser } = userContext;
	const [message, setMessage] = useState('');
	const [error, setError] = useState('');

	async function handleSignup(e) {
		e.preventDefault();
		const form = e.target;
		const formData = new FormData(form);
		const username = formData.get('username');
		const first_name = formData.get('first_name');
		const last_name = formData.get('last_name');
		const email = formData.get('email');
		const birth_date = formData.get('birth_date');
		const now: Date = new Date();
		const creation_date: string = now.toLocaleDateString('en-CA');

		const userData = {
			username,
			first_name,
			last_name,
			email,
			birth_date,
			creation_date
		}

		try {
			const response = await fetch(`/users/signup`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(userData)
			});

			if (response.status === 400) {
				setError('Check input fields and try again!');
			} else if (!response.ok) {
				throw new Error('Failed to add user');
			}
			const user: User = await response.json();
			console.log(user);
			setUser(user);
			setError('');
			navigate('/');
			
		} catch (error) {
			console.error(error)
			setError('User could not be added :(');
		}
	}
	
	return (
		<main>
			<h1>Enter signup details below</h1>
			<UserContext value={user}>
				<form onSubmit={handleSignup}>
					<label htmlFor='username'>Username: </label>
					<input type='text' id='username' name='username' required />
					<br />
					<label htmlFor='first_name'>First Name: </label>
					<input type='text' id='first_name' name='first_name' required />
					<br />
					<label htmlFor='last_name'>Last Name: </label>
					<input type='text' id='last_name' name='last_name' required />
					<br />
					<label htmlFor='email'>Email: </label>
					<input type='email' id='email' name='email' required />
					<br />
					<label htmlFor='birth_date'>Birthday: </label>
					<input type='date' id='birth_date' name='birth_date' required />
					<br />
					<br />
					<input type='submit' value='SIGN UP' />
					<br />
					<br />
					{error && (
						<div className='error-banner' role='alert'>
							{error}
						</div>
					)}
				</form>
				
			</UserContext>
		</main>
	);
}

export default Signup;
