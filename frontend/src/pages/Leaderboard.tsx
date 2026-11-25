import { useEffect, useState } from 'react';
import './Leaderboard.css';

interface Record {
	username: string,
	books_completed: number
}

function Leaderboard() {

	const [records, setRecords] = useState<Record[]>([]);
	const [message, setMessage] = useState('');

	async function getLeaderboard() {
		try {
			const response = await fetch('/users/leaderboard');
			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(errorData.error);
			}

			const data: Record[] = await response.json();

			if (data.length === 0) {
				setMessage('No users on public leaderboard');
			}

			console.log(data);
			setRecords(data);
		} catch (error) {
			console.error(error);
			alert(error.message);
		}
	}

	useEffect(() => {
		getLeaderboard();
	}, []);

	return (
		<main className='leaderboard-container'>
			<h1>2026 Reading Leaderboard</h1>
			<div className='leaderboard'>
				{records.map((record, index) => (
					<div className='leaderboard-entry'>
						<div className='leaderboard-rank'>
							<h2>#{index+1}</h2>
						</div>
						<div className='leaderboard-user'>
							<h3>{record.username}</h3>
						</div>
						<div className='leaderboard-score'>
							<p>{record.books_completed}</p>
							<p>books finished</p>
						</div>
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
