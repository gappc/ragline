# Simple function to stream response
import base64
import json
from collections import defaultdict
from typing import Any, Dict, List

from fastapi.responses import StreamingResponse
from llama_index.schema import NodeWithScore
from logger.custom_logger import logger_bind
from starlette.responses import ContentStream
from utils.llm import get_token_counts_as_text
import copy


def remove_embeddings(source_nodes: List[NodeWithScore]) -> List[NodeWithScore]:
    response_source: List[NodeWithScore] = []
    for node in source_nodes:
        tmp = copy.deepcopy(node)
        tmp.node.embedding = None
        response_source.append(tmp)
    return response_source


def extract_response_source(source_nodes: List[NodeWithScore]) -> Dict[str, list[int]]:
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
            "X-RAGLINE-PROMPT-ID": query_id,
            "X-RAGLINE-RESPONSE-SOURCE": base64_sources,
        },
    )


def log_response(chat_session_id, query_id, stream):
    stream_text = "".join(stream)
    logger = logger_bind(chat_session_id, query_id)
    logger.info("Response: {}", stream_text)
    logger.info(get_token_counts_as_text())
