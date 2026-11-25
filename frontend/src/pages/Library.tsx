import { useState, useContext, useEffect } from 'react';
import { UserContext } from '../context/UserContext';
import { Link } from 'react-router';
import EditBookStatus from '../components/EditBookStatus';
import LogModal from '../components/LogModal.tsx';
import './Library.css';

interface Record {
	book_id: number,
	title: string,
	author: string,
	status: string,
}

interface Log {
	log_id: number,
	user_id: number,
	book_id: number,
	log_date: string,
	progress: number,
	notes: string,
	session_time: number
}

function Library() {

	// if userContext is null, then the component isn't receiving the context provider
	// if user is null, the provider exists but nobody has logged in yet
	const userContext = useContext(UserContext);
	if (!userContext) {
		throw new Error('Library must be used within UserProvider');
	}

	const [records, setRecords] = useState<Record[]>([]);
	const [totalBooks, setTotalBooks] = useState(0);
	const [currentBooks, setCurrentBooks] = useState(0);
	const [finishedBooks, setFinishedBooks] = useState(0);
	const [logs, setLogs] = useState<Log[]>([]);
	const [book, setBook] = useState<{
		title: string;
		author: string;
	}>();

	const { user } = userContext;

	// modal functions and properties
	const [open, setOpen] = useState(false);
	function handleClose() {
		setOpen(false);
	};

	function handleOpen(title, author) {
		const bookData = {
			title,
			author
		}
		setBook(bookData);
		getBookReadingLogs(title, author);
		setOpen(true);
	}

	async function getLibrary() {
		try {

			if (!user) {
				throw new Error('User must be logged in');
			}

			const response = await fetch(
				`/library/${encodeURIComponent(user.username)}`
			);

			if (!response.ok) {
				const errorData = await response.json()
				let errorMessage = `Request failed with status ${response.status}`
				throw new Error(errorData.error || errorMessage);
			}

			const data: Record[] = await response.json();

			console.log(data);
			setRecords(data);

		} catch (error) {
			console.error(error.error);
			alert(error.message);
		}
	}

	async function getLibraryReport() {
		try {
			if (!user) {
				throw new Error('User must be logged in');
			}

			const response = await fetch(
				`/library/${encodeURIComponent(user.username)}/report`
			);

			if (!response.ok) {
				const errorData = await response.json();
				let errorMessage = `Request failed with status ${response.status}`
				throw new Error(errorData.error || errorMessage);
			}

			const report = await response.json();

			console.log(report);
			setTotalBooks(report['total books']);
			setCurrentBooks(report['currently reading']);
			setFinishedBooks(report['finished']);
		} catch (error) {
			console.error(error);
			alert(error.message);
		}
	}

	async function getBookReadingLogs(title, author) {
		try {
			if (!user) {
				throw new Error('User must be logged in');
			}

			const response = await fetch(
				`/library/logs/${encodeURIComponent(user.username)}/${encodeURIComponent(author)}/${encodeURIComponent(title)}`
			);

			if (!response.ok) {
				const errorData = await response.json();
				let errorMessage = `Request failed with status ${response.status}`
				throw new Error(errorData.error || errorMessage);
			}

			const data = await response.json();
			console.log(data);
			setLogs(data);

		} catch (error) {
			console.error(error);
			alert(error.message);
		}
	}

	// must tell react to rerun the effect when the selected user changes
	useEffect(() => { 
		if (!user) return;

		getLibrary();
		getLibraryReport();

	}, [user]);

	if (!user) {
		return (
			<main className='login-prompt'>
				<h1>My Library</h1>
				<p>Please log in to view your library.</p>
				<Link to='/login'>
					<button className='basic-button'>Go to Login</button>
				</Link>
			</main>
		)
	}

	return (
		<main className='library'>
			<h1>Welcome to your personal library, {user.first_name}!</h1>
			<div className='report'>
				<div className='report-card'>
					<h5>📚</h5>
					<h3>{totalBooks}</h3>
					<p>Total books</p>
				</div>
				<div className='report-card'>
					<h5>📖</h5>
					<h3>{currentBooks}</h3>
					<p>Currently Reading</p>
				</div>
				<div className='report-card'>
					<h5>✅</h5>
					<h3>{finishedBooks}</h3>
					<p>Finished</p>
				</div>
			</div>
			<div>
				<Link to='/my-reviews'>
					<button className='basic-button'>Go to Reviews</button>
				</Link>
			</div>
			<div className='books-grid'>
				{records.map((record) => (
					<div className='book-card' key={record.book_id}>
						<div>
							<h3>{record.title}</h3>
							<p>{record.author}</p>
						</div>
						<div className='card-field'>
							<EditBookStatus
								username={user.username}
								title={record.title}
								author={record.author}
								currentStatus={record.status}
								onUpdated={getLibraryReport}
							/>
							{/* Trigger/Open the modal for viewing a book's reading logs */}
							<button onClick={() => handleOpen(record.title, record.author)} className='basic-button'>
								View Reading Logs
							</button>



						</div>
					</div>
				))}
			</div>

			{/* The modal */}
			<LogModal isOpen={open} onClose={handleClose}>
				<>
					<div className='logs-content'>
						<h2>Reading Logs for {book?.title} by {book?.author}</h2>
						{logs.length > 0 ? (
							<div>
								{logs.map((log) => (
									<div className='log-card' key={log.log_id}>
										<div className='log-field'>
											<h3>{log.log_date}</h3>
											<div className='progress'>
												<progress max='100' value={log.progress}>
													{log.progress}%
												</progress>
												<span>{log.progress}%</span>
											</div>

										</div>
										<div className='log-field'>
											{log.notes &&
												<p>{log.notes}</p>
											}
										</div>
										<div>
											{log?.session_time != null &&
												<p>{log.session_time}</p>
											}	
										</div>	

									</div>
								))}
							</div>

						) : (

								<p>No reading logs yet!</p>

							)
						}

					</div>
				</>
			</LogModal>
		</main>
	);
}

export default Library;
