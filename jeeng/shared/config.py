from dataclasses import dataclass

BASE_INDEX_SCORED_URLS = 'scored_urls'
BASE_INDEX_URL_USER = 'url_user_index'

@dataclass(frozen=True)
class StressTestConfig:
    URL_USER_INDEX: str
    SCORED_URLS_INDEX: str
    N_DOMAINS: int
    N_URLS: int
    N_SUBS: int
    N_ENTS: int
    N_VISITS: int
    BATCH_SIZE: int = 1000


STRESS_SMALL = StressTestConfig(
    URL_USER_INDEX=BASE_INDEX_URL_USER+'_synt_small',
    SCORED_URLS_INDEX=BASE_INDEX_SCORED_URLS+'_synt_small',
    N_DOMAINS=2,
    N_URLS=100,
    N_SUBS=200,
    N_ENTS=3,
    N_VISITS=5
)

STRESS_LARGE = StressTestConfig(
    URL_USER_INDEX=BASE_INDEX_URL_USER+'_synt_large',
    SCORED_URLS_INDEX=BASE_INDEX_SCORED_URLS+'_synt_large',
    N_DOMAINS=4,
    N_URLS=5000,
    N_SUBS=5000,
    N_ENTS=5,
    N_VISITS=10
)
