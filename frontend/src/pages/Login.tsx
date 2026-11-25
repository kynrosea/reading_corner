import { useState, useContext } from 'react';
import type { User } from '../types/user.ts';
import { UserContext } from '../context/UserContext';
import { useNavigate } from 'react-router';
import './Login.css';

function Login() {
	const navigate = useNavigate();
	const userContext = useContext(UserContext);

	if (!userContext) {
		throw new Error('UserContext must be used within UserProvider');
	}

	const { user, setUser } = userContext;

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
				const errorData = await response.json();
				throw new Error(errorData.error);
			}

			const data = await response.json();
			console.log(data);
			const preferences = await setPreferences(data.username);
			const userData = {
				user_id: data.user_id,
				username: data.username,
				first_name: data.first_name,
				last_name: data.last_name,
				email: data.email,
				birth_date: data.birth_date,
				profile_visibility: data.profile_visibility,
				preferences
			}
			
			setUser(userData);
			navigate('/');
				
		} catch (error) {
			console.error(error);
			alert(error.message);
		}
	}

	async function setPreferences(username) {
		try {
			const response = await fetch(`/users/preferences/${encodeURIComponent(username)}`);

			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(errorData.error);
			}

			const data: Preference[] = await response.json();
			return data;
		} catch(error) {
			console.error(error);
			alert(error.message);
		}
	}


	return (
		<main className='login-container'>
			<h1>Welcome back!</h1>
			<UserContext value={user}>
				<form className='login-form' onSubmit={handleLogin}>
					<h2>Enter Login Details Below</h2>
					<label htmlFor='username'>Username: </label>
					<input type='text' id='username' name='username' />
					<label htmlFor='email'>Email: </label>
					<input type='email' id='email' name='email' />
						
					<button className='login-button' type='submit'>Login</button>
				</form>
			</UserContext>
		</main>
	);
}

export default Login;
