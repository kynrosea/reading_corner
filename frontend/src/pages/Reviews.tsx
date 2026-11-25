import { useState, useEffect, useContext } from 'react';
import { UserContext } from '../context/UserContext';
import { Link } from 'react-router';
import './Reviews.css';

interface Review {
	review_id: number,
	rating: number,
	review_text: string,
	title: string,
	author: string,
}

function Reviews() {

	const userContext = useContext(UserContext);
	if (!userContext) {
		throw new Error('Reviews must be used within UserProvider');
	}

	const [reviews, setReviews] = useState<Review[]>([]);

	const { user } = userContext;

	async function getReviews() {
		try {
			if (!user) {
				throw new Error('Must be logged in');
			}

			const response = await fetch(
				`/reviews/user/${encodeURIComponent(user.username)}`
			);

			if (!response.ok) {
				const errorData = await response.json();
				let errorMessage = `Request failed with status ${response.status}`
				throw new Error(errorData.error || errorMessage);
			}

			const data: Review[] = await response.json();

			console.log(data);
			setReviews(data);
		} catch (error) {
			console.error(error.message);
			alert(error.message);
		}
	}

	useEffect(() => {
		if (!user) return;

		getReviews();
	}, [user]);

	return (
		<main className='reviews'>
			<h1>View all of your reviews here</h1>
			<Link to='/add-review'>
				<button className='basic-button'>Add a new review</button>
			</Link>
			<div className='review-flow'>
				{reviews.map((review) => (
					<div className='review-card' key={review.review_id}>
						<div>
							<h3>{review.title}</h3>
							<h5>{review.author}</h5>
						</div>
						<div>
							<p>{review.review_text}</p>
							<p>{review.rating} stars</p>
						</div>
					</div>
									
				))}
			</div>
		</main>
		
	);
}

export default Reviews;
