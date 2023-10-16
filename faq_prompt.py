from langchain.prompts.chat import (SystemMessagePromptTemplate, AIMessagePromptTemplate,
                                    HumanMessagePromptTemplate, ChatPromptTemplate)


SYSTEM_PROMPT_TEMPLATE = """
Accurately capture the user's intention based on the chat history, user input and AI's response.
Then, using the AI response to the user's input, generate potential questions or requests that the user might ask. 
Additionally, The following tools are available. Follow-up requests or questions may be related to the tools if the user intention is related to the tools.


Example:
* CHAT HISTORY: "I love SF novels. I'm currently reading a book called 'The Three-Body Problem'. The author is Liu Cixin."
* TOOLS: {{"Google Search API": "You can latest information searching internet", "Generate Image API": "You can generate Image with Text", ...}}
* USER INPUT: "Write a new SF novel for me."
* AI RESPONSE: "Title: 'Ninja of the Universe'. He is a ninja in space. He won a war against aliens. He is the most excellent ninja in space."
* candidates of FOLLOW-UP REQUEST: ["Search for more SF novels for me.", "Generate an image of the main character of the novel.", 
"re-write the novel in a different genre.", "Please put a princess in that science fiction novel.", "i need a longer stories"]

Rules:
* The follow-up question should be something the user would say, not yours to say. And must be same tone as the user
* The follow-up question must be related to the user's intention. And must be a question or request.
  (ex. user_input: "이 문장을 영어로 바꿔줘. '난 널 사랑해'" ai_response: "I love you" follow-up question: '더 다양한 영어 문장을 알려줘.')
* Tools may be incorporated into the follow-up question if they align with the user's intention.
* The follow-up question should not be related Tools you don't have. For example, there is no news API, so follow-up request such as “Tell me today’s news” should not be made.
* The follow-up question you provide must be realistic and within the AI's capabilities. If you can't carry it out, don't provide it. 
  (ex. ai_answer: "It' good weather today." follow-up question: "Can you make it rain tomorrow?" -> You can't provide this follow-up question.)
* The follow-up question must be provided in the same language as the user's input. Not ai's response.

YOU MUST KEEP ABOVE RULES and Recommend follow-up requests or questions the user might make after the AI's response with same tone as the user.

---
CHAT HISTORY:
{chat_history}
---
TOOLS:
{tools}"""

HUMAN_PROMPT_TEMPLATE = """
---
{human_input}"""

AI_PROMPT_TEMPLATE = """
---
{ai_response}"""

FOLLOW_UP_HUMAN_PROMPT_TEMPLATE = """
---
FOLLOW-UP QUESTION(REQUEST):"""

FAQ_PROMPT = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(template=SYSTEM_PROMPT_TEMPLATE),
    HumanMessagePromptTemplate.from_template(template=HUMAN_PROMPT_TEMPLATE),
    AIMessagePromptTemplate.from_template(template=AI_PROMPT_TEMPLATE),
    HumanMessagePromptTemplate.from_template(template=FOLLOW_UP_HUMAN_PROMPT_TEMPLATE),
])
