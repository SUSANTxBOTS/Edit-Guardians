# 🛡️ Edit Guardian Bot

A Telegram bot that automatically deletes edited messages in groups to maintain transparency in conversations.

## ✨ Features

- 🔹 **Message Guardian**: Automatically deletes edited messages in groups
- 🔹 **Broadcast System**: Admin can broadcast messages to all users & groups
- 🔹 **Database Storage**: Stores user and group information in MongoDB
- 🔹 **Clean Interface**: Simple and user-friendly interface

## 🚀 Quick Deploy

### Deploy on Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://dashboard.heroku.com/new?template=https://github.com/SUSANTxBOTS/Edit-Guardians)

### Deploy on VPS

1. **Clone the repository:**
```bash
git clone https://github.com/NoxxOP/Edit-Guardians
cd Edit-Guardians
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Create .env file:**
```bash
nano .env
```

4. **Add your credentials:**
```env
BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_admin_id
MONGO_URL=your_mongodb_connection_string
CHANNEL_URL=https://t.me/your_channel
SUPPORT_GROUP_URL=https://t.me/your_support_group
```

5. **Run the bot:**
```bash
python main.py
```

### Deploy with Docker

1. **Build Docker image:**
```bash
docker build -t edit-guardian-bot .
```

2. **Run container:**
```bash
docker run -d --name edit-guardian --env-file .env edit-guardian-bot
```

### Deploy with PM2 (Process Manager)

1. **Install PM2:**
```bash
npm install -g pm2
```

2. **Start bot with PM2:**
```bash
pm2 start main.py --name "edit-guardian-bot" --interpreter python3
```

3. **Save PM2 configuration:**
```bash
pm2 save
pm2 startup
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description |
|----------|-------------|
| `BOT_TOKEN` | Your Telegram bot token from @BotFather |
| `ADMIN_ID` | Your Telegram user ID (admin privileges) |
| `MONGO_URL` | MongoDB connection string |
| `CHANNEL_URL` | Your channel link for bot promotion |
| `SUPPORT_GROUP_URL` | Your support group link |

### Getting Bot Token

1. Message @BotFather on Telegram
2. Send `/newbot`
3. Choose a name for your bot
4. Choose a username ending with "bot"
5. Copy the token

### Getting Your User ID

1. Message @userinfobot on Telegram
2. It will send your user ID

### MongoDB Setup

1. Create account on [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a new cluster
3. Get connection string
4. Replace `<username>` and `<password>` with your credentials

## 🛠️ Usage

### Bot Commands

- `/start` - Welcome message and bot information
- `/broadcast <message>` - Broadcast message to all users & groups (Admin only)

### Bot Features

1. **Add to Group**: Add the bot to your group
2. **Give Permissions**: Grant "Delete Messages" permission
3. **Automatic Protection**: Bot will delete any edited messages

## 📋 Requirements

- Python 3.11+
- MongoDB database
- Telegram Bot Token
- VPS or Heroku account

## 🔧 Installation

### Local Development

```bash
# Clone repository
git clone https://github.com/NoxxOP/Edit-Guardians
cd Edit-Guardians

# Install dependencies
pip install -r requirements.txt

# Create .env file with your credentials
cp .env.example .env

# Run the bot
python main.py
```

## 📁 File Structure

```
Edit-Guardians/
├── main.py              # Main bot code
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── heroku.yml          # Heroku deployment config
├── .env.example        # Environment variables example
└── README.md           # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

- **Channel**: [Join Channel](https://t.me/ShrutiBots)
- **Support Group**: [Get Help](https://t.me/ShrutiBotSupport)
- **Issues**: [Report Bug](https://github.com/NoxxOP/Edit-Guardians/issues)

## 📄 License

This project is licensed under the GNU License - see the [LICENSE](LICENSE) file for details.

## ⭐ Star History

If you find this project useful, please consider giving it a star!

---

Made with ❤️ by [NoxxOP](https://github.com/NoxxOP)
