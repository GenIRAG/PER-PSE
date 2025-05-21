"""
How to Build Llama-2-7B-Chat or OpenAI Generator.
"""

from flashrag.config import Config
from flashrag.utils import get_generator
from flashrag.prompt import PromptTemplate

## CASE1: Llama2-7B-Chat
config_dict = {
    # Generator Settings
    "framework": "hf",
    "generator_model": "llama2-7B-chat"
}

config = Config("../my_config.yaml", config_dict=config_dict)
llama2_7b_chat_generator = get_generator(config)

# option1: single query
query = "who is Adele Adkins?"
results4s1 = llama2_7b_chat_generator.generate(query)

# option2: multiple query
query_lst = ["who is Taylor Swift?", "who is Adele Adkins?"]
results4m1 = llama2_7b_chat_generator.generate(query_lst)

print(f"Single query output (Llama2-7B-Chat):\n{results4s1}")
print(f"Multiple query output (Llama2-7B-Chat):\n{results4m1}")


## CASE2: GPT-4o-mini
config_dict = {
    # Generator Settings
    "framework": "openai",
    "generator_model": "gpt-4o-mini",
    "openai_setting": {
        "base_url": "YOUR_URL",
        "api_key": "YOUR_KEY"
    }
}

config = Config("../my_config.yaml", config_dict=config_dict)
chatgpt_generator = get_generator(config)
prompt_template = PromptTemplate(
    config=config,
    system_prompt="Answer the question based on your own knowledge. Only give me the answer and do not output any other words.",
    user_prompt="Question: {question}",
)

# option1: single query
query = "who is Adele Adkins?"
input_prompts = [prompt_template.get_string(question=query)]
results4s2 = chatgpt_generator.generate(input_prompts, temperature=0.0)

# option2: multiple query
query_lst = ["who is Taylor Swift?", "who is Adele Adkins?"]
input_prompts = [prompt_template.get_string(question=query) for query in query_lst]
results4m2 = chatgpt_generator.generate(input_prompts, temperature=0.0)

print(f"Single query output (GPT-4o-mini):\n{results4s2}")
print(f"Multiple query output (GPT-4o-mini):\n{results4m2}")
