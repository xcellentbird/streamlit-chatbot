import asyncio

from langchain.agents.agent import AgentExecutor
from langchain.agents.openai_functions_multi_agent.base import OpenAIMultiFunctionsAgent
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.llms.openai import OpenAI
from langchain.schema.messages import SystemMessage

from faq_prompt import FAQ_PROMPT
from utils import datatime_tool, custom_google_search_tool

Tools = [
    datatime_tool,
    custom_google_search_tool
]


class OpenAIChatAgent:
    def __init__(self, openai_api_key: str, openai_model_name: str, llm_temp: float = 0.5):
        self.openai_api_key = openai_api_key
        self.openai_model_name = openai_model_name
        self.llm_temp = llm_temp
        self.llm = ChatOpenAI(
            openai_api_key=self.openai_api_key,
            model_name=self.openai_model_name,
            temperature=self.llm_temp,
        )
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=OpenAIMultiFunctionsAgent.from_llm_and_tools(
                self.llm,
                Tools,
                system_message=SystemMessage(
                    content="""
                    You are chat bot 🤖. You are helpful and friendly. 
                    You must understand the Intent of the user and respond accordingly. 
                    You can also use the tools to help you.
                    """),
                extra_prompt_messages=[],
            ),
            tools=Tools,
        )

    def run(self, chat_history, human_input, st_gen):
        st_callback = StreamlitCallbackHandler(st_gen.container())

        ai_response = self.agent_executor.run(
            chat_history=str(chat_history),
            input=human_input,
            callbacks=[st_callback],
            verbose=True,
        )

        return ai_response


class GenFAQsLLM:
    def __init__(self, openai_api_key: str, openai_model_name: str, llm_temp: float = 1.5):
        self.openai_api_key = openai_api_key
        self.openai_model_name = openai_model_name
        self.llm_temp = llm_temp
        self.faq_prompt_template = FAQ_PROMPT

        self.llm = OpenAI(
            openai_api_key=self.openai_api_key,
            model_name=self.openai_model_name,
            temperature=self.llm_temp,
            max_tokens=128,
        )
        self.llm_chain = LLMChain(llm=self.llm, prompt=self.faq_prompt_template)

    def run(self, chat_history, human_input, ai_response, st_gen, n_faqs=4):
        st_callback = StreamlitCallbackHandler(st_gen.container())

        faqs = [
            self.llm_chain.arun(
                chat_history=str(chat_history),
                human_input=human_input,
                ai_response=ai_response,
                tools=str({tool.name: tool.description for tool in Tools}),
                callbacks=[st_callback],
            )
            for _ in range(n_faqs)
        ]

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        faqs = list(loop.run_until_complete(asyncio.gather(*faqs)))
        loop.close()

        return faqs
