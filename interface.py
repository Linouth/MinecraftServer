import curses
import time

QUIT = ['q', 'quit', 'stop', 'exit']

class Interface():
    def __init__(self, stdscr):
        curses.noecho()
        curses.cbreak()

        self.stdscr = stdscr
        y, x = stdscr.getmaxyx()

        self.output_win = stdscr.subwin(y-2, x, 0, 0)
        self.output_win.scrollok(True)
        self.output_line_index = 0

        self.input_win = stdscr.subwin(1, x, y-1, 0)
        self.input_win.nodelay(True)
        self.input_win.attron(curses.A_STANDOUT)
        self.input_win.bkgdset(' ', curses.A_STANDOUT)
        self.input_win.keypad(True)
        self.input_win.leaveok(True)

        self.win_clear(self.input_win, '>>> ', refresh=True)

        self.max_output_dim = self.output_win.getmaxyx()
        self.cmd = ''
        self.cmds = []

    def stop(self):
        curses.nocbreak()
        self.input_win.keypad(False)
        curses.echo()
        curses.endwin()

    def update(self):
        c = self.stdscr.getch()

        if c != -1:
            if c == curses.KEY_ENTER or c == 10 or c == 13:
                self.cmds.append(self.cmd)
                self.cmd = ''
            elif c == curses.KEY_BACKSPACE or c == ord('\b') or c == 127:
                self.cmd = self.cmd[:-1]
            else:
                self.cmd += chr(c)

            self.win_clear(self.input_win, '>>> ')
            self.input_win.addnstr(0, 4, self.cmd, self.max_output_dim[1]-5)
            self.input_win.refresh()

    def print(self, line, refresh=True):
        if self.output_line_index == self.max_output_dim[0]:
            self.output_win.scroll()
            self.output_line_index -= 1
        self.output_win.addnstr(self.output_line_index, 0, line, self.max_output_dim[1]-1)
        if refresh:
            self.output_win.refresh()
        self.output_line_index += 1

    def handle(self, server, line):
        self.print(line.strip())

    @staticmethod
    def win_clear(win, initial, refresh=False):
        win.clear()
        if initial:
            win.addstr(initial)
        if refresh:
            win.refresh()


interface = Interface(curses.initscr())
