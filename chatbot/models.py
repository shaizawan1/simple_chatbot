from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
load_dotenv()

#models name: llama-3.3-70b-versatile for Groq and qwen3:0.6b for ollama

def select_model(mode, model_provider, temperature):

    model = init_chat_model(
        model=mode,
        model_provider=model_provider,
        temperature = temperature
    )
    return model


