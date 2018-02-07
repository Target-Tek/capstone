import curses
from curses import wrapper

def main(stdscr):
	stdscr.clear()
	print("Running some program")
	while True:
		# Store the key value in the variable 'direction'
		direction = stdscr.getch()
		# clear the terminal
		stdscr.clear()
		if direction == ord('6'):
			stdscr.addstr("I want to move right")
		elif direction == ord('8'):
			stdscr.addstr("I want to move up")
		elif direction == ord('4'):
			stdscr.addstr("I want to move left")
		elif direction == ord('2'):
			stdscr.addstr("I want to move down")

wrapper(main)

