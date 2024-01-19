import logging
import sys
from better_example.utils.context import query_engine

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

question = "What is gnurkpfu?"

print("Asking question: " + question)

response = query_engine.query(question)
response.print_response_stream()
