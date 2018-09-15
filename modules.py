import re


class Module(object):
    def handle(self, server, line):
        raise NotImplementedError

class Users(Module):
    def __init__(self):
        self.users = set()

    def handle(self, server, line):
        m = re.search(r'There are \d+ of a max \d+ players online: (.*)', line)
        joined = re.search(r'(\w+) joined the game', line)
        left = re.search(r'(\w+) left the game', line)
        if joined:
            self.users.add(joined.group(1))
        if left:
            self.users.remove(left.group(1))
