import os

# Absolute path to the folder where this config file lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

####------ VECTOR STORE CONFIG --------####
VECTOR_STORE_DB_FOLDER = os.path.join(BASE_DIR, ".chroma")
os.makedirs(VECTOR_STORE_DB_FOLDER, exist_ok=True)
VECTOR_STORE_DATA_FOLDER = os.path.join(BASE_DIR, "data-demo")
os.makedirs(VECTOR_STORE_DATA_FOLDER, exist_ok=True)
VECTOR_STORE_EMBEDDING_MODEL = "text-embedding-3-small"

###------- WEBSEARCH CONFIG ---------#######
K_TAVILY_SEARCH_RESULTS = 3