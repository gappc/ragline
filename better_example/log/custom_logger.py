import sys
import logging
import loguru

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = loguru.logger
logger.remove()
logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DDTHH:mm:ss,SSS} - {name} - {level} - ({extra[request_id]}) {message} ",
    level="DEBUG",
)


def build_stdout_handler():
    stdout = logging.StreamHandler(stream=sys.stdout)
    stdout.setLevel(logging.DEBUG)
    stdout.setFormatter(formatter)
    return stdout
