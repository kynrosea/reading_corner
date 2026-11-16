import { useState, useContext, useEffect } from 'react';
import { UserContext } from '../context/UserContext';
import { Link } from 'react-router';
import EditBookStatus from '../components/EditBookStatus';

interface Record {
	book_id: number,
	title: string,
	author: string,
	status: string,
}

function Library() {

	// if userContext is null, then the component isn't receiving the context provider
	// if user is null, the provider exists but nobody has logged in yet
	const userContext = useContext(UserContext);
	if (!userContext) {
		throw new Error('Library must be used within UserProvider');
	}
	
	const [records, setRecords] = useState<Record[]>([]);
	const [showRecords, setShowRecords] = useState(false);
	const [error, setError] = useState('');
	
	const { user } = userContext;

	
	async function getLibrary() {
		try {
			
			if (!user) {
				throw new Error('User must be logged in');
			}
			
			const response = await fetch(
				`/library/${encodeURIComponent(user.username)}`
			);

			if (!response.ok) {
				throw new Error('Failed to retrieve library');
			}

			const data: Record[] = await response.json();

			console.log(data);
			setRecords(data);
			setShowRecords(true);
			setError('');

			
		} catch (error) {
			console.error(error);
			setError('Could not load library');
		}
	}

	
	// must tell react to rerun the effect when the selected user changes
	useEffect(() => { 
		if (!user) return;
	
		getLibrary(); 
		
	}, [user]);
	
	if (!user) {
		return (
			<main>
				<h1>My Library</h1>
				<p>Please log in to view your library.</p>
				<Link to='/login'>
					<button>Go to Login</button>
				</Link>
			</main>
		)
	}

	return (
		<main>
			<header>
				<Link to='/'>
					<button>Home</button>
				</Link>
			</header>
			<h1>Welcome to your personal library!</h1>
			<div>
				{records.map((record) => (
					<div key={record.book_id}>
						<h3>{record.title}</h3>
						<p>{record.author}</p>
						
						<EditBookStatus
							username={user.username}
							title={record.title}
							author={record.author}
							currentStatus={record.status}
							onUpdated={getLibrary}
						 />
					</div>
				))}
			</div>
		</main>
	);
}

export default Library;
