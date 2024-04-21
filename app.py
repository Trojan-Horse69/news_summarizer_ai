import streamlit as st
from langchain.chains.summarize import load_summarize_chain
from summarizer import summarize
from scraper import scrape_website

st.title("Site Summarizer")

# Input field for user text
url_query = st.text_area("Enter site URL you want to summarize")

if st.button("Summarize Site"):
    with st.spinner("Scraping URL...."):
        url, scraped_content = scrape_website(url_query)
        print(f"Scraping {url}")
                
        if scraped_content is None:
            raise Exception("Couldn't scrape site")
        else: 
            with open("./content.txt", "w", encoding="utf-8") as f:
                content = scraped_content
                f.write(content)

            output = summarize()
            st.write(output)
                    