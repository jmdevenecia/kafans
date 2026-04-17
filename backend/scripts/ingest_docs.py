import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))

from app.ingest import ingest_directory

if __name__ == "__main__":
    data_path = sys.argv[1] if len(sys.argv) > 1 else "./research_data"
    print(f"Ingesting from: {data_path}")
    result = ingest_directory(data_path)
    print(f"Done — {result['ingested']} files, {result['chunks']} chunks stored.")