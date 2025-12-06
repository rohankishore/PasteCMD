import cmd

import pyperclip
import requests
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
keytxt_path = os.path.join(script_dir, "api_key.txt")
try:
    with open(keytxt_path, "r") as api_file:
        API_KEY = api_file.read().strip()
except FileNotFoundError:
    print("ERROR: Failed to get API key. Please get an API key and then run the add_api_key command with the key as an argument in this program's interactive shell.")

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
            if text_pb != "":
                data = {"api_dev_key": API_KEY, "api_option": "paste", "api_paste_code": text_pb}
                response = requests.post("https://pastebin.com/api/api_post.php", data=data).text
                self.respond(response)
            else:
                print("WARNING: Cowardly refusing to upload blank text") # that would be spam anyways

        except Exception as e:
            print(f"An error occurred: {e}")

    def do_file(self, file_pb):
        try:
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
        print(response)
        if response.startswith("Bad API request"):
            print("ERROR: Pastebin upload NOT SUCCESSFUL")
        else:
            pyperclip.copy(response)
            print("Your Pastebin link has been copied to the clipboard!")

    def do_quit(self, line):
        """Exit the CLI."""
        return True

    def do_exit(self, line):
        """Same purpose as quit function"""
        return True

    def postcmd(self, stop, line):
        print()  # Add an empty line for better readability
        return stop


if __name__ == '__main__':
    YTWrap().cmdloop()
