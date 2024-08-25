import os
import requests
from datetime import datetime, timedelta

# 创建存储目录
output_dir = os.path.join(os.getcwd(), "playlists")
os.makedirs(output_dir, exist_ok=True)

def search_github_repos(query, token, days_ago):
    # GitHub API URL
    search_url = "https://api.github.com/search/repositories"
    
    # 计算指定天数前的日期
    days_ago_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
    
    # 查询参数
    params = {
        "q": f'{query} created:>{days_ago_date}',
        "sort": "created",
        "order": "desc"
    }
    
    # HTTP 请求头
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()  # 检查请求是否成功
        return response.json().get('items', [])
    except requests.exceptions.RequestException as e:
        print(f"搜索时出错: {e}")
        return []

def search_and_download_files(repo, token):
    # 获取存储库的内容
    contents_url = repo['contents_url'].replace('{+path}', '')
    
    headers = {"Authorization": f"token {token}"}
    
    try:
        response = requests.get(contents_url, headers=headers)
        response.raise_for_status()
        contents = response.json()
        
        for content in contents:
            # 检查文件后缀名，下载 .m3u, .m3u8和 .txt 文件
            if content['type'] == 'file' and content['name'].endswith(('.m3u', '.m3u8', '.txt')):
                download_and_save_file(content['download_url'], content['name'], headers)
    except requests.exceptions.RequestException as e:
        print(f"无法访问存储库 {repo['name']} 的内容: {e}")

def download_and_save_file(file_url, file_name, headers):
    try:
        response = requests.get(file_url, headers=headers)
        response.raise_for_status()
        
        file_path = os.path.join(output_dir, file_name)
        
        with open(file_path, 'wb') as file:
            file.write(response.content)
        
        print(f"已保存 {file_name} 到 {output_dir}")
    except requests.exceptions.RequestException as e:
        print(f"下载 {file_name} 失败: {e}")

def main():
    # 从环境变量中获取参数
    github_token = os.getenv('GITHUB_TOKEN', 'your_default_token')  # 默认值可以改成你的Token
    search_queries = os.getenv('SEARCH_QUERIES', '直播源').split(',')
    days_ago = int(os.getenv('DAYS_AGO', 20))
    
    # 对每个搜索关键词进行搜索
    for search_query in search_queries:
        print(f"正在搜索关键词: {search_query}")
        repos = search_github_repos(search_query.strip(), github_token, days_ago)
        
        if repos:
            for repo in repos:
                search_and_download_files(repo, github_token)
        else:
            print(f"未找到与关键词 '{search_query}' 相关的存储库。")

if __name__ == "__main__":
    main()
