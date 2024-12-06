import os, sys, subprocess, shutil

def check_or_install(module):
    try: __import__(module)
    except ImportError: subprocess.check_call([sys.executable, "-m", "pip", "install", module])

def check_firefox():
    if not shutil.which("firefox") and not os.path.exists(r"C:\Program Files\Mozilla Firefox\firefox.exe"):
        sys.exit("Firefox must be installed to run this")

def check_and_update_webhook(file_path, line_num=125):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        if line_num <= len(lines) and 'webhook_url' in lines[line_num - 1]:
            line_content = lines[line_num - 1]
            if "https://" in line_content.split("'")[1]:
                print("Webhook is already set")
                return

        webhook_url = input("Webhook: ").strip()
        if not webhook_url.startswith("https://"):
            sys.exit("Invalid webhook")

        lines[line_num - 1] = f"                webhook_url = '{webhook_url}'\n"
        with open(file_path, 'w') as file:
            file.writelines(lines)

        print("Webhook successfully added to main.py")
    except Exception as e:
        sys.exit(f"Couldnt check webhook: {e}")

if __name__ == "__main__":
    for mod in ["requests", "selenium", "colorama"]: check_or_install(mod)
    check_firefox()
    check_and_update_webhook("main.py")
    try: subprocess.run([sys.executable, "main.py"], check=True)
    except subprocess.CalledProcessError as e: sys.exit(f"Error running main.py: {e}")