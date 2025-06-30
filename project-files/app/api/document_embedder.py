import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Connect to or create index
index_name = "smart-city-index"

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,  # MiniLM model output size
        metric='cosine',
        spec=ServerlessSpec(cloud='aws', region='us-west-2')
    )

index = pc.Index(index_name)

# Sample documents
documents = [
    {"id": "doc1", "text": "Smart cities aim to improve sustainability through efficient energy usage..."},
    {"id": "doc2", "text": "Policy for water conservation in urban areas includes rainwater harvesting..."},
]

# Load embedding model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Prepare data
vectors = []
for doc in documents:
    embedding = model.encode(doc["text"]).tolist()
    vectors.append({
        "id": doc["id"],
        "values": embedding,
        "metadata": {"text": doc["text"]}
    })

# Upload to Pinecone
index.upsert(vectors=vectors)

print("✅ Documents embedded and uploaded to Pinecone!")
