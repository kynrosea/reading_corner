import { useState, useContext, useEffect } from 'react';
import { Link } from 'react-router';
import type { User } from '../types/user.ts';
import { UserContext } from '../context/UserContext';
import './Profile.css';

function Profile() {
	
	const userContext = useContext(UserContext);
	if (!userContext) {
		throw new Error('UserContext must be used within UserProvider');
	}

	const { user, setUser } = userContext;

	async function handleUpdateUser(e) {
		e.preventDefault();
		const form = e.target;
		const formData = new FormData(form);
		const first_name = formData.get('first_name');
		const last_name = formData.get('last_name');
		const profile_visibility = formData.get('profile_visibility');

		const userData = {
			first_name,
			last_name,
			profile_visibility
		}

		try {
			if (!user) return;
			const response = await fetch(
				`/users/settings/${encodeURIComponent(user.username)}`,
				{
					method: 'PUT',
					headers: {
						'Content-Type' : 'application/json'
					},
					body: JSON.stringify(userData)
				}
			);

			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(errorData.error);
			}

			const data: User = await response.json();
			
			const updateUserData = {
				username: data.username,
				first_name: data.first_name,
				last_name: data.last_name,
				email: data.email,
				user_id: data.user_id,
				leaf_balance: data.leaf_balance,
				profile_visibility: data.profile_visibility,
				birth_date: data.birth_date,
				preferences: user.preferences
			}

			setUser(updateUserData);
			alert('Profile updated!!');
			console.log(user.profile_visibility);
			
		} catch(error) {
			console.log(error);
			alert(error.message);
		}
	}


	useEffect(() => {
		if (!user) return;
	
	}, [user]);

	if (!user) {
		return (
			<div className='login-prompt'>
				<h1>Profile Settings</h1>
				<p>Please log in to view your profile settings.</p>
				<Link to='/login'>
					<button className='basic-button'>Go to Login</button>
				</Link>
				
			</div>
		);
	}
	
	return (
		<main className='profile-container'>
			<h1>Profile Settings</h1>
			<form onSubmit={handleUpdateUser} className='profile-form'>
				<div>
					<span>
						<label htmlFor='username'>Username: </label>
						<input id='username' name='username' defaultValue={user.username} disabled />
					</span>
					<span>
						<label htmlFor='email'>Email: </label>
						<input id='email' name='email' defaultValue={user.email} disabled />
					</span>
				</div>
				<div>
					<span>
						<label htmlFor='first_name'>First Name: </label>
						<input id='first_name' name='first_name' defaultValue={user.first_name} />
					</span>
					<span>
						<label htmlFor='last_name'>Last Name: </label>
						<input id='last_name' name='last_name' defaultValue={user.last_name} />
					</span>
				</div>
				<div>
					<span>
						<label htmlFor='profile_visibility'>Profile Visibility: </label>
						<select id='profile_visibility' name='profile_visibility' defaultValue={user.profile_visibility}>
							<option value='private'>Private</option>
							<option value='public'>Public</option>
						</select>
					</span>
				</div>
				<Link to='/my-preferences'>
					<button className='basic-button'>Edit Book Preferences</button>
				</Link>
				<input className='basic-button' type='submit' value='Save Changes' />
				
			</form>
		</main>
	
	);
}

export default Profile;
