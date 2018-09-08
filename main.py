import subprocess
import threading
import time
import re
from interface import interface


class MinecraftServer():
    def __init__(self, memory=1024, cwd='.', jar=None):
        self.modules = []

        self.command = ['java']
        self.command += ['-Xmx{}M'.format(memory)]
        self.command += ['-Xms{}M'.format(memory)]
        self.command += ['-jar', jar]
        self.command += ['nogui']

        self.cwd = cwd
        self.proc = None

        self.running = False
        self.ready = False

    def start(self):
        self.proc = subprocess.Popen(self.command, cwd=self.cwd,
                                     stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        self.read_thread = threading.Thread(target=self.handle_stdout)
        self.read_thread.start()
        self.running = True
    
    def stop(self):
        self.send_command('stop')

    def send_command(self, cmd):
        self.proc.stdin.write('{}\n'.format(cmd).encode())
        self.proc.stdin.flush()

    def handle_stdout(self):
        for line in iter(self.proc.stdout.readline, b''):
            line = line.strip().decode()
            if 'Done' in line:
                self.ready = True

            for module in self.modules:
                module.handle(self, line)

        self.proc.stdout.close()
        self.running = False

    def add_module(self, module):
        self.modules += [module]


class Users:
    def __init__(self):
        self.users = []

    def handle(self, server, line):
        m = re.search(r'There are \d+ of a max \d+ players online: (.*)', line)
        if m:
            self.users = m.group(1).split(', ')
            print('Users: ' + ' ,'.join(self.users))


if __name__ == '__main__':
    server = MinecraftServer(cwd='server/', jar='server.jar')
    server.start()

    user_module = Users()
    server.add_module(interface)
    server.add_module(user_module)

    try:
        while True:
            interface.update()
            if interface.cmds:
                cmd = interface.cmds.pop(0)
                server.send_command(cmd)
                if cmd in ('stop', '/stop'):
                    interface.stop()
                    break
    except KeyboardInterrupt:
        server.stop()
        interface.stop()

    while server.running:
        time.sleep(1)
