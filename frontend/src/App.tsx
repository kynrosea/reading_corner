import { useState } from 'react'
import heroImg from './assets/hero.png'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import './App.css'

function App() {
	const [count, setCount] = useState(0)

	{/* Specifies what the component displays */}
	return (
		<div>
			<h1>Reading Corner</h1>
			<p>Welcome to your cozy reading corner!</p>
			<button>Browse Books</button>
		</div>
	);
}

{/* allows other files to import this component */}
export default App;
