from logging import Logger
from elasticsearch.client import Elasticsearch
from elasticsearch.helpers import streaming_bulk
from collections import Counter
from dataclasses import dataclass
from typing import List, Iterable, Union, AsyncIterable
from jeeng.shared.common import CompositeDict


def elastic_connect(es_url: str, es_user: str, es_password: str) -> Elasticsearch:
    return Elasticsearch(
        hosts=[es_url],
        http_auth=(es_user, es_password),
        scheme="https",
        port=9200,
        timeout=180,
        max_retries=3,
        retry_on_timeout=True
    )


def get_hits(r: CompositeDict) -> List[CompositeDict]:
    if r.get('status', 0) != 200 or r.get('timed_out', False) or not (hits := r.get('hits', {}).get('hits', [])):
        return []
    return hits


IterableActions = Union[Iterable[CompositeDict], AsyncIterable[CompositeDict]]


@dataclass(frozen=True)
class BulkUpserterResult:
    op_type: str
    success: int
    errors: List[CompositeDict]

    def log(self, name: str, logger: Logger):
        if not self.errors:
            logger.info(f'{name}: {self.success} ok')
        else:
            error_types = (d[self.op_type].get('error', {}).get('type', "UNKNOWN_ERROR") for d in self.errors)
            break_down = "error_types: " + "; ".join(
                f"{k}: {v}"
                for k, v in sorted(Counter(error_types).items(), key=lambda t: -t[1]))
            logger.warning(f'{name}: {self.success} ok, {len(self.errors)} failed, {break_down}')
        return self


class BulkUpserter:
    def __init__(self, elastic_client: Elasticsearch, index: str, request_timeout: int = 120):
        self.elastic_client = elastic_client
        self.index = index
        self.request_timeout = request_timeout

    def _prep_action(self, action: CompositeDict, op_type: str):
        action["_index"] = self.index
        action["_op_type"] = op_type
        return action

    def bulk_index(self, actions: IterableActions):
        return self.bulk_actions(op_type="index", actions=actions)

    def bulk_update(self, actions: IterableActions):
        return self.bulk_actions(op_type="update", actions=actions)

    def bulk_actions(self, actions: IterableActions, op_type: str) -> BulkUpserterResult:
        success = 0
        errors = []
        for ok, item in streaming_bulk(
            client=self.elastic_client,
            actions=(self._prep_action(action, op_type) for action in actions) if op_type else actions,
            raise_on_error=False,
            raise_on_exception=True,
            max_retries=3,
            yield_ok=True,
            request_timeout=self.request_timeout
        ):
            if ok:
                success += 1
            else:
                errors.append(item)
        # TODO can retry here
        self.elastic_client.indices.refresh(index=self.index)
        return BulkUpserterResult(op_type=op_type, success=success, errors=errors)
