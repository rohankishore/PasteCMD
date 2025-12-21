import cmd

import pyperclip
import requests
import os
import platform

if platform.system() == "Linux":
    config_dir = os.path.join(os.path.expanduser("~"), ".config", "PasteCMD")
elif platform.system() == "Windows":
    localappdata = os.environ.get("LOCALAPPDATA")
    config_dir = os.path.join(localappdata, "PasteCMD")
elif platform.system() == "Darwin":
    applicationsupport = os.path.join(os.path.expanduser("~"), "Library", "Application Support")
    config_dir = os.path.join(applicationsupport, "PasteCMD")
else:
    config_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(config_dir, exist_ok=True)
keytxt_path = os.path.join(config_dir, "api_key.txt")
try:
    with open(keytxt_path, "r") as api_file:
        API_KEY = api_file.read().strip()
except FileNotFoundError:
    print("ERROR: Failed to get API key. Please get an API key and then run the add_api_key command with the key as an argument in this program's interactive shell.")
    API_KEY = None

art = r"""
 ____           _        ____ __  __ ____  
|  _ \ __ _ ___| |_ ___ / ___|  \/  |  _ \ 
| |_) / _` / __| __/ _ \ |   | |\/| | | | |
|  __/ (_| \__ \ ||  __/ |___| |  | | |_| |
|_|   \__,_|___/\__\___|\____|_|  |_|____/ 
                                           
"""


class YTWrap(cmd.Cmd):
    prompt = ">> "
    intro = "Welcome to PasteCMD. " + art + "Type 'help' to view all commands" + "\n"

    def __init__(self):
        super().__init__()

    def do_add_api_key(self, apiKey):
        global API_KEY
        with open(keytxt_path, "w") as api_file:
            api_file.write(apiKey.strip())
        API_KEY = apiKey.strip()

    def do_text(self, text_pb):
        try:
            if not API_KEY:
                print("ERROR: No API key found. Please add an API key using the add_api_key command.")
                return
            if text_pb != "":
                data = {"api_dev_key": API_KEY, "api_option": "paste", "api_paste_code": text_pb}
                response = requests.post("https://pastebin.com/api/api_post.php", data=data).text
                self.respond(response)
            else:
                print("WARNING: Cowardly refusing to upload blank text") # that would be spam anyways

        except Exception as e:
            print(f"An error occurred: {e}")

    def do_clipboard(self, line):
        clipboard_content = pyperclip.paste()
        print("Uploading clipboard content:" + '\n' + clipboard_content)
        self.do_text(clipboard_content)

    def do_file(self, file_pb):
        try:
            if not API_KEY:
                print("ERROR: No API key found. Please add an API key using the add_api_key command.")
                return
            with open(file_pb, "r") as file:
                content = file.read()
            if content != "":
                data = {"api_dev_key": API_KEY, "api_option": "paste", "api_paste_code": content}
                response = requests.post("https://pastebin.com/api/api_post.php", data=data).text
                self.respond(response)
            else:
                print("WARNING: Cowardly refusing to upload a blank file")

        except Exception as e:
            print(f"An error occurred: {e}")

    def format_time(self, seconds):
        """Format time in seconds to HH:MM:SS format."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def respond(self, response):
        # print(response)
        if response.startswith("Bad API request"):
            print(f"ERROR: Pastebin upload NOT SUCCESSFUL: {response}")
        else:
            pyperclip.copy(response)
            print("Your Pastebin link has been copied to the clipboard!")

    def do_quit(self, line):
        """Exit the CLI."""
        return True

    def do_exit(self, line):
        """Same purpose as quit function"""
        return True

    def do_EOF(self, line):
        """Quit with EOF (i,e Ctrl+D)"""
        return True

    def postcmd(self, stop, line):
        print()  # Add an empty line for better readability
        return stop

if __name__ == '__main__':
    try:
        YTWrap().cmdloop()
    except KeyboardInterrupt:
        print("Restarting shell...")
        YTWrap().cmdloop()
