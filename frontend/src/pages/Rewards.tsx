import { useState, useEffect, useContext } from 'react'
import { UserContext } from '../context/UserContext';


interface Butterfly {
	reward_id: number;
	species: string;
	rarity: string;
	image_url: string | null;
	description: string;
	duplicate_count: number;
}

interface WishResponse {
	reward: Butterfly;
	remaining_leaves: number;
}

function Rewards() {
	const context = useContext(UserContext);

	const [latestReward, setLatestReward] = useState<Butterfly | null>(null);
	const [butterflies, setButterflies] = useState<Butterfly[]>([]);
	const [message, setMessage] = useState('');
	const [loading, setLoading] = useState(false);

	const user = context?.user;
	const [leaves, setLeaves] = useState(0);
	
	async function loadRewards() {
		try {
			const response = await fetch(
				`/rewards/${encodeURIComponent(user!.username)}`
			);

			if (!response.ok) {
				throw new Error('Could not load user rewards')
			}

			const data: Butterfly[] = await response.json();

			setButterflies(data);
		} catch (error) {
			console.error(error);
			setMessage("Unable to load your butterflies.");
		}
	}

	useEffect(() => {
		if (!user) return;

		
		void loadRewards();
		void loadLeaves();
		
	}, [user]);

	async function makeWish() {
		if (!user || loading) return;

		setLoading(true);
		setMessage('');

		try {
			const response = await fetch(`/rewards/wish/${encodeURIComponent(user!.username)}`, {
				method: 'PUT'
			});

			const data = await response.json();

			if (!response.ok) {
				throw new Error(data.message ?? 'Unable to make a wish');
			}

			const result = data as WishResponse;

			setLatestReward(result.reward);
			setLeaves(result.remaining_leaves);
			setMessage(`You received ${result.reward.species}!`);
		} catch (error) {
			setMessage(
				error instanceof Error ? error.message : 'Something went wrong'
			);
		} finally {
			setLoading(false);
		}
	}

	async function loadLeaves() {
		try {
			const response = await fetch(
				`/users/${encodeURIComponent(user!.username)}`
			);

			if (!response.ok) {
				throw new Error('Could not load leaf balance');
			}

			const data = await response.json();
			setLeaves(data.leaf_balance);
		} catch (error) {
			console.error(error);
			setMessage('Unable to load your leaf balance.');
		}
	}

	if (!user) {
		return <p>Please log in to view your rewards.</p>
	}

	return (
		<main>
			<h1>Butterfly Garden 🦋💮</h1>
			<h2>Leaves: {leaves} 🍃</h2>

			<button onClick={makeWish} disabled={loading || leaves < 100}>
				{loading ? 'Making a wish...' : 'Make a wish - 100 Leaves'}
			</button>
			{latestReward && (
				<div>
					<h3>You received: {latestReward.species}!</h3>
					<p>Rarity: {latestReward.rarity}</p>
				</div>
			
			)}

			<p>{message}</p>

			{butterflies.length === 0 ? (
				<p>You haven't collected any butterflies yet!</p>
			) : (
				<div>
					{butterflies.map((butterfly) => (
						<div key={butterfly.reward_id}>
							<h3>{butterfly.species}</h3>
							<p>Rarity: {butterfly.rarity}</p>
							<p>Duplicates: {butterfly.duplicate_count}</p>
						</div>
					))}		
				</div>
			)}
		</main>
	);
}

export default Rewards;
