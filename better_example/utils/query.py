from llama_index.indices.query.query_transform.base import HyDEQueryTransform
from llama_index.query_engine.transform_query_engine import TransformQueryEngine
from llama_index.vector_stores.types import ExactMatchFilter, MetadataFilters
from utils.context import index

RAGLINE_USER_KEY = "ragline_user"


def query_by_term(username: str, term: str):
    # hyde = HyDEQueryTransform(include_original=True)

    query_engine = index.as_query_engine(
        streaming=True,
        filters=MetadataFilters(
            filters=[
                ExactMatchFilter(
                    key=RAGLINE_USER_KEY,
                    value=username,
                )
            ]
        ),
        similarity_top_k=5,
    )

    # query_engine = TransformQueryEngine(query_engine, query_transform=hyde)

    response = query_engine.query(term)
    return response


if __name__ == "__main__":
    print("Nothing")
