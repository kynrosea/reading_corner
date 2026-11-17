import { Link } from 'react-router';
import { useState, useContext, useEffect } from 'react';
import { UserContext } from '../context/UserContext';


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
		<div>
			<section>
				<Welcome />
			</section>
		
			<br />
			<Link to='/browse'>
				<button>Browse Books</button>
			</Link>
			<br />
			<br />
			<Link to='/my-library'>
				<button>View Personal Library💮</button>
			</Link>
			<br />
			<br />
			<Link to='/leaderboard'>
				<button>View 2026 Leaderboard</button>
			</Link>
			<br />
			<br />
			<Link to='/butterfly-garden'>
				<button>View Butterfly Garden🦋</button>
			</Link>
		</div>
	);

}

export default Home;

