import os
from langchain_ollama import ChatOllama
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
)
from dotenv import load_dotenv

from .embeddings import get_vector_store
from .memory import get_memory
from .language import get_response_language, build_language_instruction

load_dotenv()

_SYSTEM_TEMPLATE = """{language_instruction}

You are a knowledgeable research assistant. Your answers must be grounded \
exclusively in the research knowledge base provided below. \
If the question cannot be answered from the retrieved context, \
say clearly that the information is not in the current database — \
do not fabricate answers or use outside knowledge.

Be concise, accurate, and cite which part of the research you are drawing from \
when possible.

Retrieved research context:
{context}
"""

def _build_chain(session_id: str, lang: str) -> ConversationalRetrievalChain:
    llm = ChatOllama(
        model=os.getenv("LLM_MODEL", "llama3.2:3b"),
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        temperature=0.3,   # Lower temp = more faithful to retrieved docs
        num_predict=768,
    )

    retriever = get_vector_store().as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5},
    )

    system_prompt = SystemMessagePromptTemplate(
        prompt=PromptTemplate(
            input_variables=["context", "language_instruction"],
            template=_SYSTEM_TEMPLATE,
        )
    )
    human_prompt = HumanMessagePromptTemplate(
        prompt=PromptTemplate(
            input_variables=["question"],
            template="{question}",
        )
    )

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=get_memory(session_id),
        combine_docs_chain_kwargs={
            "prompt": ChatPromptTemplate.from_messages([system_prompt, human_prompt]),
            "document_variable_name": "context",
        },
        return_source_documents=True,
        verbose=False,
    )

async def run_agent(session_id: str, message: str) -> dict:
    lang = get_response_language(session_id, message)
    lang_instruction = build_language_instruction(lang)
    chain = _build_chain(session_id, lang)

    result = chain.invoke({
        "question": message,
        "language_instruction": lang_instruction,
    })

    sources = list({
        doc.metadata.get("source", "")
        for doc in result.get("source_documents", [])
        if doc.metadata.get("source")
    })

    return {
        "answer": result["answer"],
        "response_language": lang,
        "sources": sources,
    }