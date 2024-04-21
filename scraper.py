import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.environ.get('OPENAI_API_KEY')


def scrape_website(url):
    """Scrapes a URL and returns the text content, attempting to filter out footer content.

    Args:
        url (str): The URL to scrape.

    Returns:
        tuple: A tuple containing the URL and the scraped text content.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all paragraphs in the page
        paragraphs = soup.find_all('p')

        # Extract the text content of paragraphs
        text_content = [p.get_text().strip() for p in paragraphs]

        # Find potential footer paragraphs based on their position in the page
        max_paragraphs = 3  # Maximum number of paragraphs assumed to be in the footer
        footer_paragraphs = text_content[-max_paragraphs:]

        # Remove potential footer paragraphs from the text content
        filtered_content = [p for p in text_content if p not in footer_paragraphs]

        # Join the remaining paragraphs to create the formatted data
        formatted_data = "\n".join(filtered_content)

        return url, formatted_data
    
    except requests.RequestException as e:
        print(f"Failed to retrieve the webpage: {e}")
        return url, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return url, None