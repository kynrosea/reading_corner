import { useEffect, useState } from 'react';

interface Record {
	username: string,
	books_completed: number
}

function Leaderboard() {

	const [records, setRecords] = useState<Record[]>([]);
	const [showRecords, setShowRecords] = useState(false);
	const [message, setMessage] = useState('');
	const [error, setError] = useState('');

	async function getLeaderboard() {
		try {
			const response = await fetch('/rewards/leaderboard');
			if (!response.ok) {
				throw new Error('Failed to retrieve leaderboard');
			}

			const data: Record[] = await response.json();

			if (data === []) {
				setMessage('No users on public leaderboard');
			}

			console.log(data);
			setRecords(data);
			setShowRecords(true);
			setError('');
		} catch (error) {
			console.error(error)
			setError('Could not load leaderboard');
		}
	}

	useEffect(() => {
		getLeaderboard();
	}, []);

	return (
		<main>
			<h1>2026 Reading Leaderboard</h1>
			<div>
				{records.map((record) => (
					<div>
						<h3>{record.username}</h3>
						<p>{record.books_completed}</p>
					</div>
				))}
			</div>
			{message && (
				<div className='message-banner' role='alert'>
					{message}
				</div>	
			)}	
		</main>
	);
}

export default Leaderboard;
