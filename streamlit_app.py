# Phoenix setup (must be first)
import os
from phoenix.otel import register

# Configure Phoenix
os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = "https://agentopsacc-backend-app.yellowriver-a22b4385.westus.azurecontainerapps.io/v1/traces"
tracer_provider = register(
    project_name="crewAI-trip-planner",
    endpoint="https://agentopsacc-backend-app.yellowriver-a22b4385.westus.azurecontainerapps.io/v1/traces",
    auto_instrument=True,
    batch=True
)

from openinference.instrumentation.litellm import LiteLLMInstrumentor
LiteLLMInstrumentor().instrument()

from openinference.instrumentation.langchain import LangChainInstrumentor
LangChainInstrumentor().instrument()

# Now import Streamlit and other dependencies
import streamlit as st

# Set page config (must be first Streamlit command)
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import after page config
from trip_planner.app import main

if __name__ == "__main__":
    main() 