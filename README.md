# Discord Channel Message Cloner

A powerful Discord bot that mirrors messages from a channel in one Discord server to a channel in another server in real time.

Perfect for synchronizing announcements, sharing updates across communities, creating backups, or managing content across multiple Discord servers.

## ✨ Features

* 🔄 Real-time message cloning
* 📝 Supports regular text messages
* 📎 Supports file attachments
* 🎨 Supports Discord embeds
* ⚡ Fast and lightweight
* 🔒 Permission validation and error handling
* 🌐 Cross-server channel synchronization

## 📋 Requirements

### Software

* Python **3.11+**
* A Discord Bot Token

### Python Dependencies

Install the required packages using:

```bash
pip install discord.py requests
```

Or:

```bash
python -m pip install discord.py requests
```

## 🔑 Required Permissions

### Source Server (Read From)

The bot must have:

* View Channel
* Read Message History

### Destination Server (Write To)

The bot must have:

* View Channel
* Send Messages
* Embed Links
* Attach Files

## 🚀 Setup

1. Install Python **3.11 or newer**.
2. Install the required dependencies:

```bash
pip install discord.py requests
```

3. Create a Discord application and bot through the Discord Developer Portal.
4. Invite the bot to both servers.
5. Grant the required permissions.
6. Configure the source and destination channel IDs.
7. Start the bot.

## 💡 Use Cases

* Server announcement mirroring
* Community network management
* Cross-server notifications
* Content backups and archives
* Multi-server content distribution

## ⚠️ Notes

The bot can only clone messages if it has access to both channels:

* Read access in the source server
* Read and write access in the destination server

Without the required permissions, message cloning will not function correctly.

---

**A simple and reliable Discord bot for cloning messages between channels across multiple servers.**
