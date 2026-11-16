import { Link } from 'react-router';


function Home() {

	let welcomeMessage = 'Welcome to your cozy reading corner!'
	
	// contains the browse books button
	// app passes a function to here
	// that function is called when button is clicked
	
	return (
		<div>
			<h1>{welcomeMessage}</h1>
			<Link to='/browse'>
				<button>Browse Books</button>
			</Link>
			<br />
			<Link to='/my-library'>
				<button>View Personal Library💮</button>
			</Link>
			<br />
			<Link to='/login'>
				<button>Log In</button>
			</Link>
			<br />
			<Link to='/leaderboard'>
				<button>View 2026 Leaderboard</button>
			</Link>
			<br />
			<Link to='/butterfly-garden'>
				<button>View Butterfly Garden🦋</button>
			</Link>
		</div>
	);

}

export default Home;

