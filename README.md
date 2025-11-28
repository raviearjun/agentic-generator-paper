# Agentic AI Framework Generator

## Description

This project is a tool/pipeline that automatically generates Agentic AI framework code from Knowledge Graphs (KGs) of Agentic AI patterns. The system reads KGs constructed using the [Agentic AI Ontology](https://w3id.org/agentic-ai/onto) and transforms them into executable code for target frameworks such as CrewAI and AutoGen.

### Project Overview

The generator bridges the gap between abstract agentic AI patterns defined in ontologies and concrete implementations in popular agentic AI frameworks. By parsing Knowledge Graphs that describe agentic AI patterns, the tool can automatically produce runnable code that implements these patterns in different target frameworks.

### Key Features

- **Ontology-based Generation**: Uses the standard Agentic AI Ontology (https://w3id.org/agentic-ai/onto) as the foundation
- **Multi-framework Support**: Generates code for multiple agentic AI frameworks:
  - CrewAI
  - AutoGen
- **Knowledge Graph Parsing**: Reads and interprets KGs in RDF/Turtle format (.ttl, .rdf)
- **Pattern Recognition**: Extracts agentic AI patterns including agents, tasks, tools, and workflows
- **Automated Code Generation**: Produces executable Python scripts for target frameworks

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nauraranantya/agentic-generator.git
   cd agentic-generator
   ```
2.	Create and activate a virtual environment:
   ```bash
  python -m venv venv
  source venv/bin/activate       # macOS/Linux
  venv\Scripts\activate          # Windows
  ```
3. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Usage
1. Place the Knowledge Graph (in .ttl or .rdf format) inside the data/ folder.
   Example: data/dummy_kg.ttl
2. Run the parser to extract ontology elements:
   ```bash
   python src/parser.py
   ```
3. Generate CrewAI framework code:
   ```bash
   python src/mapper_crewai.py
   ```
4. Generate AutoGen framework code:
   ```bash
   python src/mapper_autogen.py
   ```
5. Check the output/ folder for generated scripts:
	•	crewai_generated.py
	•	autogen_generated.py

