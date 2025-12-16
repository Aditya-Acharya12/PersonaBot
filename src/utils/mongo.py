from bson import ObjectId

def serialize_doc(doc: dict) -> dict:
    """
    Converts MongoDB document into JSON-serializable format.
    Turns ObjectId into string and handles nested ObjectIds.
    """
    if not isinstance(doc, dict):
        return doc

    serialized = {}
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            serialized[key] = str(value)
        elif isinstance(value, list):
            serialized[key] = [serialize_doc(v) for v in value]
        elif isinstance(value, dict):
            serialized[key] = serialize_doc(value)
        else:
            serialized[key] = value

    return serialized


def serialize_docs(docs: list) -> list:
    """
    Converts a list of MongoDB documents into JSON-serializable format.
    """
    return [serialize_doc(doc) for doc in docs]