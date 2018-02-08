import curses
import time
from curses import wrapper

def main(stdscr):
	stdscr.clear()
	stdscr.nodelay(True)
	print("Running some program")
	while True:
		# Store the key value in the variable 'direction'
		direction = stdscr.getch()
		# clear the terminal
		stdscr.clear()
		time.sleep(.05)
		if direction == -1:
			stdscr.addstr("No key press")
		elif direction == ord('6'):
			stdscr.addstr("I want to move right")
			
		elif direction == ord('8'):
			stdscr.addstr("I want to move up")
			
		elif direction == ord('4'):
			stdscr.addstr("I want to move left")
			
		elif direction == ord('2'):
			stdscr.addstr("I want to move down")
		
		else:
			stdscr.addstr("I dont'know that key")
			direction = '0'

		# clear the terminal
		#stdscr.clear()
		#stdscr.addstr("I'm working")

wrapper(main)

