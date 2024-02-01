# Simple function to stream response
import base64
import json
from collections import defaultdict
from typing import Any, Dict, List

from fastapi.responses import StreamingResponse
from llama_index.schema import NodeWithScore
from logger.custom_logger import query_logger_for_qid
from starlette.responses import ContentStream
from utils.llm import get_token_counts_as_text


def extract_response_source(source_nodes: List[NodeWithScore]):
    response_source = defaultdict(list)

    for node in source_nodes:
        response_source[node.metadata["file_name"]].append(
            int(node.metadata["page_label"])
        )

    return response_source


def stream_response(
    query_id: str,
    content: ContentStream,
    response_source: Dict[str, Any],
):
    json_sources = json.dumps(response_source)
    base64_sources = base64.b64encode(json_sources.encode("utf-8")).decode()

    return StreamingResponse(
        content,
        media_type="text/event-stream",
        headers={
            "X-RAGLINE-QUERY-ID": query_id,
            "X-RAGLINE-RESPONSE-SOURCE": base64_sources,
        },
    )


def log_response(query_id, stream):
    stream_text = "".join(stream)
    query_logger_for_qid(query_id).info("Response: {}", stream_text)
    query_logger_for_qid(query_id).info(get_token_counts_as_text())
