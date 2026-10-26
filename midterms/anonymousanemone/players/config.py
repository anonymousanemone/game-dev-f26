"""Load only known local settings; never execute shell content or print secrets."""
import os

NAMES = {'OPENAI_API_KEY', 'CROC_MODEL', 'CROC_MAX_COST_USD', 'CROC_INPUT_PRICE',
         'CROC_OUTPUT_PRICE', 'CROC_PRICE_DATE', 'CROC_PRICE_SOURCE'}


def load_env(path):
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        name, separator, value = line.partition('=')
        name, value = name.strip(), value.strip()
        if separator and name in NAMES:
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            if value and not os.environ.get(name):
                os.environ[name] = value
