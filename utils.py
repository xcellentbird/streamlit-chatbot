from langchain.tools.google_search.tool import GoogleSearchRun, GoogleSearchAPIWrapper

from config import GOOGLE_API_KEY, GOOGLE_CSE_ID

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

