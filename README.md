# ChatGPT Telegram Bot

This project is ChatGPT as a Telegram Bot to offer an alternative interface. It uses the OpenAI API, which is much cheaper than the official ChatGPT web interface.

This is a hard fork of [karfly/chatgpt_telegram_bot](https://github.com/karfly/chatgpt_telegram_bot) and is not intended to make me money.

## Features

- Supports ChatGPT 4
- Low latency replies (it usually takes about 3-5 seconds)
- No request limits
- Code highlighting
- Special chat modes: 👩🏼‍🎓 Assistant, 👩🏼‍💻 Code Assistant, 📝 Text Improver and 🎬 Movie Expert. You can easily create your own chat modes by editing `config/chat_modes.yml`
- Support for [ChatGPT API](https://platform.openai.com/docs/guides/chat/introduction)
- List of allowed Telegram users

## Bot commands

- `/retry` – Regenerate last bot answer
- `/new` – Start new dialog
- `/mode` – Select chat mode
- `/help` – Show help

## Setup

1. Get your [OpenAI API](https://openai.com/api/) key
1. Get your Telegram bot token from [@BotFather](https://t.me/BotFather)
1. Copy the example configuration

   ```console
   cp config/config.example.yml config/config.yml
   ```

1. Edit `config/config.yml` and set your tokens and so on there
1. Build the Docker image:

   ```console
   docker-compose build
   ```

1. Run the bot:

   ```console
   docker-compose up -d
   ```

This starts the bot in the background. To see logs, run `docker-compose logs`.

## Comparison to the original project

The [original project](https://github.com/karfly/chatgpt_telegram_bot) has some insecure defaults and other inconveniences and it doesn't seem to accept PRs (at the time of writing). This project is more opinionated and adjusted to fit my personal needs better. My use case is different from the original, I want to use this myself and share with my friends. I don't want use it to make money.

Differences from the original project as of writing, and reasoning why.

### Security

- Don't allow everyone on Telegram to use the bot
  - Allow specific usernames or user IDs in `allowed_telegram_usernames`. I want to use it myself, and share with friends
- Don't store chat messages longer than needed
  - By not storing them in the database longer than `new_dialog_timeout`, there is less for an attacker to steal
- Don't store user information longer than needed
  - By not storing user IDs (and other data) in the database longer than `new_dialog_timeout`, there is less for an attacker to steal. I don't need to track user information because I don't use it commercially
- Don't store username, first name, and last name
  - It's not used for anything. The less data we have, the less someone can steal
- Don't include mongo-express at all
  - mongo-express is an administration interface for MongoDb. Previously, it was exposed to the network with default username `username` and password `password`, which is bad from a security point of view
- Don't expose MongoDb to the network or even localhost
  - Exposing MongoDb (especially with no authentication) to the network is a security risk
- Use multi-stage builds to get a minimal final Docker image
  - With fewer things that can be abused by an attacker the service is more secure. Uses [distroless](https://github.com/GoogleContainerTools/distroless)
- Set the filesystem for the bot container to read only
  - Improves security because an attacker can't write to the filesystem
- Don't run as root
  - Improves security, mainly for the host running the container

### Added features

- Make it configurable which ChatGPT model to use (for example `gpt-3.5-turbo`)
  - Via `chatgpt_model` in `config/config.yml`, to make it future proof for new models
- Mount `config/config.yml` so we don't need to re-build the Docker image when updating the configuration
  - Use `docker-compose restart chatgpt_telegram_bot` to reload the configuration

### Removed features

Every line of code is a potential bug!

- Don't use `config.env`
  - Unnecessary code complexity for my use-case
- Remove voice support
  - I have no personal use for this, which means it's unnecessary code complexity
- Remove check balance function
  - It's not accurate because it doesn't check the billing via OpenAI but rather an internal db. I don't need to track usage of specific users since I don't intend to charge them
- Remove option to use non-chat API
  - I see no personal use-case for using the non-chat completion API for a chat bot
