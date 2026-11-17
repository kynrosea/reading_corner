
import { useState, useEffect } from "react";

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
	const [status, setStatus] = useState(currentStatus);
	const [loading, setLoading] = useState(false);
	const [message, setMessage] = useState("");

	useEffect(() => {
		setStatus(currentStatus);
	}, [currentStatus]);

	async function saveStatus() {
		setLoading(true);
		setMessage('');

		try {
			const response = await fetch(
				`/library/${encodeURIComponent(username)}/${encodeURIComponent(title)}/${encodeURIComponent(author)}`, {
					method: 'PUT',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify({
						status: status,
					}),
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
				onClick={saveStatus}
				disabled={loading || status === currentStatus}
			>
				{loading ? 'Saving...' : 'Save Status'}
			</button>

			{message && <p>{message}</p>}
		</div>
	);
}

