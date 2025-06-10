# crewAI-trip-planner

A smart, agent-based trip planner leveraging AI and OpenAI's GPT-4 for generating and managing travel itineraries. Built with Python and Jupyter Notebook, this project aims to automate and optimize trip planning with advanced reasoning and retrieval capabilities.

## Features

- **Agent-based planning:** Modular agents coordinate to create and refine trip plans.
- **Integration with OpenAI:** Utilizes GPT-4 for reasoning and retrieval-augmented generation (RAG).
- **Jupyter Notebook demos:** Interactive exploration and rapid prototyping.
- **Extensible tooling:** Easily add custom tasks and agents.

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/Hrishitcodethis/crewAI-trip-planner.git
   cd crewAI-trip-planner
   ```

2. **Install dependencies:**
   - With [Poetry](https://python-poetry.org/):
     ```sh
     poetry install
     ```
   - Or manually (see `pyproject.toml` for dependencies).

3. **Set up OpenAI API key:**
   - The API key is already configured in the code
   - Alternatively, you can set it as an environment variable:
     ```sh
     export OPENAI_API_KEY="your-api-key"
     ```

## Usage

- **Interactive notebook demo:**  
  Open `langgraph_rag_agent_llama3_local (1).ipynb` in JupyterLab to explore or test the planner.
- **Run main script:**  
  ```sh
  poetry run python main.py
  ```
  Or, if not using Poetry:
  ```sh
  python main.py
  ```

## Project Structure

- `main.py` — Main entry point for the planner.
- `agents.py` — Definitions of agent logic and orchestration.
- `tasks.py` — Task definitions and workflows.
- `tools/` — Additional utilities and tools for agents.
- `pyproject.toml` / `poetry.lock` — Dependency management.

## Requirements

- Python 3.8+
- Poetry (recommended) or pip
- OpenAI API key

## Contributing

Pull requests and issues are welcome! Please open an issue for bug reports or feature suggestions.

## License

[MIT](LICENSE) (or specify your license here)

---

> **Note:** This README is based on the current repository contents. For a full list of files, visit the [project directory](https://github.com/Hrishitcodethis/crewAI-trip-planner/tree/main/).
