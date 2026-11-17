import { BrowserRouter, Routes, Route } from 'react-router';
import './App.css';
import Home from './pages/Home';
import BrowseBooks from './pages/BrowseBooks';
import AddBook from './pages/AddBook';
import Library from './pages/Library';
import Login from './pages/Login';
import Leaderboard from './pages/Leaderboard';
import Rewards from './pages/Rewards';
import Signup from './pages/Signup';

// responsible for defining app's pages rather than managing individual content
function App() {
	return (
		<BrowserRouter>
			<Routes>
				<Route path='/' element={<Home />} />
				<Route path='/browse' element={<BrowseBooks />} />
				<Route path='/add-book' element={<AddBook />} />
				<Route path='/my-library' element={<Library />} />
				<Route path='/login' element={<Login />} />
				<Route path='/leaderboard' element={<Leaderboard />} />
				<Route path='/butterfly-garden' element={<Rewards />} />
				<Route path='/signup' element={<Signup />} />
			</Routes>
		</BrowserRouter>

	);

}

// allows other files to import this component
export default App;
