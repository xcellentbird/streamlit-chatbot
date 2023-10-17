import traceback

import streamlit as st
from funcy import chunks

from llm_agent import OpenAIChatAgent, GenFAQsLLM

N_FAQS = st.sidebar.number_input("Number of FAQs", min_value=1, max_value=10, value=4)
openai_model_name = "gpt-3.5-turbo"

st.title('🦜🔗 Wrtn Up')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

input_content = st.chat_input("What is up?")
if "clicked_faq" in st.session_state:
    input_content = st.session_state['clicked_faq']

    del st.session_state['clicked_faq']


try:
    llm_agent = OpenAIChatAgent()
    gen_faq_llm = GenFAQsLLM()

except Exception as e:
    st.error(f"Error initializing agent...\n\n{traceback.format_exc()}\n{e.__class__.__name__}: {e}")
    st.stop()

else:
    def faq_button_callback(clicked_faq: str):
        st.session_state['clicked_faq'] = clicked_faq

    if input_content:
        st.session_state.messages.append({"role": "human", "content": input_content})

        with st.chat_message("human"):
            st.markdown(input_content)

        with st.chat_message("ai"):
            response = llm_agent.run(
                chat_history=st.session_state.messages[:-1],
                human_input=input_content,
                st_gen=st,
            )

            st.markdown(response)
            st.markdown("---")
            st.session_state.messages.append({"role": "ai", "content": response})

            faqs = gen_faq_llm.run(
                chat_history=st.session_state.messages[:-1],
                human_input=input_content,
                ai_response=response,
            )

            btn_id = 1
            n_cols = 2
            for faqs in chunks(n_cols, faqs):
                cols = st.columns([1] * n_cols)
                for col, faq in zip(cols, faqs):
                    col.button(label=f"*{btn_id}.* {faq}", key=btn_id, on_click=faq_button_callback, args=(faq,))
                    btn_id += 1
