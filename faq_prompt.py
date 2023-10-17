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
* TOOLS: {{"Google Search API": "You can latest information searching internet", "Generate Image API": "You can generate Image with Text", ...}}
* USER INPUT: "Write a new SF novel for me."
* AI RESPONSE: "Title: 'Ninja of the Universe'. He is a ninja in space. He won a war against aliens. He is the most excellent ninja in space."
* candidates of FOLLOW-UP USER REQUEST: ["Search for more SF novels for me.", "Generate an image of the main character of this novel.", 
"re-write the novel in a different genre.", "Could you please write shorter?", "Could you rewrite it with a heavier vibe?", "I wish the characters were a little gentler..."]
  
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
    SystemMessagePromptTemplate.from_template(template=SYSTEM_PROMPT_TEMPLATE),
    HumanMessagePromptTemplate.from_template(template=HUMAN_PROMPT_TEMPLATE),
    AIMessagePromptTemplate.from_template(template=AI_PROMPT_TEMPLATE),
    SystemMessagePromptTemplate.from_template(template=LAST_SYSTEM_PROMPT_TEMPLATE),
])
