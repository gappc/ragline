# Simple function to stream response
from fastapi.responses import StreamingResponse
from logger.custom_logger import query_logger_for_qid
from starlette.responses import ContentStream


def stream_response(query_id: str, content: ContentStream, status_code: int = 200):
    return StreamingResponse(
        content,
        status_code=status_code,
        media_type="text/event-stream",
        headers={
            "X-RAGLINE-QUERY-ID": query_id,
        },
    )


def log_response(query_id, stream):
    stream_text = "".join(stream)
    query_logger_for_qid(query_id).info("Response: {}", stream_text)
