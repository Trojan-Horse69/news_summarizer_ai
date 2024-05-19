import streamlit as st
from scraper import scrape_website, can_fetch_url  # Import your scraping functions from your scraping script
from langchain.chains.summarize import load_summarize_chain
from summarizer import summarize
from utils import check_valid_url
import httpx


def main():
    try:
        st.title("Site Summarizer")

        # Input field for user text
        url_query = st.text_area("Enter site URL you want to summarize")

        if st.button("Summarize Site"):
            try:
                if check_valid_url(url_query):
                    # Check if the URL can be fetched according to robots.txt rules
                    if can_fetch_url(url_query):
                        # Scraping process
                        with st.spinner("Scraping URL...."):
                            url, scraped_content = scrape_website(url_query)
                            print(f"Scraping {url}")
                            
                            if scraped_content is None:
                                st.write("Couldn't scrape site")
                            else: 
                                with open("./content.txt", "w", encoding="utf-8") as f:
                                    content = scraped_content
                                    f.write(content)

                                summary = summarize()
                                st.write(summary)

                                #deleting the contents of the files because i've noticed that "scraped_content error" is raised if the same site is scraped consecutively
                                try:
                                    with open("./content.txt", "r+") as f:
                                        f.truncate(0)
                                except FileNotFoundError:
                                    print("file not found")
                                pass
                    else:
                        st.write("Access to this site is disallowed by robots.txt rules")
                else:
                    st.write("Invalid URL! Please enter a valid URL")

            except ValueError as e:
                st.write("Invalid URL! Please enter a valid URL")

    except httpx.ConnectError as e:
        # Handle the connection error
        st.write("Check your internet connection")

if __name__ == "__main__":
    main()
