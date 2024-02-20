import os
import string
import secrets

def generate_secret_key(length=24):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    secret_key = ''.join(secrets.choice(alphabet) for i in range(length))
    return secret_key

def generate_key():
    key = generate_secret_key()
    with open('config.py', 'r') as f:
        lines = f.readlines()

    with open('config.py', 'w') as f:
        for line in lines:
            if line.strip() == "class Config:":
                f.write(line)
                f.write(f"    SECRET_KEY = '{key}'\n")
            else:
                f.write(line)

if __name__ == "__main__":
    generate_key()
    print("Secret key has been generated and added to config.py.")
