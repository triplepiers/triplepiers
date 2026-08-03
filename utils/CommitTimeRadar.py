import requests
from collections import Counter
from datetime import datetime, timedelta, timezone

USERNAME = "triplepiers"
TOKEN = os.environ["GH_STATS_TOKEN"]  # 不要允许 token 静默为空
TIMEZONE_OFFSET = 8

API_HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
}


def github_get(url, **params):
    response = requests.get(
        url,
        headers=API_HEADERS,
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def fetch_owned_repos():
    """获取当前 Token 所属账号拥有的全部 public + private 仓库。"""
    repos = []

    for page in range(1, 1000):
        batch = github_get(
            "https://api.github.com/user/repos",
            visibility="all",
            affiliation="owner",
            type="owner",
            sort="full_name",
            direction="asc",
            per_page=100,
            page=page,
        )
        if not batch:
            break

        # fork 默认不计入，避免将上游历史误认为自己的提交。
        repos.extend(repo for repo in batch if not repo["fork"])

    return repos


def fetch_data(username, token=None):
    """统计本人在所有自有仓库默认分支中、完整历史范围内的 commit 时段。"""
    hours = []
    repos = fetch_owned_repos()

    for repo in repos:
        repo_name = repo["full_name"]
        print(f"Scanning {repo_name} ...")

        for page in range(1, 100000):
            commits = github_get(
                f"https://api.github.com/repos/{repo_name}/commits",
                author=username,
                per_page=100,
                page=page,
            )
            if not commits:
                break

            for commit in commits:
                # 使用 Git commit 中 author 的原始提交时间，而不是 API 返回时间。
                created_at = commit["commit"]["author"]["date"]
                dt = datetime.strptime(
                    created_at, "%Y-%m-%dT%H:%M:%SZ"
                ).replace(tzinfo=timezone.utc)

                local_dt = dt + timedelta(hours=TIMEZONE_OFFSET)
                hours.append(local_dt.hour)

    print(f"Scanned {len(repos)} repositories, found {len(hours)} commits.")
    return hours
