
import { useState, useEffect } from "react";
import { useNavigate } from 'react-router';

interface EditBookStatusProps {
	username: string;
	title: string;
	author: string;
	currentStatus: string;
	onUpdated: () => void;
}

export default function EditBookStatus({
	username,
	title,
	author,
	currentStatus,
	onUpdated,
}: EditBookStatusProps) {

	const navigate = useNavigate();
	const [status, setStatus] = useState(currentStatus);
	const [loading, setLoading] = useState(false);
	const [message, setMessage] = useState('');
	const [showMessage, setShowMessage] = useState<boolean>(false);

	useEffect(() => {
		setStatus(currentStatus);
	}, [currentStatus]);

	// sets a timeout function so that the message will disappear after 1.5 seconds
	useEffect(() => {
		if (!showMessage) return;

		const timer = setTimeout(() => {
			setShowMessage(false);
		}, 1500);

		return () => clearTimeout(timer);
	}, [showMessage]);

	async function saveStatus() {
		setLoading(true);
		setMessage('');
		let updateData = {
			status
		};
		
		if (status === 'read') {
			
			const today: string = new Date().toLocaleDateString('en-CA');
			updateData = {
				status,
				finished_date: today
			};
		}
		try {
			const response = await fetch(
				`/library/${encodeURIComponent(username)}/${encodeURIComponent(title)}/${encodeURIComponent(author)}`, {
					method: 'PUT',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify(updateData),
				}
			);


			if (!response.ok) {
				const data = await response.json();
				let errorMessage = `Request failed with status ${response.status}`;
				throw new Error(data.error || errorMessage);
			}
			
			const data = await response.json();

			onUpdated();

			setMessage(
				data.reward?.leaves_earned > 0
					? `Book updated! You earned ${data.reward.leaves_earned} leaves!`
					: 'Reading status updated!'
			);
			
			setShowMessage(true);
		
		} catch (error) {
			console.error(error);
			setMessage(
				error instanceof Error 
					? error.message :
					'Something went wrong!'
			);
		} finally {
			setLoading(false);
		}
	}


	return (
		<div>
			<select
				value={status}
				onChange={(event) => setStatus(event.target.value)}
			>
				<option value="tbr">Want to Read</option>
				<option value="currently reading">Currently Reading</option>
				<option value="read">Finished</option>
				<option value="dnf">Did Not Finish</option>
			</select>

			<button
				className='basic-button'
				onClick={saveStatus}
				disabled={loading}
			>
				{loading ? 'Saving...' : 'Save Status'}
			</button>

			{showMessage && <p>{message}</p>}

		</div>
	);
}

