# Simple function to stream response
import base64
import json
from collections import defaultdict
from typing import Any, Dict

from fastapi.responses import StreamingResponse
from logger.custom_logger import query_logger_for_qid
from starlette.responses import ContentStream


def extract_response_source(response_metadata: Dict[str, Any] | None = None):
    response_source = defaultdict(list)
    if response_metadata:
        for key, metadata in response_metadata.items():
            response_source[metadata["file_name"]].append(int(metadata["page_label"]))

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
