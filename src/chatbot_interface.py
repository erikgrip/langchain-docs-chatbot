import streamlit as st
from langchain.chains.base import Chain


def streamlit_chatbot_app(qa_chain: Chain):
    """
    Run a Streamlit chatbot interface using a langchain retrieval chain.

    Parameters:
    -----------
    qa_chain : Chain
        A conversational retrieval model that takes a question and a chat history
        as input, and returns an answer as output.

    Returns:
    --------
    None
    """
    st.title("Langchain Chatbot")

    # Initialize chat history
    if "messages" not in st.session_state or not st.session_state.messages:
        st.session_state.messages = []
        st.session_state.chat_history = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if question := st.chat_input("Enter a question here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": question})

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(question)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("▌")
            result = qa_chain(
                {"question": question, "chat_history": st.session_state.chat_history}
            )
            message_placeholder.markdown(result["answer"])

        # Update chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": result["answer"]}
        )
        st.session_state.chat_history.extend([(question, result["answer"])])
        st.session_state.chat_history = st.session_state.chat_history[-4:]
