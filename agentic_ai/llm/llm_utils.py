from crewai import LLM
from config.app_config import get_llm_config

LLM_MODEL = get_llm_config().get('model')
OPENAI_ENDPOINT = get_llm_config().get('openai_endpoint')
OPENAI_API_KEY = get_llm_config().get('openai_api_key')

def get_crew_llm():
    return LLM(
        model=f"openai/{LLM_MODEL}",
        base_url=OPENAI_ENDPOINT,
        api_key=OPENAI_API_KEY
    )
