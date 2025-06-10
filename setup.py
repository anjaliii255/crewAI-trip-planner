from setuptools import setup, find_packages

setup(
    name="trip_planner",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "langchain",
        "langchain-openai",
        "openai",
        "python-dotenv",
        "pandas",
        "plotly",
        "beautifulsoup4",
        "pydantic",
        "requests"
    ],
    python_requires=">=3.8",
) 