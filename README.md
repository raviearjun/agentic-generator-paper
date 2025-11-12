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
      
