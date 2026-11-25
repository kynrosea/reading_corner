import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.tsx';
import { UserProvider } from './context/UserContext';
import { BookProvider } from './context/BookContext';

createRoot(document.getElementById('root')!).render(
	<StrictMode>
		<UserProvider>
			<BookProvider>
				<App />
			</BookProvider>
		</UserProvider>
	</StrictMode>,
);
