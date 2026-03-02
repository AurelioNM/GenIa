import logging
import os
from typing import List

from langchain_community.embeddings import OllamaEmbeddings
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from models.question_and_answer import QuestionAndAnswer


class QuestionStorage:
    def __init__(self, db_connection: MongoClient):
        self.logger = logging.getLogger(__name__)
        self.db_connection: MongoClient = db_connection
        self.collection = self.db_connection.get_collection("question_and_answer")
        self.embedding_model = OllamaEmbeddings(
            model="nomic-embed-text",
            base_url=os.getenv("OLLAMA_BASE_URL"),
        )
        self.min_score = 0.80

    def search_similar_questions(self, customer_question: str, limit: int = 3):
        try:
            self.logger.info(f"Searching similar questions for: {customer_question}")

            query_embedding = self.embedding_model.embed_query(customer_question)

            pipeline = [
                {
                    "$vectorSearch": {
                        "index": "qa_vector_index",
                        "path": "embedding",
                        "queryVector": query_embedding,
                        "numCandidates": 30,
                        "limit": limit,
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "subject": 1,
                        "question": 1,
                        "answer": 1,
                        "score": {"$meta": "vectorSearchScore"},
                    }
                },
                {"$match": {"score": {"$gte": self.min_score}}},
            ]

            results = list(self.collection.aggregate(pipeline))

            self.logger.info(f"Found {len(results)} similar questions: {results}")

            return results
        except PyMongoError as e:
            self.logger.error(f"Searching similar questions failed: {e}")
            raise

    def create_question_and_answer(
        self, question_and_answers: List[QuestionAndAnswer]
    ) -> str:
        try:
            self.logger.info(
                f"Generating embeddings and in DB: Q&A={question_and_answers}"
            )

            self.logger.info(f"Generating test embedding")

            test = self.embedding_model.embed_query("hello world")
            self.logger.info(f"Generated test embedding: {test[:5]}...")

            documents = []

            for entity in question_and_answers:
                text_to_embed = f"Subject: {entity.subject}\nQuestion: {entity.question}\nAnswer: {entity.answer}"

                embedding = self.embedding_model.embed_query(text_to_embed)
                self.logger.info(
                    f"Generated embedding for Q&A: question={entity.question}, embedding={embedding[:5]}..."
                )

                documents.append(
                    {
                        "subject": entity.subject,
                        "question": entity.question,
                        "answer": entity.answer,
                        "embedding": embedding,
                    }
                )

            self.collection.insert_many(documents)

            self.logger.info(f"Documents saved in DB")
        except PyMongoError as e:
            self.logger.error(
                f"Failed to create question and answer in DB. PyMongoError: {e}"
            )
            raise
