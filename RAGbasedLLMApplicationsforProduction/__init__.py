import os
from configparser import SafeConfigParser

config = SafeConfigParser()
config.read('config.ini')

RAY_ADDRESS = os.getenv("RAY_ADDRESS")

if not RAY_ADDRESS:
    print(f"RAY_ADDRESS not set, assuming local cluster exists...")
    os.environ["RAY_ADDRESS"] = config.get("ray",'RAY_ADDRESS')