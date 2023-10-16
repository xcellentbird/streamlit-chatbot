from datetime import datetime
from typing import List

from langchain.agents.tools import Tool
from langchain.schema.output import Generation
from langchain.schema.output_parser import BaseLLMOutputParser
from langchain.tools.google_search.tool import GoogleSearchRun, GoogleSearchAPIWrapper

from config import GOOGLE_API_KEY, GOOGLE_CSE_ID


class FaqOutputParser(BaseLLMOutputParser):
    def parse_result(self, result: List[Generation], *, partial: bool = False):
        text = result[0].text
        if text.startswith("'") and text.endswith("'"):
            text = text.split("'")[1]
        elif text.startswith('"') and text.endswith('"'):
            text = text.split('"')[1]
        return text


def datatime_func(query: str) -> str:
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S %Z")


datatime_tool = Tool.from_function(
    func=datatime_func,
    name="datetime",
    description="Get the current date and time. Only one string argument is supported.",
)

custom_google_search_tool = GoogleSearchRun(
    name="google_search",
    description=("A wrapper around Google Search. "
                 "Useful for when you need to understand user intents "
                 "and answer user's questions about current events. "
                 "Or Double Check the fact to avoid AI hallucinations. "
                 "Input should be a search query."),
    api_wrapper=GoogleSearchAPIWrapper(
        google_api_key=GOOGLE_API_KEY,
        google_cse_id=GOOGLE_CSE_ID,
        k=8
    )
)

