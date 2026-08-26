"""CLI / env helpers. No hardcoded Sanity project, dataset, or tokens."""
from __future__ import annotations

import argparse
import os

SANITY_PROJECT_ENV = "NEXT_PUBLIC_SANITY_PROJECT_ID"
SANITY_DATASET_ENV = "NEXT_PUBLIC_SANITY_DATASET"
SANITY_TOKEN_ENVS = (
    "SANITY_API_EDITOR_TOKEN",
    "SANITY_WRITE_TOKEN",
    "SANITY_API_WRITE_TOKEN",
    "SANITY_API_READ_TOKEN",
)
ALGOLIA_APP_ENV = "ALGOLIA_APP_ID"
ALGOLIA_KEY_ENV = "ALGOLIA_SEARCH_KEY"
API_VERSION = "2021-10-21"
ACTIONS_API_VERSION = "2024-01-01"


def first_env(*names: str) -> str | None:
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


def add_sanity_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--project-id",
        default=None,
        help=f"Sanity project id (or env {SANITY_PROJECT_ENV})",
    )
    parser.add_argument(
        "--dataset",
        default=None,
        help=f"Sanity dataset (or env {SANITY_DATASET_ENV})",
    )
    parser.add_argument(
        "--token",
        default=None,
        help=f"Sanity editor token (or env {SANITY_TOKEN_ENVS[0]})",
    )


def add_algolia_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--algolia-app-id",
        default=None,
        help=f"Algolia app id (or env {ALGOLIA_APP_ENV})",
    )
    parser.add_argument(
        "--algolia-search-key",
        default=None,
        help=f"Algolia search key (or env {ALGOLIA_KEY_ENV})",
    )


def _require(label: str, value: str | None, flag: str, env_name: str) -> str:
    if value:
        return value
    raise SystemExit(
        f"Missing {label}. Pass {flag} or prefix {env_name}=... on the CLI "
        "(collect at FIRST RUN / Definition — never hardcode)."
    )


def resolve_sanity(args: argparse.Namespace) -> tuple[str, str, str]:
    project_id = _require(
        "Sanity project id",
        args.project_id or first_env(SANITY_PROJECT_ENV),
        "--project-id",
        SANITY_PROJECT_ENV,
    )
    dataset = _require(
        "Sanity dataset",
        args.dataset or first_env(SANITY_DATASET_ENV),
        "--dataset",
        SANITY_DATASET_ENV,
    )
    token = _require(
        "Sanity editor token",
        args.token or first_env(*SANITY_TOKEN_ENVS),
        "--token",
        SANITY_TOKEN_ENVS[0],
    )
    return project_id, dataset, token


def resolve_algolia(args: argparse.Namespace) -> tuple[str, str]:
    app_id = _require(
        "Algolia app id",
        args.algolia_app_id or first_env(ALGOLIA_APP_ENV),
        "--algolia-app-id",
        ALGOLIA_APP_ENV,
    )
    api_key = _require(
        "Algolia search key",
        args.algolia_search_key or first_env(ALGOLIA_KEY_ENV),
        "--algolia-search-key",
        ALGOLIA_KEY_ENV,
    )
    return app_id, api_key


def sanity_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def sanity_mutate_url(project_id: str, dataset: str) -> str:
    return f"https://{project_id}.api.sanity.io/v{API_VERSION}/data/mutate/{dataset}"


def sanity_query_url(project_id: str, dataset: str) -> str:
    return f"https://{project_id}.api.sanity.io/v{API_VERSION}/data/query/{dataset}"


def sanity_actions_url(project_id: str, dataset: str) -> str:
    return f"https://{project_id}.api.sanity.io/v{ACTIONS_API_VERSION}/data/actions/{dataset}"


def sanity_assets_url(project_id: str, dataset: str, filename: str | None) -> str:
    url = f"https://{project_id}.api.sanity.io/v{API_VERSION}/assets/images/{dataset}"
    if filename:
        return f"{url}?filename={filename}"
    return url
