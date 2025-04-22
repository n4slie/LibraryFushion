from googleapiclient.discovery import build
from django.conf import settings
import os
from typing import Dict, List, Optional

class GoogleBooksService:
    def __init__(self):
        # Get API key from environment variables
        self.api_key = os.getenv('GOOGLE_BOOKS_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_BOOKS_API_KEY environment variable is not set")
        
        # Initialize the service with the API key
        self.service = build('books', 'v1', 
                           developerKey=self.api_key,
                           static_discovery=False)

    def search_books(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Search for books using the Google Books API
        
        Args:
            query (str): Search query string
            max_results (int): Maximum number of results to return (default: 10)
            
        Returns:
            List[Dict]: List of book information dictionaries
        """
        try:
            # Execute the search
            results = self.service.volumes().list(
                q=query,
                maxResults=max_results
            ).execute()

            # Extract relevant information from each book
            books = []
            for item in results.get('items', []):
                volume_info = item.get('volumeInfo', {})
                book = {
                    'title': volume_info.get('title', ''),
                    'authors': volume_info.get('authors', []),
                    'publisher': volume_info.get('publisher', ''),
                    'published_date': volume_info.get('publishedDate', ''),
                    'description': volume_info.get('description', ''),
                    'isbn_13': next((identifier['identifier'] for identifier in volume_info.get('industryIdentifiers', [])
                                if identifier['type'] == 'ISBN_13'), None),
                    'page_count': volume_info.get('pageCount', 0),
                    'categories': volume_info.get('categories', []),
                    'language': volume_info.get('language', ''),
                    'preview_link': volume_info.get('previewLink', ''),
                    'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', '')
                }
                books.append(book)
            
            return books
        except Exception as e:
            print(f"Error searching Google Books API: {str(e)}")
            return []

    def get_book_by_isbn(self, isbn: str) -> Optional[Dict]:
        """
        Get book details by ISBN
        
        Args:
            isbn (str): ISBN of the book
            
        Returns:
            Optional[Dict]: Book information dictionary if found, None otherwise
        """
        try:
            results = self.service.volumes().list(
                q=f'isbn:{isbn}'
            ).execute()

            if not results.get('items'):
                return None

            volume_info = results['items'][0].get('volumeInfo', {})
            return {
                'title': volume_info.get('title', ''),
                'authors': volume_info.get('authors', []),
                'publisher': volume_info.get('publisher', ''),
                'published_date': volume_info.get('publishedDate', ''),
                'description': volume_info.get('description', ''),
                'isbn_13': isbn,
                'page_count': volume_info.get('pageCount', 0),
                'categories': volume_info.get('categories', []),
                'language': volume_info.get('language', ''),
                'preview_link': volume_info.get('previewLink', ''),
                'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', '')
            }
        except Exception as e:
            print(f"Error fetching book by ISBN from Google Books API: {str(e)}")
            return None 