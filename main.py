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

if __name__ == "__main__":
    main()
