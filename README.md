# Training a Llama2-Powered Chatbot to Interact with Research Papers
![Chatbot Diagram](https://github.com/anair123/Llama2-Powered-QA-Chatbot-For-Research-Papers/assets/47230033/5ea10939-b3a3-48c7-819e-9af6db879dbc)


## Introduction
The goal of this project is to build a closed-source chatbot on a CPU using the quantized Llama2 model (7B parameters).

The resulting application will be evaluated based on it's ability as a tool of convenience for retrieving information from research papers. More specifically, it will evaluated by the quality of it's responses, the run time, and the memory expenditure. 

## Installation Instructions

1. Clone this repository using the command:  
```git clone https://github.com/NikolayVorobyov/Llama2-Powered-Chatbot-For-IPHM```

2. Download a quantized Llama2 model (pick any one) from the following link:     https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/tree/main

3. Store the model in the "models" directory

4. Create a virtual environment and enter it  
```python -m venv <name_of_venv>```  
```source <name_of_venv>/bin/activate```

5. Install the dependencies with the command:
```pip install -r requirements.txt```

6. Install the dependencies to download and parse the Web site:
```sudo apt-get install httrack```
```pip install lxml beautifulsoup4```

7. Download HTML files from https://iphostmonitor.com site in the "data" folder using collect_data.sh script.

8. Create vector store from HTML files (will be saved into faiss folder):
```python3 create_vector_store.py```

9. Run the Streamlit web app with the command:  
```streamlit run app.py```
