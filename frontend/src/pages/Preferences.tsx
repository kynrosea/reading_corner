import { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router';
import { UserContext } from '../context/UserContext';
import type { User } from '../types/user.ts';
import type { Preference } from '../types/preference.ts';
import './Preferences.css';

interface Tag {
	tag_id: number,
	tag_name: string
}

function Preferences() {
	
	const navigate = useNavigate();

	const userContext = useContext(UserContext);
	if (!userContext) {
		throw new Error('Preferences must be used within UserProvider');
	}

	const { user, setUser } = userContext;

	const [preference, setPreference] = useState<Preference>();
	const [preferences, setPreferences] = useState<Preference[]>([]);
	const [availableTags, setAvailableTags] = useState<Tag[]>([]);
	const [selected, setSelected] = useState<number[]>();
	
	async function getAvailableTags() {
		try {
			const response = await fetch('/tags/');

			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(errorData.error);
			}

			const data = await response.json();
			setAvailableTags(data);
			
		} catch(error) {
			console.log(error);
			alert(error.message);
		}
	}

	function addPreference(tag_id) {
		const does_like = 1;
		const preference: Preference = {
			tag_id,
			does_like
		}
		
		const my_prefs = preferences;
		my_prefs.push(preference);
		setPreferences(my_prefs);
		
	}
	
	function removePreference(tag_id) {
		const my_prefs = preferences.filter(pref => pref.tag_id !== tag_id);
		setPreferences(my_prefs);
	}
	
	async function toggleButton(tag_id: number) {
		try {
			if (selected.includes(tag_id)) {
				await removePreference(tag_id);

				setSelected(prev =>
					prev.filter(item => item !== tag_id)
				);
			} else {
				await addPreference(tag_id);

				setSelected(prev => [...prev, tag_id]);
			}
		} catch (error) {
			console.error(error);
			alert(error instanceof Error
				? error.message
				: "Unable to update preferences");
		}
	}
	
	async function handleSave() {

		if (preferences.length > 7) {
			alert('Can only select at most 7 genres!');
			return;
		}
		
		let deletePrefs = [];
		if (user.preferences != null) {
			const prefs= new Set(preferences);
			deletePrefs = user.preferences.filter((item) => !prefs.has(item));
		}

		console.log('Delete: ', deletePrefs);
		setPreferences(selected);
		
		for (const delPref of deletePrefs) {
			
			try {
				
				const response = await fetch(
					`/users/preferences/${encodeURIComponent(user.username)}/${encodeURIComponent(delPref.tag_id)}`,
					{
						method: 'DELETE',
						headers: {
							'Content-Type' : 'application/json'
						},
						body: JSON.stringify(delPref)
					}
				);

				if (!response.ok) {
					const errorData = await response.json();
					throw new Error(errorData.error);
				}

				console.log('Deleted');
				
			} catch(error) {
				console.error(error);
				alert(error.message);
			}
		}
		
		for (const pref of preferences) {
			
			try {
				const response = await fetch(
					`/users/preferences/${encodeURIComponent(user.username)}`,
					{
						method: 'POST',
						headers: {
							'Content-Type' : 'application/json'
						},
						body: JSON.stringify(pref)
					}
				);

				if (!response.ok) {
					const errorData = await response.json();
					throw new Error(errorData.error);
				}
			} catch(error) {
				console.error(error);
				alert(error.message);
			}
			
		}
		
		const userData = {
			user_id: user.user_id,
			first_name: user.first_name,
			last_name: user.last_name,
			email: user.email,
			birth_date: user.birth_date,
			profile_visibility: user.profile_visibility,
			leaf_balance: user.leaf_balance,
			username: user.username,
			preferences
		}

		setUser(userData);

		console.log('Preferences: ', userData.preferences);
		alert('Preferences have been updated!');
		navigate('/');
	}
	
	useEffect(() => {
		if (!user) return;
		getAvailableTags();
		
		if (user.preferences != null && user?.preferences.length > 0) {
			const pref_ids = [];
			for (const pref of user.preferences) {
				pref_ids.push(pref.tag_id);
			}
			setSelected(pref_ids);
			console.log('selected: ', selected);
			console.log('user', user.preferences);
			setPreferences(user.preferences);
		} else {
			setSelected([]);
		}
		
	}, [user]);
	
	return (
		<main className='preference-container'>
			<h1>Set Your Preferences Here</h1>
			<div className='tag-section'>
				<h3>Click on the genres that you like!</h3>
				<p>Highlighted means you've already liked this genre</p>
				<div className='tag-buttons'>
					{availableTags.map((tag) => {
						const isActive = selected.includes(tag.tag_id);
						return (
							<button 
								key={tag.tag_id} 
								onClick={() => toggleButton(tag.tag_id)} 
								className={isActive ? 'active-tag' : 'inactive-tag'}
							>
								{tag.tag_name}
							</button>
						);
					})}
				</div>
				
			</div>
			<button className='basic-button' onClick={handleSave}>
				Save Preferences
			</button>
			
		</main>
	);
}

export default Preferences;
