import requests
import re

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
        return [user["login"] for user in response.json()]
    return []

def get_following(username):
    url = f"https://api.github.com/users/{username}/following"
    response = requests.get(url)
    if response.status_code == 200:
        return [user["login"] for user in response.json()]
    return []

def get_starred_repos(username):
    url = f"https://api.github.com/users/{username}/starred"
    response = requests.get(url)
    if response.status_code == 200:
        repos = response.json()
        sorted_repos = sorted(repos, key=lambda x: x["stargazers_count"], reverse=True)
        return [f"{repo['full_name']} ({repo['stargazers_count']} stars)" for repo in sorted_repos]
    return []

def main():
    usernames = input("Введите один или несколько GitHub-никнеймов через запятую: ")
    usernames = [u.strip() for u in usernames.split(",") if u.strip()]
    
    for username in usernames:
        print(f"\n[+] Получаем информацию о пользователе {username}...")
        user_info = get_user_info(username)
        if user_info:
            for key, value in user_info.items():
                print(f"{key}: {value}")
        
        print(f"\n[+] Ищем email-адреса в публичных событиях для {username}...")
        emails = get_emails_from_events(username)
        if emails:
            for email in emails:
                print(f"[+] Найден email: {email}")
        else:
            print("[-] Email-адреса не найдены.")
        
        print(f"\n[+] Анализ подписчиков {username}...")
        followers = get_followers(username)
        print(f"Подписчики ({len(followers)}): {', '.join(followers) if followers else 'Нет данных'}")
        
        print(f"\n[+] Анализ подписок {username}...")
        following = get_following(username)
        print(f"Подписки ({len(following)}): {', '.join(following) if following else 'Нет данных'}")
        
        print(f"\n[+] Анализ избранных репозиториев {username}...")
        starred_repos = get_starred_repos(username)
        print(f"Избранные репозитории ({len(starred_repos)}):\n" + "\n".join(starred_repos) if starred_repos else "Нет данных")

if __name__ == "__main__":
    main()