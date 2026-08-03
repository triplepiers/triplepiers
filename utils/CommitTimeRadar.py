import os
from collections import Counter
from datetime import datetime, timedelta, timezone

import matplotlib.pyplot as plt
import numpy as np
import requests
from matplotlib.colors import LinearSegmentedColormap


# --- 配置信息 ---
USERNAME = "triplepiers"
TOKEN = os.getenv("GH_STATS_TOKEN", "").strip() # GitHub Actions 中由 Secret 注入
TIMEZONE_OFFSET = 8  # UTC+8


if not TOKEN:
    raise RuntimeError(
        "GH_STATS_TOKEN is empty. Configure Actions secret MY_GITHUB_TOKEN "
        "and map it to GH_STATS_TOKEN in the workflow."
    )

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

    if not response.ok:
        try:
            details = response.json().get("message", response.text)
        except ValueError:
            details = response.text

        request_id = response.headers.get("X-GitHub-Request-Id", "unknown")
        raise RuntimeError(
            f"GitHub API request failed: HTTP {response.status_code}; "
            f"message={details!r}; request_id={request_id}"
        )

    return response.json()

def fetch_owned_repos():
    """获取当前 Token 所属账号拥有的全部 public + private 仓库。"""
    repos = []

    for page in range(1, 1000):
        batch = github_get(
            "https://api.github.com/user/repos",
            type="owner",
            sort="full_name",
            direction="asc",
            per_page=100,
            page=page,
        )

        if not batch:
            break

        # 排除 fork：避免将上游项目的历史提交纳入统计。
        repos.extend(repo for repo in batch if not repo["fork"])

    return repos


def fetch_data(username):
    """
    统计本人在全部自有仓库「默认分支」完整历史中的 commit 时段。

    注意：
    - author=username 仅匹配作者邮箱已关联到该 GitHub 账号的 commit。
    - 仅统计最终可从默认分支到达的 commit；
      未合并的 feature branch commit 不在此统计范围内。
    """
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
                # 采用 Git commit author 的原始提交时间，而非 API 事件创建时间。
                created_at = commit["commit"]["author"]["date"]
                utc_dt = datetime.strptime(
                    created_at,
                    "%Y-%m-%dT%H:%M:%SZ",
                ).replace(tzinfo=timezone.utc)

                local_dt = utc_dt + timedelta(hours=TIMEZONE_OFFSET)
                hours.append(local_dt.hour)

    print(f"Scanned {len(repos)} repositories; found {len(hours)} commits.")
    return hours


def plot_advanced_radar(hours):
    """绘制提交时间分布雷达图。"""
    if not hours:
        raise RuntimeError(
            "No commits found. Check the Token permissions, GitHub username, "
            "and whether commit author emails are linked to this account."
        )

    counts = Counter(hours)
    total = len(hours)
    percentages = [(counts.get(hour, 0) / total) * 100 for hour in range(24)]

    angles = np.linspace(0, 2 * np.pi, 24, endpoint=False)
    width = (2 * np.pi) / 24
    step_angles = []
    step_data = []

    for index in range(24):
        step_angles.extend([angles[index], angles[index] + width])
        step_data.extend([percentages[index], percentages[index]])

    step_angles.append(step_angles[0])
    step_data.append(step_data[0])

    fig = plt.figure(figsize=(10, 10), facecolor="none")
    ax = fig.add_axes([0.1, 0.15, 0.8, 0.8], polar=True, facecolor="none")

    cmap = LinearSegmentedColormap.from_list(
        "pixel_green",
        ["#1B4F72", "#3DB580", "#216E39"],
    )

    for index in range(1, 11):
        ax.fill(
            step_angles,
            np.array(step_data) * (index / 10),
            color=cmap(index / 10),
            alpha=0.12,
        )

    ax.plot(
        step_angles,
        step_data,
        color="#3DB580",
        linewidth=2.5,
        antialiased=False,
    )

    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.spines["polar"].set_color("#3DB580")
    ax.spines["polar"].set_linewidth(2)

    font_props = {
        "family": "monospace",
        "weight": "bold",
        "color": "#3DB580",
        "fontsize": 11,
    }
    ax.set_thetagrids(
        np.degrees(angles),
        [f"{hour}h" for hour in range(24)],
        **font_props,
    )
    ax.set_yticklabels([])
    ax.grid(color="#3DB580", linestyle=":", alpha=0.4)

    analysis_time = datetime.now(
        timezone.utc,
    ) + timedelta(hours=TIMEZONE_OFFSET)
    footer_text = (
        f"Analyzed @ {analysis_time.strftime('%Y-%m-%d %H:%M:%S')} "
        f"(UTC+{TIMEZONE_OFFSET})"
    )

    fig.text(
        0.5,
        0.05,
        footer_text,
        fontsize=12,
        family="monospace",
        color="#3DB580",
        ha="center",
        va="center",
        weight="bold",
    )

    output_name = "./imgs/github_commit_radar.png"
    os.makedirs(os.path.dirname(output_name), exist_ok=True)

    plt.savefig(
        output_name,
        transparent=True,
        dpi=300,
        bbox_inches=None,
    )
    plt.close(fig)

    print(f"Radar chart saved to {output_name}")


if __name__ == "__main__":
    hours_data = fetch_data(USERNAME)
    plot_advanced_radar(hours_data)
