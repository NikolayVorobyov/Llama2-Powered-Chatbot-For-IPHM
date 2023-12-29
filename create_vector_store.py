from langchain.document_loaders import DirectoryLoader #, TextLoader, PyPDFLoader
#from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.document_loaders import BSHTMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

# define what documents to load
#loader = DirectoryLoader(path='data', glob="*.html", loader_cls=PyPDFLoader)
loader = DirectoryLoader(path='data', glob="**/*.html", loader_cls=BSHTMLLoader, show_progress=True)

# interpret information in the documents
documents = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                          chunk_overlap=50)
texts = splitter.split_documents(documents)

#print ("---")
#print (texts)
#print ("---")

#return (0)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    #model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={'device': 'cpu'})

# create the vector store database
db = FAISS.from_documents(texts, embeddings)

# save the vector store
db.save_local("faiss")
