import streamlit as st
from streamlit_chat import message
from langchain.llms import CTransformers
from langchain.llms import Ollama
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
from glob import glob
import pickle

from PIL import Image
st.set_page_config(page_title='Llama2-Chatbot')
image = Image.open("IPHost.png")
st.image(image, width=64)
st.header('IP Host Monitor Llama2-Powered Chatbot')

@st.cache_resource()
def load_llm():

    # load the llm with ctransformers
    #llm = CTransformers(model='models/llama-2-7b-chat.ggmlv3.q2_K.bin', # model available here: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/tree/main
    #                model_type='llama',
    #                context_length=4096,
    #                config={'max_new_tokens': 256, 'temperature': 0})
    llm = Ollama(model="llama2:13b", num_thread=6) # Use 6 CPU cores
    #llm = Ollama(model="llama2:13b") # Use 50% of CPU cores
    return llm

@st.cache_resource()
def load_vector_store():

    # load the vector store
    embeddings = HuggingFaceEmbeddings(
        #model_name="sentence-transformers/all-MiniLM-L12-v2",
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        #model_name="sentence-transformers/all-mpnet-base-v2",
        model_kwargs={'device': 'cpu'})
    db = FAISS.load_local("faiss", embeddings)
    return db

@st.cache_data()
def load_prompt_template():

    # prepare the template we will use when prompting the AI
    template = """Use the provided context to answer the user's question.
    If you don't know the answer, respond with "I do not know".

    Context: {context}
    Question: {question}
    Answer:
    """

    prompt = PromptTemplate(
    template=template,
    input_variables=['context', 'question'])

    return prompt 

def create_qa_chain():

    # load the llm, vector store, and the prompt
    llm = load_llm()
    db = load_vector_store()
    prompt = load_prompt_template()

    # create the qa_chain
    retriever = db.as_retriever(search_kwargs={'k': 2})
    qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                        chain_type='stuff',
                                        retriever=retriever,
                                        return_source_documents=True,
                                        chain_type_kwargs={'prompt': prompt})
    
    return qa_chain

def generate_response(query, qa_chain):

    # use the qa_chain to answer the given query
    return qa_chain({'query':query})['result']


def get_user_input():

    # get the user query
    input_text = st.text_input('Ask me anything about the use of IP Host monitor software', "", key='input')
    return input_text



# create the qa_chain
qa_chain = create_qa_chain()


# create empty lists for user queries and responses
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

# get the user query
user_input = get_user_input()


if user_input:

    # generate response to the user input
    response = generate_response(query=user_input, qa_chain=qa_chain)

    # add the input and response to session state
    st.session_state.past.append(user_input)
    st.session_state.generated.append(response)


# display conversaion history (if there is one)
if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) -1, -1, -1):
        message(st.session_state['generated'][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
