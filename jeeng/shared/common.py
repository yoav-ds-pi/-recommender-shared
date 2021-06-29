import enum
import hashlib
from typing import Dict, Any, Optional, Union

CompositeDict = Dict[str, Any]


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
