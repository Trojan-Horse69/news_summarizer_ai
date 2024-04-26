import requests
from bs4 import BeautifulSoup
import time
from time import sleep
from requests.exceptions import ConnectionError
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser


# Define global variables for rate limiting
REQUEST_DELAY = 2  # Delay between requests in seconds
last_request_time = None

def wait_for_rate_limit():
    """
    Waits for the appropriate time to make the next request based on the request delay.
    """
    global last_request_time
    if last_request_time:
        elapsed_time = time.time() - last_request_time
        if elapsed_time < REQUEST_DELAY:
            sleep(REQUEST_DELAY - elapsed_time)
    last_request_time = time.time()

def can_fetch_url(url):
    """
    Check if the given URL can be fetched according to robots.txt rules.
    """
     # Parse the base URL
    base_url = urlparse(url)
    
    # Get the URL of the robots.txt file
    robots_url = f"{base_url.scheme}://{base_url.netloc}/robots.txt"

    # Initialize a RobotFileParser object and fetch the robots.txt
    rp = RobotFileParser()
    rp.set_url(robots_url)
    rp.read()
    
    # Check if the URL is allowed to be fetched
    return rp.can_fetch("*", url)

def scrape_website(url):
    """Scrapes a URL and returns the text content, attempting to filter out footer content.

    Args:
        url (str): The URL to scrape.

    Returns:
        tuple: A tuple containing the URL and the scraped text content.
    """
    global last_request_time
    try:
        if not can_fetch_url(url):
            print(f"Access to {url} is disallowed by robots.txt")
            return url, None
        
        wait_for_rate_limit()  # Respect rate limiting
        
        # Set headers to mimic a browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
        }
        
        # Send the request with headers
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Check if the response is successful and is HTML content
        if response.status_code == 200 and 'text/html' in response.headers.get('Content-Type', ''):
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
        else:
            print(f"Failed to retrieve HTML content from: {url}")
            return url, None

    except requests.RequestException as e:
        print(f"Failed to retrieve the webpage: {e}")
        return url, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return url, None
