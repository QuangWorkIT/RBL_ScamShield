"""
Jira Integration Script for ScamShield-VN (RBL)
Connects to Jira Cloud REST API, fetches boards, sprints, and issues.
"""

import os
import sys
import json
import base64
import urllib.request
import urllib.error

sys.stdout.reconfigure(encoding='utf-8')

# Load from .env if available
def load_env(env_path):
    env = {}
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    env[k.strip()] = v.strip()
    return env

class JiraClient:
    def __init__(self, base_url, email, api_token):
        self.base_url = base_url.rstrip('/')
        self.email = email
        self.api_token = api_token
        auth_str = f"{email}:{api_token}"
        self.auth_b64 = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
        self.headers = {
            'Authorization': f'Basic {self.auth_b64}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def request(self, endpoint, method='GET', data=None):
        url = f"{self.base_url}{endpoint}"
        req_data = json.dumps(data).encode('utf-8') if data else None
        req = urllib.request.Request(url, data=req_data, headers=self.headers, method=method)
        try:
            with urllib.request.urlopen(req) as resp:
                content = resp.read().decode('utf-8')
                return json.loads(content) if content else {}
        except urllib.error.HTTPError as e:
            err_body = e.read().decode('utf-8')
            print(f"[HTTP {e.code}] Error requesting {url}: {err_body}")
            raise e

    def get_myself(self):
        return self.request('/rest/api/3/myself')

    def get_boards(self):
        return self.request('/rest/agile/1.0/board')

    def get_sprints(self, board_id=1):
        return self.request(f'/rest/agile/1.0/board/{board_id}/sprint')

    def search_issues(self, jql, max_results=50):
        # Jira Cloud API v3 search uses /rest/api/3/search/jql with POST
        return self.request('/rest/api/3/search/jql', method='POST', data={
            'jql': jql,
            'maxResults': max_results
        })

    def get_sprint_issues(self, sprint_id):
        return self.request(f'/rest/agile/1.0/sprint/{sprint_id}/issue')

    def get_board_issues(self, board_id=1):
        return self.request(f'/rest/agile/1.0/board/{board_id}/issue')

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_file = os.path.join(root_dir, '.env')
    env = load_env(env_file)

    base_url = env.get('JIRA_URL', 'https://nguyenminhquangnmqlamdong.atlassian.net')
    email = env.get('JIRA_EMAIL', 'cristand2825@gmail.com')
    token = env.get('JIRA_API_TOKEN', '')
    project_key = env.get('JIRA_PROJECT_KEY', 'SCRUM')

    if not token:
        print("Missing JIRA_API_TOKEN in .env!")
        return

    client = JiraClient(base_url, email, token)

    print("==================================================")
    print("🔍 KIỂM TRA KẾT NỐI JIRA CLOUD")
    print("==================================================")
    user = client.get_myself()
    print(f"✅ Người dùng xác thực : {user.get('displayName')} ({user.get('emailAddress')})")
    print(f"✅ Quyền hạn / TimeZone : {user.get('timeZone')} | Active: {user.get('active')}")

    print("\n--------------------------------------------------")
    print("📋 DANH SÁCH BOARDS TRÊN JIRA:")
    boards = client.get_boards().get('values', [])
    for b in boards:
        print(f" • Board ID [{b['id']}]: {b['name']} ({b['type']})")

    print("\n--------------------------------------------------")
    print("🏃 DANH SÁCH SPRINTS TRÊN BOARD 1 (SCRUM Board):")
    try:
        sprints = client.get_sprints(1).get('values', [])
        if sprints:
            for s in sprints:
                print(f" • Sprint ID [{s['id']}]: {s['name']} (State: {s['state']})")
        else:
            print(" (Chưa có Sprint nào hoặc đang ở trạng thái backlog)")
    except Exception as e:
        print(f" Không lấy được sprint: {e}")

    print("\n--------------------------------------------------")
    print(f"📌 DANH SÁCH ISSUES TRONG SPRINT ĐANG CHẠY (Sprint ID: 2 - SCRUM Sprint 0):")
    try:
        sprint_issues = client.get_sprint_issues(2).get('issues', [])
        print(f"Tổng số Issues trong Sprint 0: {len(sprint_issues)}\n")
        for idx, issue in enumerate(sprint_issues, 1):
            key = issue['key']
            fields = issue['fields']
            summary = fields.get('summary', 'No summary')
            status = fields.get('status', {}).get('name', 'N/A')
            issue_type = fields.get('issuetype', {}).get('name', 'Task')
            assignee = fields.get('assignee')
            assignee_str = assignee.get('displayName') if assignee else 'Chưa gán'
            print(f"{idx:02d}. [{key}] [{issue_type}] [{status}] {summary} (Assignee: {assignee_str})")
    except Exception as e:
        print(f" Lỗi truy xuất sprint issues: {e}")

    print("\n--------------------------------------------------")
    print(f"📌 TẤT CẢ ISSUES TRÊN BOARD (Board ID: 1):")
    try:
        board_issues = client.get_board_issues(1).get('issues', [])
        print(f"Tổng số Issues trên Board: {len(board_issues)}\n")
        for idx, issue in enumerate(board_issues, 1):
            key = issue['key']
            fields = issue['fields']
            summary = fields.get('summary', 'No summary')
            status = fields.get('status', {}).get('name', 'N/A')
            issue_type = fields.get('issuetype', {}).get('name', 'Task')
            assignee = fields.get('assignee')
            assignee_str = assignee.get('displayName') if assignee else 'Chưa gán'
            print(f"{idx:02d}. [{key}] [{issue_type}] [{status}] {summary} (Assignee: {assignee_str})")
    except Exception as e:
        print(f" Lỗi truy xuất board issues: {e}")

if __name__ == '__main__':
    main()
