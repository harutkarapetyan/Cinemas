import configparser

config = configparser.ConfigParser()
config.read("./core/config.ini")

SERVER_ADDRESS = config["DEFAULT"]["SERVER_ADDRESS"]
VERIFICATION_BASE_URL = f"{SERVER_ADDRESS}/api/auth/mail_verification"