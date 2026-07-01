"""Configuration — provider, model, the ICP, and the qualification thresholds.

Default provider is ``mock``: a deterministic crew so the pipeline runs, tests, and gates CI with no
keys. ``SDR_PROVIDER=openai`` (or ``anthropic``) switches to a real CrewAI crew. The ICP and the tier
thresholds are policy and live here.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SDR_", env_file=".env", extra="ignore")

    provider: str = "mock"  # "mock" | "openai" | "anthropic"
    model: str = "gpt-5.2"

    # Ideal Customer Profile (comma-separated env overrides supported).
    icp_industries: str = "saas,fintech,e-commerce,healthtech,devtools"
    icp_regions: str = "north america,europe"
    icp_min_employees: int = 50
    icp_max_employees: int = 5000

    # Tier thresholds on the 0-100 fit score.
    tier_a: int = 80
    tier_b: int = 60
    tier_c: int = 40

    cost_ceiling_usd: float = 0.30
    web_origin: str = "http://localhost:3000"

    def industries(self) -> set[str]:
        return {s.strip().lower() for s in self.icp_industries.split(",") if s.strip()}

    def regions(self) -> set[str]:
        return {s.strip().lower() for s in self.icp_regions.split(",") if s.strip()}


_CACHE: dict[str, Settings] = {}


def get_settings(name: str = "default") -> Settings:
    if name not in _CACHE:
        _CACHE[name] = Settings()
    return _CACHE[name]


def reset_settings(name: str = "default") -> None:
    _CACHE.pop(name, None)
