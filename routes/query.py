from flask import Blueprint, request, jsonify
from services.chroma_client import chroma
from services.groq_client import groq_client

query_bp = Blueprint("query", __name__)


@query_bp.route("/query", methods=["POST"])
def query():
    """
    Contract Query with AI
    ---
    tags:
      - Contract Query
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            query:
              type: string
              example: payment terms missing

    responses:
      200:
        description: Success
    """

    data = request.get_json()

    if not data or "query" not in data:
        return jsonify({"error": "Query required"}), 400

    user_query = data["query"]

    # 🔹 Fetch related contract documents from vector DB
    results = chroma.query(user_query)

    # 🔹 AI response using query + context
    ai_prompt = f"""
You are a contract lifecycle knowledge assistant.

Answer the query using ONLY the provided context.

CONTEXT:
{results}

QUESTION:
{user_query}

If the answer is not found in the context, reply:
"The provided context does not contain enough information to answer this question."

Return only plain text.
"""

    ai_response = groq_client.generate(ai_prompt)

    return jsonify({
        "query": user_query,
        "results": results,
        "ai_response": ai_response
    })
    