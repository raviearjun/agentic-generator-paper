import os
from src.parser import parse_kg
from src.mapper_crewai import generate_crewai_code
from src.mapper_autogen import generate_autogen_code

DATA_DIR = "data"
OUTPUT_DIR = "output"
PROCESSED_COUNT = 0

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    
print("Memulai Konversi KG ke Script Agentic AI")

# Iterasi setiap file di folder 'data'
for filename in os.listdir(DATA_DIR):
    # Hanya proses file KG (.ttl atau .rdf)
    if filename.endswith(".ttl") or filename.endswith(".rdf"):
        
        kg_path = os.path.join(DATA_DIR, filename)
        base_name = os.path.splitext(filename)[0] # Contoh: 'pattern_1'

        print(f"\n[Processing] {filename}")
        
        try:
            # 1. Parsing (Ekstraksi data dari KG)
            # Hasil: struktur data Python (dict)
            parsed_data = parse_kg(kg_path) 
            
            # 2. Mapping ke CrewAI
            crewai_code = generate_crewai_code(parsed_data)
            crewai_output_path = os.path.join(OUTPUT_DIR, f"crewai_{base_name}.py")
            with open(crewai_output_path, "w") as f:
                f.write(crewai_code)
            print(f"   -> CrewAI Code Generated: {crewai_output_path}")

            # 3. Mapping ke AutoGen
            autogen_code = generate_autogen_code(parsed_data)
            autogen_output_path = os.path.join(OUTPUT_DIR, f"autogen_{base_name}.py")
            with open(autogen_output_path, "w") as f:
                f.write(autogen_code)
            print(f"   -> AutoGen Code Generated: {autogen_output_path}")
            
            PROCESSED_COUNT += 1

        except Exception as e:
            print(f"   [ERROR] Gagal memproses {filename}: {e}")
            # Jika ada error, hentikan loop
            # Jika hanya error karena tidak ada file dummy_kg.ttl, 
            # ini akan ditangani oleh parser.py

# Print Hasil
print(f"\nSelesai. Total {PROCESSED_COUNT} KG berhasil dikonversi.")