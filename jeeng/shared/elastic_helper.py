from elasticsearch.client import Elasticsearch
from elasticsearch.helpers import streaming_bulk
from collections import Counter
from dataclasses import dataclass
from typing import List
from jeeng.shared.common import CompositeDict


def elastic_connect(es_url: str, es_user: str, es_password: str) -> Elasticsearch:
    return Elasticsearch(
        hosts=[es_url],
        http_auth=(es_user, es_password),
        scheme="https",
        port=9200,
    )


@dataclass(frozen=True)
class BulkUpserterResult:
    num_of_actions: int
    success: int
    errors: List[CompositeDict]

    def print(self, name: str):
        if not self.errors:
            print(f'{name}: {self.num_of_actions} actions, {self.success} ok')
        else:
            print(f'{name}: {self.num_of_actions} actions, {self.success} ok, {len(self.errors)} failed')
            error_types = (d['update']['error']['type'] for d in self.errors)
            print("error_types: " + "; ".join(
                f"{k}: {v}" for k, v in sorted(Counter(error_types).items(), key=lambda t: -t[1]))
            )
        return self


class BulkUpserter:
    def __init__(self, elastic_client: Elasticsearch):
        self.elastic_client = elastic_client

    def bulk(self, actions: List[CompositeDict]) -> BulkUpserterResult:
        success = 0
        errors = []
        for ok, item in streaming_bulk(
            client=self.elastic_client,
            actions=actions,
            raise_on_error=False,
            raise_on_exception=True,
            max_retries=3,
            yield_ok=True
        ):
            if ok:
                success += 1
            else:
                errors.append(item)
        # TODO can retry here
        return BulkUpserterResult(num_of_actions=len(actions), success=success, errors=errors)
