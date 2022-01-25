import hashlib
from typing import Any, Optional, Union

CompositeDict = dict[str, Any]

RDB_URLS = 1  # SUB_TO_EXCLUDED_URLS, DOMAIN_TO_CANDIDATES
RDB_SUB_TO_RECS = 2


def str_to_bool(s: Optional[str]) -> bool:
    return s is not None and s.lower() in {'yes', 'true', '1', 'on'}


def to_uint(s: str, default: int) -> int:
    return int(s) if s and s.isdigit() else default


def sub_ids_to_keys(domain_id: str, sub_ids: list[str]) -> list[str]:
    return [f'{domain_id}:{sub_id}' for sub_id in sub_ids]


class UnimplementedException(Exception):
    def __init__(self):
        super().__init__("Unimplemented method")


############
# doc keys #
############


def str_digest(s: str) -> str:
    return hashlib.md5(s.encode("utf-8")).hexdigest()


def generate_key_url_ext(domain_id: str, url: str) -> Optional[str]:
    return f'{domain_id}-{str_digest(url)}' if url and domain_id else None


def generate_key_url_agg(domain_id: str, url: str, year: Union[int, str], dayofyear: Union[int, str]) -> Optional[str]:
    return f'{domain_id}-{str_digest(url)}-{year}-{dayofyear}' if year and dayofyear and url and domain_id else None
