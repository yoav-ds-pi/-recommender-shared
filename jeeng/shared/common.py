import enum
import hashlib
from typing import Dict, Any

CompositeObj = Dict[str, Any]


class Events(enum.Enum):
    url_extracted = 1
    user_visited_page = 2


def generate_url_ext_key(url: str, domain_id: str):
    if url and domain_id:
        return f'{domain_id}-{hashlib.md5(url.encode("utf-8")).hexdigest()}'
    return None


def generate_url_agg_key(year, dayofyear, url, domain_id):
    if year and dayofyear and url and domain_id:
        return f'{domain_id}-{hashlib.md5(url.encode("utf-8")).hexdigest()}-{year}-{dayofyear}'
    return None
