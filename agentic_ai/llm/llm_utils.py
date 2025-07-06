from crewai import LLM
from config.llm_config import LLM_ENDPOINT, LLM_MODEL

def get_crew_llm():
    return LLM(
        model=f"openai/{LLM_MODEL}",
        base_url=LLM_ENDPOINT
    )
