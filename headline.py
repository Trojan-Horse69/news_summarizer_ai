from utils import llm
from langchain_core.prompts import ChatPromptTemplate

def headline(summary):
    template = """Based on the news summary below, generate a short, catchy one-line headline for the summary:
    {summary}
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Given the news summary, generate a catchy but relevant headline for the summary. No preamble"),
            ("human", template.format(summary=summary)),
        ]
    )

    chain = prompt | llm

    result = chain.invoke({"summary": summary})
    headline_content =  result.content.strip('""')
    return headline_content
