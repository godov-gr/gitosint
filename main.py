import requests
import re
import json

def get_user_info(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "Username": data.get("login"),
            "Name": data.get("name"),
            "Bio": data.get("bio"),
            "Location": data.get("location"),
            "Email": data.get("email"),
            "Public Repos": data.get("public_repos"),
            "Followers": data.get("followers"),
            "Following": data.get("following"),
            "Created At": data.get("created_at")
        }
    else:
        print(f"[!] Ошибка: пользователь {username} не найден или превышен лимит API.")
        return None

def get_emails_from_events(username):
    url = f"https://api.github.com/users/{username}/events/public"
    response = requests.get(url)
    emails = set()
    if response.status_code == 200:
        events = response.json()
        for event in events:
            if "payload" in event and "commits" in event["payload"]:
                for commit in event["payload"]["commits"]:
                    email = commit["author"].get("email")
                    if email and re.match(r"[^@]+@[^@]+\.[^@]+", email):
                        emails.add(email)
    return emails

def get_followers(username):
    url = f"https://api.github.com/users/{username}/followers"
    response = requests.get(url)
    if response.status_code == 200:
        return [f"[{user['login']}](https://github.com/{user['login']})" for user in response.json()]
    return []

def get_following(username):
    url = f"https://api.github.com/users/{username}/following"
    response = requests.get(url)
    if response.status_code == 200:
        return [f"[{user['login']}](https://github.com/{user['login']})" for user in response.json()]
    return []

def get_starred_repos(username):
    url = f"https://api.github.com/users/{username}/starred"
    response = requests.get(url)
    if response.status_code == 200:
        repos = response.json()
        sorted_repos = sorted(repos, key=lambda x: x["stargazers_count"], reverse=True)
        return [f"{repo['full_name']} ({repo['stargazers_count']} stars)" for repo in sorted_repos]
    return []

def print_section(title, content, no_data_msg="[Нет данных]"):
    print("\n" + "=" * 50)
    print(f"{title}")
    print("=" * 50)
    print(content if content else no_data_msg)

def save_report(username, data):
    filename = f"{username}_report.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"[+] Отчёт сохранён в {filename}")

def main():
    usernames = input("Введите один или несколько GitHub-никнеймов через запятую: ")
    usernames = [u.strip() for u in usernames.split(",") if u.strip()]
    
    for username in usernames:
        report_data = {}
        
        print_section(f"Информация о пользователе {username}", "")
        user_info = get_user_info(username)
        if user_info:
            for key, value in user_info.items():
                print(f"{key}: {value}")
            report_data["User Info"] = user_info
        
        print_section(f"Email-адреса из событий {username}", "\n".join(get_emails_from_events(username)), "[-] Email-адреса не найдены.")
        report_data["Emails"] = list(get_emails_from_events(username))
        
        followers = get_followers(username)
        print_section(f"Подписчики {username}", "\n".join(followers), "[-] Подписчики отсутствуют.")
        report_data["Followers"] = followers
        
        following = get_following(username)
        print_section(f"Подписки {username}", "\n".join(following), "[-] Подписок нет.")
        report_data["Following"] = following
        
        starred_repos = get_starred_repos(username)
        print_section(f"Избранные репозитории {username}", "\n".join(starred_repos), "[-] Нет избранных репозиториев.")
        report_data["Starred Repos"] = starred_repos
        
        download = input("\nDownload report (y/n)? ").strip().lower()
        if download == "y":
            save_report(username, report_data)
        else:
            print("[-] Отчёт не был сохранён.")

if __name__ == "__main__":
    main()
