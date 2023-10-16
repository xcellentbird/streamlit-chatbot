import traceback

import streamlit as st
from funcy import chunks

from config import OPENAI_API_KEY
from llm_agent import OpenAIChatAgent, GenFAQsLLM

N_FAQS = st.sidebar.number_input("Number of FAQs", min_value=1, max_value=10, value=4)
openai_model_name = "gpt-3.5-turbo"

st.title('🦜🔗 Wrtn Up')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["type"]):
        st.markdown(message["data"])


try:
    llm_agent = OpenAIChatAgent(
        openai_api_key=OPENAI_API_KEY,
        openai_model_name=openai_model_name,
    )

    gen_faq_llm = GenFAQsLLM(
        openai_api_key=OPENAI_API_KEY,
        openai_model_name=openai_model_name,
    )

except Exception as e:
    st.error(f"Error initializing agent...\n\n{traceback.format_exc()}\n{e.__class__.__name__}: {e}")
    st.stop()

else:
    def faq_button_callback(faq: str):
        st.session_state['clicked_faq'] = faq

    def update_input(input_text: str):
        st.session_state.messages.append({"type": "human", "data": input_text})

        with st.chat_message("human"):
            st.markdown(input_text)

        with st.chat_message("ai"):
            response = llm_agent.run(
                chat_history=st.session_state.messages[:-1],
                human_input=input_text,
                st_gen=st,
            )

            st.markdown(response)
            st.markdown("---")
            st.session_state.messages.append({"type": "ai", "data": response})

            faqs = gen_faq_llm.run(
                chat_history=st.session_state.messages[:-1],
                human_input=input_text,
                ai_response=response,
                st_gen=st,
            )

            btn_id = 1
            n_cols = 2
            for faqs in chunks(n_cols, faqs):
                cols = st.columns([1] * n_cols)
                for col, faq in zip(cols, faqs):
                    col.button(label=f"*{btn_id}.* {faq}", key=btn_id, on_click=faq_button_callback, args=(faq,))
                    btn_id += 1

    if "clicked_faq" in st.session_state:
        input_content = st.session_state['clicked_faq']
        update_input(input_content)

        del st.session_state['clicked_faq']

    elif input_content := st.chat_input("What is up?"):
        update_input(input_content)
