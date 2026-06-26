import json  
# from sentence_transformers import SentenceTransformer
from openai import OpenAI

with open("bot_config.json") as f:  
    _config = json.load(f)  
  
# LLM  
LLM_API_KEY   = _config["openai"]["api_key"]  
LLM_BASE_URL  = _config["openai"]["base_url"]  
LLM_MODEL     = _config["openai"]["model"]  

client = OpenAI(
    api_key=LLM_API_KEY,
    base_url=LLM_BASE_URL
)
# # Qdrant  
# QDRANT_URL    = _config["qdrant"]["url"]  
# QDRANT_PREFIX = _config["qdrant"].get("prefix", None)  
  
# # Collections  
# MEMORY_COLLECTION   = "agent_memories"  
# CODEBASE_COLLECTION = "codebase_chunks"  
  
# # Embedding  
# EMBEDDING_MODEL = "./all-MiniLM-L6-v2"
# EMBEDDING_DIM   = 384  
  
# # Agent loop limits  
# MAX_ITERATIONS = 15  
