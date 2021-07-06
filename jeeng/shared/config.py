from dataclasses import dataclass, field

BASE_INDEX_SCORED_URLS = 'scored_urls'
BASE_INDEX_URL_USER = 'url_user_index'


@dataclass(frozen=True)
class StressTestConfig:
    SUB_ENV: str
    INDEX_URL_USER: str = field(init=False)
    INDEX_SCORED_URLS: str = field(init=False)
    N_DOMAINS: int
    N_URLS: int
    N_SUBS: int
    N_ENTS: int
    N_VISITS: int
    BATCH_SIZE: int = 1000

    def __post_init__(self):
        postfix = '_' + self.SUB_ENV if self.SUB_ENV and self.SUB_ENV.lower() != 'none' else ''
        object.__setattr__(self, 'INDEX_SCORED_URLS', BASE_INDEX_SCORED_URLS + postfix)
        object.__setattr__(self, 'INDEX_URL_USER', BASE_INDEX_URL_USER + postfix)


STRESS_SMALL = StressTestConfig(
    SUB_ENV='synt_small',
    N_DOMAINS=2,
    N_URLS=100,
    N_SUBS=200,
    N_ENTS=3,
    N_VISITS=5
)

STRESS_LARGE = StressTestConfig(
    SUB_ENV='synt_large',
    N_DOMAINS=4,
    N_URLS=5000,
    N_SUBS=5000,
    N_ENTS=5,
    N_VISITS=10
)
