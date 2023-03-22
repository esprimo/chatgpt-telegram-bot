import yaml
from pathlib import Path

config_dir = Path(__file__).parent.parent.resolve() / "config"

# load yaml config
with open(config_dir / "config.yml", 'r') as f:
    config_yaml = yaml.safe_load(f)

# telegram config
telegram_token = config_yaml.get("telegram_token")
telegram_allowed_users = config_yaml.get('telegram_allowed_users', [])

mongodb_uri = "mongodb://mongo:27017"

# gpt config
openai_api_key = config_yaml.get("openai_api_key")
chatgpt_model = config_yaml.get("chatgpt_model", "gpt-3.5-turbo")
new_dialog_timeout = int(config_yaml.get("new_dialog_timeout", 600))

# chat_modes
with open(config_dir / "chat_modes.yml", 'r') as f:
    chat_modes = yaml.safe_load(f)
