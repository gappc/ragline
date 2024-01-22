import logging
import sys
import uuid

import loguru

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = loguru.logger
logger.remove()
logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DDTHH:mm:ss,SSS} - {name} - {level} - ({extra[request_id]}) {message} ",
    level="DEBUG",
)

# Queries and responses are logged to a separate file
logger.add(
    "./log/query.log",
    format="{time:YYYY-MM-DDTHH:mm:ss,SSS} - (qid:{extra[qid]}) - {message} ",
    level="DEBUG",
    filter=lambda record: "qid" in record["extra"],
    serialize=True,
)


def new_query_logger():
    query_id = uuid.uuid4().hex
    return query_id, query_logger_for_qid(query_id)


def query_logger_for_qid(qid: str):
    print("query_logger_for_qid", qid)
    return logger.bind(qid=qid)


def build_stdout_handler():
    stdout = logging.StreamHandler(stream=sys.stdout)
    stdout.setLevel(logging.DEBUG)
    stdout.setFormatter(formatter)
    return stdout
