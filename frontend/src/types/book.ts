
// interface for Book object
export interface Book {
	book_id: number;
	title: string;
	author: string;
	publication_year: number;
	synopsis: string;
	isbn: string;
	page_count: number;
	cover: Blob
}
