import { NavLink, Outlet } from 'react-router';
import logo from '../assets/reading_corner_logo.png';
import './Header.css';

function Header() {

	return (
		<main>
			<header>
				<nav className='header-nav'>
					<div className='header-brand'>
						<NavLink to='/'>
							<img className='header-logo' src={logo} alt='Reading Corner Logo' />
						</NavLink>
						<h2>Reading Corner</h2>
					</div>
					<div className='header-links'>
						<NavLink to='/'>
							<button>
								Home
							</button>
						</NavLink>
						<NavLink to='/browse'>
							<button>Browse Books</button>
						</NavLink>
						<NavLink to='/butterfly-garden'>
							<button>Garden</button>
						</NavLink>
						<NavLink to='/my-library'>
							<button>My Library</button>
						</NavLink>
						<NavLink to='/my-profile'>
							<button>Profile</button>
						</NavLink>
					</div>
				</nav>
			</header>
			<div>
				<Outlet />
			</div>
		</main>
		
	);
}

export default Header;
