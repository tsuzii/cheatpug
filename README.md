# 🐾 CheatPug Bot

A Telegram bot with DeepSeek AI support. Users can run the bot locally via Docker in just a few commands.

---

## 1. Clone the repository

**Windows (PowerShell / CMD):**

```powershell
git clone https://github.com/YOUR_USERNAME/cheatpug.git
cd cheatpug
```

**macOS / Linux (Terminal):**

```bash
git clone https://github.com/YOUR_USERNAME/cheatpug.git
cd cheatpug
```

---

## 2. Create a `.env` file

In the root of the project, create a `.env` file with the following content:

```env
CHANNEL_USERNAME=cheat_pug
URL_DEEPSEEK=https://api.deepseek.com
DEEPSEEK_TOKEN=YOUR_DEEPSEEK_TOKEN
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_TOKEN
```

> ⚠️ Important: **Do not use quotes** around the values.
> Tokens can be obtained from [BotFather](https://t.me/botfather) (Telegram) and DeepSeek API.

**Windows:**

```powershell
notepad .env
```

Paste the content above and save the file.

**macOS / Linux:**

```bash
nano .env
```

Paste the content above, then press `Ctrl+O`, `Enter`, `Ctrl+X` to save and exit.

---

## 3. Build the Docker image

**Windows / macOS / Linux:**

```bash
docker build --no-cache -t cheatpug-bot .
```

* `--no-cache` ensures a fresh build.
* `cheatpug-bot` is the name of the local Docker image.

---

## 4. Run the bot

**Windows / macOS / Linux:**

```bash
docker run --env-file .env cheatpug-bot
```

The bot will automatically connect to Telegram and DeepSeek.

---

## 5. Verification

* If everything is correct, the bot should start without errors.
* The error `Token is invalid!` usually appears if the token is incorrect or the `.env` file contains quotes or extra spaces.

**Check inside the container (optional):**

```bash
docker run --env-file .env -it cheatpug-bot /bin/sh
echo $TELEGRAM_BOT_TOKEN
```

Make sure the token is displayed **without quotes**.

---

## 6. Updating the bot

**Windows / macOS / Linux:**

```bash
git pull
docker build --no-cache -t cheatpug-bot .
docker run --env-file .env cheatpug-bot
```

