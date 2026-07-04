import streamlit as st
import re
from models import select_model
from agent import create_new_agent
from langchain_core.messages import AIMessageChunk

st.title("Welcome to AI World!")

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.header("Model Controls")
    
    # Radio and slider update instantly on each rerun
    model_option = st.radio(
        "Choose your AI Model:",
        options=["Qwen3 (ollama)", "Llama 3.3 (Groq)"],
        index=0,
        horizontal=True
    )
    
    temp_value = st.slider(
        label="Temperature (0 to 1):",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.1,
        format="%.1f"
    )
    
    # Clear button – no form, just a button
    if st.button("Clear Conversation", use_container_width=True):
        st.session_state["messages"] = []
        st.success("Chat history cleared!")
        # No explicit rerun needed – Streamlit reruns automatically

# ----------------- Session State Initialization -----------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ----------------- Display Chat History -----------------
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ----------------- Agent Creation (cached by settings) -----------------
@st.cache_resource
def get_agent(model_name, provider, temperature):
    """Create and cache the agent based on current settings."""
    model = select_model(mode=model_name, model_provider=provider, temperature=temperature)
    return create_new_agent(model=model)

# Map UI choices to model parameters
if model_option == "Qwen3 (ollama)":
    model_name = "qwen3:0.6b"
    provider = "ollama"
else:
    model_name = "llama-3.3-70b-versatile"
    provider = "groq"

# Get the agent (cached, so it's only recreated when settings change)
agent = get_agent(model_name, provider, temp_value)

# ----------------- Handle User Input -----------------
if prompt := st.chat_input("Ask anything..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # Generate AI response
    with st.chat_message("ai"):
        inputs = {"messages": {"role": "ai", "content": prompt}}
        
        full_response = ""
        placeholder = st.empty()

        # Stream the answer, filtering out tool‑call messages and think tags
        for chunk, metadata in agent.stream(inputs, stream_mode="messages"):
            if isinstance(chunk, AIMessageChunk) and not chunk.tool_calls:
                if chunk.content:
                    full_response += chunk.content
                    full_response = full_response.replace("</think>", '')
                    full_response = full_response.replace(",", '', 1)
                    placeholder.markdown(full_response)
        

    st.session_state["messages"].append({"role": "ai", "content": full_response})


