from langchain.prompts.chat import (SystemMessagePromptTemplate, AIMessagePromptTemplate,
                                    HumanMessagePromptTemplate, ChatPromptTemplate)


INTRO_SYSTEM_PROMPT_TEMPLATE = """
You are a helpful assistant.
Based on the user's request, generate an appropriate follow-up request user might be saying after the AI's response.
YOU MUST KEEP THE RULES

Guidelines:
* "CHAT HISTORY": Grasp what the user is interested in and the current context of the conversation.
* "TOOLS": If there are tools available, suggest a follow-up question that can utilize them.

Rules:
* Reflect the user's tone in the follow-up user request.
* The follow-up user request must be natural and realistic with same language as the user input.
* If a necessary tool hasn't been provided, refrain from suggesting actions that would require it.

Example:
(1)
* USER INPUT: "Write a new SF novel for me."
* AI RESPONSE: "Title: 'Ninja of the Universe'. He is a ninja in space. He won a war against aliens. He is the most excellent ninja in space."
* FOLLOW-UP USER REQUEST: "Could you rewrite it with a heavier vibe?"

(2)
* TOOLS: {{"Google Search": "You can latest information searching internet"}}
* USER INPUT: "오늘 날씨 좋다!"
* AI RESPONSE: "아주 좋네요! 밖에 산책을 나가 보는 건 어떨까요?"
* FOLLOW-UP USER REQUEST: "좋은 생각이야! 그럼 산책하기 좋은 곳을 알려줘."

(3)
* TOOLS: {{"Generate Image": "You can generate Image with Text"}}
* USER INPUT: "Tell me how to sort a list in Python."
* AI RESPONSE: "You can use the sort() method."
* FOLLOW-UP USER REQUEST: "Could you show me an example?"

(4)
* CHAT HISTORY: "human: I want to be a doctor\nai: That's a great goal!"
* USER INPUT: "Also, I want to be a lawyer."
* AI RESPONSE: "Then, you should be majoring in law."
* FOLLOW-UP USER REQUEST: "Compare the salary of a doctor and a lawyer."

(5)
* USER INPUT: "겨울"
* AI RESPONSE: "It's cold winter."
* FOLLOW-UP USER REQUEST: "어느 정도 까지 추워요?"

---
ai can use theses tools:
TOOLS:
{tools}
---
CHAT HISTORY:
{chat_history}
---"""

HUMAN_PROMPT_TEMPLATE = """
{human_input}
---"""

AI_PROMPT_TEMPLATE = """
{ai_response}
---"""

LAST_SYSTEM_PROMPT_TEMPLATE = """
FOLLOW-UP USER REQUEST(user might be naturally saying after the AI's response with same language, tone as the user input):"""

FAQ_PROMPT = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(template=INTRO_SYSTEM_PROMPT_TEMPLATE),
    HumanMessagePromptTemplate.from_template(template=HUMAN_PROMPT_TEMPLATE),
    AIMessagePromptTemplate.from_template(template=AI_PROMPT_TEMPLATE),
    SystemMessagePromptTemplate.from_template(template=LAST_SYSTEM_PROMPT_TEMPLATE),
])
