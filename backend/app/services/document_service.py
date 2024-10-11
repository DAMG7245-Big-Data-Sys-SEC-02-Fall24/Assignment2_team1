from app.services.mongo import MongoDBFactory
import logging
from fastapi import HTTPException
from app.config.settings import settings
# MongoDB URI and database name (ideally this should be loaded from environment variables)
database_name = "pdf_database"

# Initialize the MongoDB factory
mongo_factory = MongoDBFactory(uri=settings.MONGO_URI, database_name=database_name)


class DocumentService:

    @staticmethod
    def query_document(collection_name: str, pdf_name: str, query_text: str):
        """
        Query a document from a specific collection by PDF name and query text.
        """
        try:
            # Query the document from the specified collection using the MongoDB factory
            document = mongo_factory.db_helper.find_document_by_pdf_name(collection_name, pdf_name)

            if not document:
                raise HTTPException(status_code=404,
                                    detail=f"No document found for pdf_name '{pdf_name}' in collection '{collection_name}'")

            # Here you would implement the logic for querying the document's content (e.g., full-text search)
            # For now, we're returning the full document as an example
            logging.info(f"Document found for pdf_name: {pdf_name} in collection: {collection_name}")
            return document

        except Exception as e:
            logging.error(f"An error occurred while querying the document: {str(e)}")
            raise HTTPException(status_code=500, detail=f"An error occurred while querying the document: {str(e)}")

    @staticmethod
    def summarize_document(collection_name: str, pdf_name: str):
        """
        Summarize a document from a specific collection by PDF name.
        """
        try:
            # Query the document from the specified collection using the MongoDB factory
            document = mongo_factory.db_helper.find_document_by_pdf_name(collection_name, pdf_name)

            if not document:
                raise HTTPException(status_code=404,
                                    detail=f"No document found for pdf_name '{pdf_name}' in collection '{collection_name}'")

            # Implement your summarization logic here. For now, we return a mock summary.
            summary = f"Mock summary for the document '{pdf_name}' in collection '{collection_name}'."
            logging.info(f"Summary created for pdf_name: {pdf_name} in collection: {collection_name}")
            return summary

        except Exception as e:
            logging.error(f"An error occurred while summarizing the document: {str(e)}")
            raise HTTPException(status_code=500, detail=f"An error occurred while summarizing the document: {str(e)}")

