#!/usr/bin/env python3
"""
Task 8: NoSQL (MongoDB).
"""


def list_all(mongo_collection):
    """
    List all documents in a collection.
    """
    return [document for document in mongo_collection.find()]
