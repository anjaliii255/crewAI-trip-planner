# crewAI-trip-planner

A smart, agent-based trip planner leveraging AI and Llama models for generating and managing travel itineraries. Built with Python and Jupyter Notebook, this project aims to automate and optimize trip planning with advanced reasoning and retrieval capabilities.

## Features

- **Agent-based planning:** Modular agents coordinate to create and refine trip plans.
- **Integration with Llama3:** Utilizes Llama3 models for reasoning and retrieval-augmented generation (RAG).
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

3. **(Optional) Set up Llama3 model:**
   - Refer to `Llama3Modelfile.txt` for details.
   - You may need to run the setup script:
     ```sh
     ./llama3crew.sh
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
- `Llama3Modelfile.txt` — Model configuration/instructions.
- `llama3crew.sh` — Shell script for environment/model setup.
- `pyproject.toml` / `poetry.lock` — Dependency management.

## Requirements

- Python 3.8+
- Poetry (recommended) or pip
- Compatible hardware for running Llama3 models (see model file for details)

## Contributing

Pull requests and issues are welcome! Please open an issue for bug reports or feature suggestions.

## License

[MIT](LICENSE) (or specify your license here)

---

> **Note:** This README is based on the current repository contents. For a full list of files, visit the [project directory](https://github.com/Hrishitcodethis/crewAI-trip-planner/tree/main/).
