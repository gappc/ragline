import inspect
import json
import logging
import sys

import loguru


logger = loguru.logger
logger.remove()
logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DDTHH:mm:ss,SSS} - {name} - {level} - ({extra[request_id]}) {message}",
    level="DEBUG",
)


# Custom serialization of log records
def serialize(record):
    subset = {
        "time": record["time"].isoformat(),
        "message": record["message"],
        "level": record["level"].name,
        "extra": record["extra"],
        "timestamp": record["time"].timestamp(),
    }
    return json.dumps(subset)


def patching(record):
    record["extra"]["serialized"] = serialize(record)


# Chat sessions and events (prompts, responses, feedback) are logged to a separate file
logger = logger.patch(patching)
logger.add(
    "./log/chat_sessions.log",
    format="{extra[serialized]}",
    level="DEBUG",
    filter=lambda record: "cid" in record["extra"] and "qid" in record["extra"],
)


def logger_bind(chat_session_id: str | None, query_id: str | None):
    return logger.bind(cid=chat_session_id).bind(qid=query_id)


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )
