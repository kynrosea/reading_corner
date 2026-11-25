import { useState, useEffect, useContext } from 'react'
import { UserContext } from '../context/UserContext';
import { Link } from 'react-router';
import './Rewards.css';


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
				const errorData = await response.json();
				throw new Error(errorData.error);
			}

			const data: Butterfly[] = await response.json();
			if (data.data == null) {
				setButterflies(data);
			} else {
				setButterflies(data.data);
			}
			console.log(data);
		} catch (error) {
			console.error(error);
			alert(error.message);
		}
	}

	async function makeWish() {
		if (!user || loading) return;
		if (leaves < 100) {
			alert('Need 100 leaves to make a wish! Read more books to earn more!');
			return;
		}

		setLoading(true);
		setMessage('');

		try {
			const response = await fetch(`/rewards/wish/${encodeURIComponent(user!.username)}`, {
				method: 'PUT'
			});

			const data = await response.json();

			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(errorData.error);
			}

			const result = data as WishResponse;

			setLatestReward(result.reward);
			setLeaves(result.remaining_leaves);
			setMessage(`You received ${result.reward.species}!`);
			loadRewards();
		} catch (error) {
			console.error(error);
			alert(error.message);
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
				const errorData = await response.json();
				throw new Error(errorData.error);
			}

			const data = await response.json();
			setLeaves(data.leaf_balance);
		} catch (error) {
			console.error(error);
			alert(error.message);
		}
	}

	useEffect(() => {
		if (!user) return;

		void loadRewards();
		void loadLeaves();

	}, [user]);
	
	if (!user) {
		return (
			<div className='login-prompt'>
				<h1>Butterfly Garden</h1>
				<p>Please log in to view your garden.</p>
				<Link to='/login'>
					<button className='basic-button'>Go to Login</button>
				</Link>
				
			</div>
		);
	}
	

	return (
		<div className='wish-container'>
			<h1>Butterfly Garden 🦋💮</h1>
					
			<div className='wish'>
				<h2>Leaves: {leaves} 🍃</h2>

				<button onClick={makeWish} disabled={loading}>
					{loading ? 'Making a wish...' : 'Make a wish - 100 Leaves'}
				</button>
			</div>
			{latestReward && (
					<div className='reward-card'>
						<h3>You received: {latestReward.species}!</h3>
						<p>Rarity: {latestReward.rarity}</p>
					</div>
				
			)}

			<div className='collection-1'>
				{(butterflies == null || butterflies.length === 0) ? (
					<h3>You haven't collected any butterflies yet!</h3>
				) : (
					<div className='collection'>
						{butterflies.map((butterfly) => (
							<div className='butterfly-card' key={butterfly.reward_id}>
								<h3>{butterfly.species}</h3>
								<p>Rarity: {butterfly.rarity}</p>
								<p>Duplicates: {butterfly.duplicate_count}</p>
							</div>
						))}		
					</div>
				)}
			</div>
		</div>
	);
}

export default Rewards;
