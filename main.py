import time
import requests

BASE = "https://discord.com/api/v10"


def get_headers(token: str) -> dict:
    return {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json",
    }


def api_get(path: str, headers: dict):
    while True:
        r = requests.get(BASE + path, headers=headers)
        if r.status_code == 429:
            wait = r.json().get("retry_after", 1)
            print(f"  [rate limit] waiting {wait:.1f}s...")
            time.sleep(wait)
            continue
        if not r.ok:
            raise Exception(f"HTTP {r.status_code}: {r.text[:200]}")
        return r.json()


def api_post(path: str, payload: dict, headers: dict):
    while True:
        r = requests.post(BASE + path, json=payload, headers=headers)
        if r.status_code == 429:
            wait = r.json().get("retry_after", 1)
            print(f"  [rate limit] waiting {wait:.1f}s...")
            time.sleep(wait)
            continue
        if not r.ok:
            raise Exception(f"HTTP {r.status_code}: {r.text[:200]}")
        return r.json()


def pick_from_list(items: list, name_key: str, label: str) -> dict:
    print(f"\n  Available {label}:")
    for i, item in enumerate(items):
        print(f"    [{i+1}] {item[name_key]}  (id: {item['id']})")
    while True:
        choice = input(f"  Pick {label} number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(items):
            return items[int(choice) - 1]
        print("  Invalid choice, try again.")


def main():
    print("=" * 50)
    print("  Discord Channel Copier — last 30 messages")
    print("=" * 50)

    token = input("\nPaste your bot token: ").strip()
    if token.lower().startswith("bot "):
        token = token[4:].strip()

    headers = get_headers(token)

    print("\nVerifying token...")
    try:
        me = api_get("/users/@me", headers)
        print(f"  Logged in as: {me['username']} (bot: {me.get('bot', False)})")
    except Exception as e:
        print(f"  ERROR: {e}")
        print("  → Make sure you copied the bot token correctly.")
        return
    
    print("\nFetching servers...")
    try:
        guilds = api_get("/users/@me/guilds", headers)
    except Exception as e:
        print(f"  ERROR fetching servers: {e}")
        return

    if not guilds:
        print("  No servers found. Make sure the bot has been invited to your servers.")
        return

    print("\n--- SOURCE ---")
    src_guild = pick_from_list(guilds, "name", "source server")

    print(f"\n  Fetching channels for '{src_guild['name']}'...")
    try:
        all_channels = api_get(f"/guilds/{src_guild['id']}/channels", headers)
    except Exception as e:
        print(f"  ERROR: {e}")
        return

    text_channels = [c for c in all_channels if c["type"] in (0, 5)]
    text_channels.sort(key=lambda c: c.get("position", 0))

    if not text_channels:
        print("  No text channels found. Check bot permissions (View Channels).")
        return

    src_channel = pick_from_list(text_channels, "name", "source channel")

    print("\n--- DESTINATION ---")
    dst_guild = pick_from_list(guilds, "name", "destination server")

    print(f"\n  Fetching channels for '{dst_guild['name']}'...")
    try:
        all_channels2 = api_get(f"/guilds/{dst_guild['id']}/channels", headers)
    except Exception as e:
        print(f"  ERROR: {e}")
        return

    text_channels2 = [c for c in all_channels2 if c["type"] in (0, 5)]
    text_channels2.sort(key=lambda c: c.get("position", 0))

    if not text_channels2:
        print("  No text channels found. Check bot permissions.")
        return

    dst_channel = pick_from_list(text_channels2, "name", "destination channel")

    if src_channel["id"] == dst_channel["id"]:
        print("\n  ERROR: Source and destination are the same channel!")
        return

    print(f"\nFetching last 30 messages from #{src_channel['name']}...")
    try:
        messages = api_get(f"/channels/{src_channel['id']}/messages?limit=30", headers)
    except Exception as e:
        print(f"  ERROR: {e}")
        print("  → Make sure the bot has 'Read Message History' in that channel.")
        return

    if not messages:
        print("  No messages found in that channel.")
        return

    messages = list(reversed(messages))
    print(f"  Got {len(messages)} message(s).")

    print(f"\nCopying to #{dst_channel['name']}...")
    sent = skipped = failed = 0

    for i, msg in enumerate(messages):
        author = msg.get("author", {})
        name = author.get("global_name") or author.get("username") or "Unknown"

        parts = []
        if msg.get("content"):
            parts.append(msg["content"])
        for att in msg.get("attachments", []):
            parts.append(att["url"])
        if not parts and msg.get("sticker_items"):
            parts.append(f"[sticker: {msg['sticker_items'][0]['name']}]")

        if not parts:
            skipped += 1
            print(f"  [{i+1}/{len(messages)}] Skipped empty message from {name}")
            continue

        content = f"**{name}**: " + "\n".join(parts)
        content = content[:2000]

        try:
            api_post(f"/channels/{dst_channel['id']}/messages", {"content": content}, headers)
            sent += 1
            print(f"  [{i+1}/{len(messages)}] ✓ {name}: {parts[0][:60]}{'...' if len(parts[0]) > 60 else ''}")
        except Exception as e:
            failed += 1
            print(f"  [{i+1}/{len(messages)}] ✗ Failed ({e})")

        if i < len(messages) - 1:
            time.sleep(1.2)  # stay under Discord's rate limit

    print(f"\n{'='*50}")
    print(f"  Done! {sent} sent  |  {skipped} skipped  |  {failed} failed")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
