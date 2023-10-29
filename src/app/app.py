import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain.llms.openai import OpenAI

from src.data_downloader.run import download_repo
from src.doc_store.doc_store import DocStore


def streamlit_chatbot_app(qa_chain):
    """Run a conversation with the chatbot in a streamlit app."""
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


if __name__ == "__main__":
    download_repo()

    doc_store = DocStore()
    llm = OpenAI(temperature=0)
    retriever = doc_store.db.as_retriever(search_kwargs={"k": 10})

    chain = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=retriever,
        return_source_documents=True,
        return_generated_question=True,
    )

    streamlit_chatbot_app(chain)
