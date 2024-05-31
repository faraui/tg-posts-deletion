import config
import pyrogram
from tqdm import tqdm
import colorama
import time
import traceback

app = pyrogram.Client(
    "main",
    api_id=config.api_id, api_hash=config.api_hash
)
bot = pyrogram.Client(
   "main_bot",
   api_id=config.api_id, api_hash=config.api_hash,
   bot_token=config.bot_token
)

class Shreder:
    def __init__(self, target):
        self.target = target

    def index(self):
        print(colorama.Fore.BLUE + colorama.Style.BRIGHT + 'Indexing...' + colorama.Style.RESET_ALL)
        self.posts = []
        for post in tqdm(app.get_chat_history(self.target), total=app.get_chat_history_count(self.target), unit='msg'):
            self.posts.append(post)
        print(colorama.Fore.BLUE + colorama.Style.BRIGHT + 'Indexing complete' + colorama.Style.RESET_ALL)
        print()

    def shred(self):
        index = 0
        print(colorama.Fore.MAGENTA + colorama.Style.BRIGHT + 'Deletion...' + colorama.Style.RESET_ALL)
        for post in self.posts:
            #msg = post.text or post.caption
            #msg = f'"{msg[:20]}"' if msg else ''
            print(f'deleting post {post.id}'.ljust(44), end='  ')
            try:
                app.delete_messages(self.target, post.id)
            except Exception as e:
                print(colorama.Fore.RED + colorama.Style.BRIGHT + 'FAILED' + colorama.Style.RESET_ALL)
                print(colorama.Fore.YELLOW, e, colorama.Style.RESET_ALL)
                if not request_confirmation(SKIP_MSG):
                    self.posts = self.posts[index:]
                    return False
            index += 1
            print(colorama.Fore.GREEN + colorama.Style.BRIGHT + 'DONE' + colorama.Style.RESET_ALL)
            time.sleep(1)
        print(colorama.Fore.MAGENTA + colorama.Style.BRIGHT + 'Deletion complete! THEY ARE IN A DAZE!' + colorama.Style.RESET_ALL)
        return True

def request_confirmation(msg, yes='y'):
    return True if (input(msg).lower() == yes) else False

SKIP_MSG = 'An error occured during deletion. Skip the error post and continue? [y/N] '
CONFIRM_MSG = '!POST DELETION CAN NOT BE UNDONE! Type `confirm` if you want to continue > '
AFTER_ERROR_MSG = 'Try again? [y/N] '
if __name__ == '__main__':
    shreder = Shreder(config.target)
    with app:
        shreder.index()
        while True:
            if request_confirmation(CONFIRM_MSG, 'confirm'):
                if shreder.shred(): break
                elif not request_confirmation(AFTER_ERROR_MSG): break
                print(colorama.Fore.YELLOW, e, colorama.Style.RESET_ALL)
