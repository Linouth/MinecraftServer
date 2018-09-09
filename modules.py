import re


class Module(object):
    def handle(self, server, line):
        raise NotImplementedError

class Users(Module):
    def __init__(self):
        self.users = []

    def handle(self, server, line):
        m = re.search(r'There are \d+ of a max \d+ players online: (.*)', line)
        if m:
            self.users = m.group(1).split(', ')
            print('Users: ' + ' ,'.join(self.users))
