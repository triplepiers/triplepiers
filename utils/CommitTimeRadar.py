import requests, os
from collections import Counter
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# --- 配置信息 ---
USERNAME = 'triplepiers'
TOKEN = os.getenv('GITHUB_TOKEN')
TIMEZONE_OFFSET = 8  

def fetch_data(username, token):
    """基于 GITHUB API 获取推送时间"""
    url = f"https://api.github.com/users/{username}/events"
    headers = {'Accept': 'application/vnd.github.v3+json', 'Authorization': f'token {token}'}
    hours = []
    for page in range(1, 11):
        try:
            r = requests.get(url, headers=headers, params={'page': page, 'per_page': 100})
            if r.status_code != 200: break
            events = r.json()
            if not events: break
            for event in events:
                if event['type'] == 'PushEvent':
                    dt = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=TIMEZONE_OFFSET)
                    hours.append(dt.hour)
        except:
            break
    return hours

def plot_advanced_radar(hours):
    """绘制提交时间分布雷达图"""    
    # 1. 数据处理与步进采样
    counts = Counter(hours)
    total = len(hours)
    percentages = [float((counts.get(h, 0) / total) * 100) for h in range(24)]
    
    step_angles = []
    step_data = []
    angles = np.linspace(0, 2 * np.pi, 24, endpoint=False)
    width = (2 * np.pi) / 24
    
    for i in range(24):
        step_angles.extend([angles[i], angles[i] + width])
        step_data.extend([percentages[i], percentages[i]])
    
    step_angles.append(step_angles[0])
    step_data.append(step_data[0])
    
    # 2. 画布设置
    fig = plt.figure(figsize=(10, 10), facecolor='none')
    ax = fig.add_axes([0.1, 0.15, 0.8, 0.8], polar=True, facecolor='none')
    
    # 3. 渐变填充与
    cmap = LinearSegmentedColormap.from_list('pixel_green', ['#1B4F72', '#3DB580', '#216e39'])
    for i in range(1, 11):
        ax.fill(step_angles, np.array(step_data) * (i/10), color=cmap(i/10), alpha=0.12)
    
    # 4. 轮廓线
    ax.plot(step_angles, step_data, color='#3DB580', linewidth=2.5, antialiased=False)
    
    # 5. 极坐标细节定制
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.spines['polar'].set_color('#3DB580')
    ax.spines['polar'].set_linewidth(2)
    
    # 刻度设置（像素风等宽字体）
    font_props = {'family': 'monospace', 'weight': 'bold', 'color': '#3DB580', 'fontsize': 11}
    ax.set_thetagrids(np.degrees(angles), [f"{i}h" for i in range(24)], **font_props)
    ax.set_yticklabels([]) # 隐藏百分比数字
    ax.grid(color='#3DB580', linestyle=':', alpha=0.4)

    # 6. 底部居中显示分析时间
    # 获取当前时间并格式化
    analysis_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    footer_text = f"Analyzed @ {analysis_time} (UTC+{TIMEZONE_OFFSET})"
    
    fig.text(0.5, 0.05, footer_text, 
             fontsize=12, family='monospace', color='#3DB580',
             ha='center', va='center', weight='bold')

    # 7. 导出透明居中的图片
    output_name = './imgs/github_commit_radar.png'
    plt.savefig(output_name, transparent=True, dpi=300, bbox_inches=None)


if __name__ == '__main__':
    hours_data = fetch_data(USERNAME, TOKEN)
    plot_advanced_radar(hours_data)