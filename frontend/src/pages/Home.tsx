import { Link } from 'react-router';
import { useState, useContext, useEffect } from 'react';
import { UserContext } from '../context/UserContext';
import './Home.css';

function Home() {

	const userContext = useContext(UserContext);
	if (!userContext) {
		throw new Error('Home must be used within UserProvider');
	}
	
	let defaultWelcome = 'Welcome to your cozy reading corner!'
	const [welcomeMessage, setWelcomeMessage] = useState(defaultWelcome)
	const [loginStatus, setLoginStatus] = useState(false);
	const { user } = userContext;

	useEffect(() => {
		if (user) {
			setLoginStatus(true);
			setWelcomeMessage(`Welcome back to your cozy reading corner, ${user.first_name}!`);
		}
	}, []) // empty array so it only runs once on mount

	// contains the browse books button
	// app passes a function to here
	// that function is called when button is clicked
	//
	function Welcome() {

		if (!loginStatus) {
			return (
				<div>
					<h1>{welcomeMessage}</h1>
					<br />
					<Link to='/login'>
						<button>Log In</button>
					</Link>
					<Link to='/signup'>
						<button>Sign Up</button>
					</Link>
					<br />
				</div>	
			);
		} else {

			return (
				<div>
					<h1>{welcomeMessage}</h1>
				</div>
			);
		}
	}
	
	return (
		<div className='home-container'>
			<section className='home-welcome'>
				<Welcome />
			</section>
			<section className='home-features'>
				<div className='feature-grid'>
					<Link className='feature-card' to='/browse'>
						<h3>Browse Books</h3>
						<p>
							Discover your next favorite book.
							View a list of all available books to read.
						</p>
					</Link>
					<Link className='feature-card' to='/my-library'>
						<h3>Personal Library💮</h3>
						<p>
							Curate your tastes.
							Review your personal library.
						</p>
					</Link>
					<Link className='feature-card' to='/butterfly-garden'>
						<h3>Butterfly Garden🦋</h3>
						<p>
							Collect rewards and build your garden.
						</p>
					</Link>
					<Link className='feature-card' to='/leaderboard'>
						<h3>2026 Leaderboard</h3>
						<p>
							See who's dominating in reading this year.
						</p>
					</Link>
				</div>
			</section>
			<br />
		</div>
	);

}

export default Home;

