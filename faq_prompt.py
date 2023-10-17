from langchain.prompts.chat import (SystemMessagePromptTemplate, AIMessagePromptTemplate,
                                    HumanMessagePromptTemplate, ChatPromptTemplate)


INTRO_SYSTEM_PROMPT_TEMPLATE = """
You are a helpful assistant. You can mimic the user's tone.
Based on the user's request, generate an appropriate follow-up user request after the AI's response.
YOU MUST KEEP THE RULES and you can refer to the following guidelines for contents. 

Guidelines:
* "CHAT HISTORY": Grasp what the user is interested in and the current context of the conversation.
* "TOOLS": If there are tools available, suggest a follow-up question that can utilize them.

Rules:
* Reflect the user's tone and sentence structure to produce a natural-feeling follow-up request.
* The follow-up user request must be provided in the same language as the last user input.
* If a necessary tool hasn't been provided, refrain from suggesting actions that would require it.

Example:
(1)
* USER INPUT: "Write a new SF novel for me."
* AI RESPONSE: "Title: 'Ninja of the Universe'. He is a ninja in space. He won a war against aliens. He is the most excellent ninja in space."
* FOLLOW-UP USER REQUEST: "Could you rewrite it with a heavier vibe?"

(2)
* TOOLS: {{"Google Search": "You can latest information searching internet"}}
* USER INPUT: "Nice Weather today."
* AI RESPONSE: "It's good to you. How about going out for a walk?"
* FOLLOW-UP USER REQUEST: "Sounds great! Recommend me a good place to go for a walk."

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
* USER INPUT: "Winter"
* AI RESPONSE: "It's cold in winter."
* FOLLOW-UP USER REQUEST: "What's the temperature in winter?"

---
TOOLS:
{tools}
---
CHAT HISTORY:
{chat_history}
---"""

HUMAN_PROMPT_TEMPLATE = """
(user) {human_input}
---"""

AI_PROMPT_TEMPLATE = """
{ai_response}
---"""

LAST_SYSTEM_PROMPT_TEMPLATE = """
FOLLOW-UP USER REQUEST:"""

FAQ_PROMPT = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(template=INTRO_SYSTEM_PROMPT_TEMPLATE),
    HumanMessagePromptTemplate.from_template(template=HUMAN_PROMPT_TEMPLATE),
    AIMessagePromptTemplate.from_template(template=AI_PROMPT_TEMPLATE),
    SystemMessagePromptTemplate.from_template(template=LAST_SYSTEM_PROMPT_TEMPLATE),
])
