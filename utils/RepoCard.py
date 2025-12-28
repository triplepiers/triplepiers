import requests, os
from playwright.sync_api import sync_playwright

# --- 配置信息 ---
USERNAME = 'triplepiers'
TOKEN = os.getenv('GITHUB_TOKEN', '')
TITLE_CLR = '#3DB580'    # 标题颜色
REPOS = [                  # 需要生成卡片的 repo names
    "MAD-at-ZJUSE",
    "Crazy-ZZB",
    "iGEM24-WP-Tutorial",
    "autoWiki"
]

def get_repo_stats(repo_name):
    """动态获取仓库数据"""
    url = f"https://api.github.com/repos/{USERNAME}/{repo_name}"
    headers = {'Authorization': f'token {TOKEN}'}
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status() # 抛出 HTTP 错误
        repo_data = r.json()
        stars = repo_data.get('stargazers_count', 0)
        forks = repo_data.get('forks_count', 0)
        description = repo_data.get('description', '')# None 转为空字符串
        return stars, forks, description
    except requests.exceptions.RequestException as e:
        print(f"Error fetching repo stats: {e}")
        return 0, 0, ''

def generate_html_card(repo_name, stars, forks, desc):
    """生成 HTML 卡片字符串"""    
    html_content = f"""
    <div id="card" style="width: 350px; background-color: transparent; border: 1px solid #30363d; border-radius: 6px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; text-align: left; overflow: hidden;">
        <div style="padding: 16px;">
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <svg fill="#8b949e" viewBox="0 0 16 16" version="1.1" width="16" height="16" style="margin-right: 8px;">
                    <path d="M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5v-9zm10.5-1h-8a1 1 0 00-1 1v6.708A2.486 2.486 0 014.5 9h8v-7.5zM5 12.25a1 1 0 100 2 1 1 0 000-2z"></path>
                </svg>
                <span style="color: {TITLE_CLR}; font-size: 14px; font-weight: 600;">
                    {USERNAME} / {repo_name}
                </span>
            </div>
            
            <div style="color: #8b949e; font-size: 12px; margin-bottom: 8px; margin-left: 25px; line-height: 1.5;">
                {desc}
            </div>

            <div style="margin-left: 25px; display: flex; align-items: center; color: #8b949e; font-size: 12px;">
                <span style="margin-right: 16px; display: flex; align-items: center;">
                    <svg fill="currentColor" viewBox="0 0 16 16" width="14" height="14" style="margin-right: 4px;">
                      <path d="M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25zm0 2.445L6.615 5.5a.75.75 0 01-.564.41l-3.097.45 2.24 2.184a.75.75 0 01.216.664l-.528 3.084 2.769-1.456a.75.75 0 01.698 0l2.77 1.456-.53-3.084a.75.75 0 01.216-.664l2.24-2.183-3.096-.45a.75.75 0 01-.564-.41L8 2.694v.001z"></path>
                    </svg>
                    {stars}
                </span>
                <span style="margin-right: 16px; display: flex; align-items: center;">
                    <svg fill="currentColor" viewBox="0 0 16 16" width="14" height="14" style="margin-right: 4px;">
                      <path d="M5 5.372v.878c0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75v-.878a2.25 2.25 0 111.5 0v.878a3.75 3.75 0 01-3.75 3.75H6.75v.878a2.25 2.25 0 11-1.5 0v-.878A3.75 3.75 0 011.5 6.25v-.878a2.25 2.25 0 111.5 0zM5 3.25a.75.75 0 10-1.5 0 .75.75 0 001.5 0zm6.75.75a.75.75 0 100-1.5.75.75 0 000 1.5zm-6.75 9a.75.75 0 100-1.5.75.75 0 000 1.5z"></path>
                    </svg>
                    {forks}
                </span>
            </div>
        </div>
    </div>
    """
    return html_content

def capture_html_as_png(html_content, output_path):
    """基于 playwright 生成 HTML 截图"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # 注意：这里可能需要调整 device_scale_factor 来控制输出图片的清晰度
        # 1.0 是正常，2.0 是 Retina 屏效果
        context = browser.new_context(device_scale_factor=2.0) 
        page = context.new_page()
        
        # 为了让图片加载，可以先写入一个临时文件，再加载文件URL
        # 或者直接设置 content，但可能需要等待图片加载
        temp_html_path = "temp_card.html"
        with open(temp_html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        page.goto(f"file://{os.path.abspath(temp_html_path)}")
        page.wait_for_load_state("networkidle") 
        
        # 截取特定 id 的元素
        card_element = page.locator("#card")
        card_element.screenshot(path=output_path, omit_background=True)
        
        browser.close()
        # 清理临时 HTML 文件
        os.remove(temp_html_path)

if __name__ == "__main__":
    for repo_name in REPOS:
        # 获取仓库详情
        stars, forks, desc = get_repo_stats(repo_name)
        # 构建 HTML 卡片
        final_html_card = generate_html_card(repo_name, stars, forks, desc)
        # 使用 Playwright 截图并保存
        output_path = f'./imgs/{repo_name}_card.png'
        capture_html_as_png(final_html_card, output_path)