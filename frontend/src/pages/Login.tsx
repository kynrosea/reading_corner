import { useState, useContext } from 'react';
import type { User } from '../types/user.ts';
import { UserContext } from '../context/UserContext';
import { useNavigate } from 'react-router';

function Login() {
	const navigate = useNavigate();
	const userContext = useContext(UserContext);

	if (!userContext) {
		throw new Error('UserContext must be used within UserProvider');
	}

	const { user, setUser } = userContext;
	const [error, setError] = useState('');

	async function handleLogin(e) {
		e.preventDefault();
		const form = e.target;
		const formData = new FormData(form);
		const username = formData.get('username');
		const email = formData.get('email');

		const userData = {
			username,
			email
		}

		try {
			const response = await fetch(`/users/login?username=${username}&email=${email}`)
			
			if (!response.ok) {
				throw new Error('Failed to retrive user');
			}

			const user: User = await response.json();
			console.log(user);
			setUser(user);
			setError('');
			navigate('/my-library');
				
		} catch (error) {
			console.error(error)
			setError('Could not load user');
		}
	}


	return (
		<main>
			<h1>Welcome back!</h1>
			<h2>Enter Login Details Below</h2>
			<UserContext value={user}>
				<form onSubmit={handleLogin}>
					<label htmlFor='username'>Username: </label>
					<input type='text' id='username' name='username' />
					<br />
					<label htmlFor='email'>Email: </label>
					<input type='email' id='email' name='email' />
					<br />
					<input type='submit' value='Login' />
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

export default Login;
