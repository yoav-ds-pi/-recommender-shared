from dataclasses import dataclass


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
    URL_USER_INDEX='url_user_index_synt_small',
    SCORED_URLS_INDEX='scored_urls_synt_small',
    N_DOMAINS=2,
    N_URLS=100,
    N_SUBS=200,
    N_ENTS=3,
    N_VISITS=5
)

STRESS_LARGE = StressTestConfig(
    URL_USER_INDEX='url_user_index_synt_large',
    SCORED_URLS_INDEX='scored_urls_synt_large',
    N_DOMAINS=4,
    N_URLS=5000,
    N_SUBS=5000,
    N_ENTS=5,
    N_VISITS=10
)
