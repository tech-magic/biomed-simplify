from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.llms import Ollama

from crewai import LLM

from config.llm_config import LLM_ENDPOINT, LLM_MODEL

# Set up our backend LLM with OpenAI-compatible API
llm = ChatOpenAI(
    model=LLM_MODEL,                         # Or any local model you've downloaded
    base_url=LLM_ENDPOINT,                   # Ollama's OpenAI-compatible endpoint
    api_key="ollama",                        # Dummy API key
)

crew_llm = LLM(
   model=f"openai/{LLM_MODEL}",
   base_url=LLM_ENDPOINT
  )

def get_prompt_template(prompt_path):
    with open(prompt_path, "r") as f:
        prompt_template = f.read()
    return prompt_template

# === OpenAI LLM Call ===
def get_direct_answer(prompt):
    # Compose the chat
    messages = [HumanMessage(content=prompt)]

    # Run the model
    response = llm(messages)

    return response.content
    
def get_answer_from_llm(system_prompt, input_prompt):
    # Compose messages
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=input_prompt)
    ]

    # Run the model
    response = llm(messages)
    return response.content

def get_default_llm():
    return llm

def get_crew_llm():
    return crew_llm




