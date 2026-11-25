import { useContext } from 'react';
import { UserContext } from '../context/UserContext';
import { useNavigate } from 'react-router';
import type { User } from '../types/user.ts';
import './Signup.css';

function Signup() {

	const navigate = useNavigate();
	const userContext = useContext(UserContext);

	if (!userContext) {
		throw new Error('UserContext must be used within UserProvider');
	}
	
	const { setUser } = userContext;

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

			if (!response.ok) {
				const errorData = await response.json();
				let errorMessage = 'User could not be added';
				throw new Error(errorData.error || errorMessage);
			}
			const user: User = await response.json();
			console.log(user);
			setUser(user);
			navigate('/my-preferences');
			
		} catch (error) {
			console.error(error);
			alert(error.message);
		}
	}

	
	return (
		<main className='signup-container'>
			<h1>Enter signup details below</h1>
			<form className='signup-form' onSubmit={handleSignup}>
				<label htmlFor='username'>Username: </label>
				<input type='text' id='username' name='username' required />
				<label htmlFor='first_name'>First Name: </label>
				<input type='text' id='first_name' name='first_name' required />
				<label htmlFor='last_name'>Last Name: </label>
				<input type='text' id='last_name' name='last_name' required />
				<label htmlFor='email'>Email: </label>
				<input type='email' id='email' name='email' required />
				<label htmlFor='birth_date'>Birthday: </label>
				<input type='date' id='birth_date' name='birth_date' required />
				<input className='basic-button' type='submit' value='Sign Up' />
			</form>
		</main>
	);
}

export default Signup;
