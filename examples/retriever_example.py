"""
How to Build BM25s Retriever.
"""

from flashrag.config import Config
from flashrag.utils import get_retriever

## CASE: BM25s
config_dict = {
    # Retriever Settings
    "index_path": "YOUR_PATH",
}

config = Config("../my_config.yaml", config_dict=config_dict)
bm25s_retriever = get_retriever(config)

query = "Green is the fourth studio album by British progressive"
results, scores = bm25s_retriever.batch_search([query], num=5, return_score=True)

print(results)
print(scores)
