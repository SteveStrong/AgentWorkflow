from src.agents.transform_agent import TransformAgent
import os
from qdrant_client import QdrantClient, models
import json
from datetime import datetime
import spacy
from qdrant_client.models import VectorParams, PointStruct
import uuid


class QdrantAgent(TransformAgent):
    output_ext = "vector"
    nlp = spacy.load("en_core_web_lg")  # Move spaCy initialization here

    def __init__(self, step_num: int, scenario_id: str):
        super().__init__(step_num)
        self.scenario_id = scenario_id
        QDRANT_CA_CERT = os.getenv("QDRANT_CA_CERT", None)
        self.qdrant_instance = QdrantClient(
            url="https://qdrant.readyone.net/",
            port=443,
            https=True,
            verify=QDRANT_CA_CERT,
        )

    def process_tdp_content(self, content: bytes) -> bytes:
        print(f"Starting Step {self.step_num}")
        collection_name = self.scenario_id.lower()
        timestamp = datetime.utcnow().isoformat()

        try:
            collection_exists = self.qdrant_instance.collection_exists(
                collection_name=collection_name
            )
            if not collection_exists:
                self.qdrant_instance.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(
                        size=300, distance=models.Distance.COSINE
                    ),
                )
            content_chunks = json.loads(content.decode('utf-8'))

            responses = []
            points = []
            print(f"Processing {len(content_chunks)} content chunks")
            for chunk in content_chunks:
                # chunk["timestamp"] = timestamp
                text_content = (
                    "\n".join(chunk["text"])
                    if isinstance(chunk["text"], list)
                    else str(chunk["text"])
                )
                try:
                    doc = self.nlp(text_content)
                    embedding = doc.vector.tolist()
                    point_id = str(uuid.uuid4())
                    points.append(
                        PointStruct(
                            id=point_id,
                            vector=embedding,
                            payload={
                                "text": text_content,
                            },
                        )
                    )

                    # Upsert in batches of 50
                    if len(points) >= 50:
                        qdrant_response = self.qdrant_instance.upsert(
                            collection_name=collection_name, points=points
                        )
                        points = []  # Clear the batch

                except Exception as e:
                    print(f"Qdrant connection error for chunk: {e}")
                    responses.append({
                        "status": "error",
                        "message": "Elasticsearch service unavailable",
                        "error": str(e),
                        "chunk_id": chunk.get("chunk", "unknown")[:50] + "..."
                    })

            # Upsert any remaining points
            if points:
                qdrant_response = self.qdrant_instance.upsert(
                    collection_name=collection_name, points=points
                )

            responses.append({
                "status": "success",
                "message": f"Processed {len(content_chunks)} chunks and inserted into Qdrant collection '{collection_name}'"
            })

            content = json.dumps(responses, ensure_ascii=False).encode("utf-8")
            print(f"Step {self.step_num} Completed")

        except Exception as e:
            print(f"Error in Step {self.step_num}: {e}")
            error_response = [{
                "status": "error",
                "message": "Failed to process content",
                "error": str(e)
            }]
            content = json.dumps(error_response, ensure_ascii=False).encode("utf-8")

        return content

