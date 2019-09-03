README

Group Members: Jesse Rathy, Agis Daniels
Student Number: 11166083
NSID: jrr867

1. The language used for our implementation was Python; it was written in Pycharm, so that may possibly be the best way to open it to run it if possible.

2. Package Dependencies: Other then the packages in the zip, and Math (which should be default in python 3, to my knowledge), there were no third party packages dependencies. It was written in Python 3.4-3.5, so no assumptions can be made for it working with versions earlier than that.

unzip the file, and open the resulting folder in pycharm; it should come with a set of 4 files; ChessVar, GameTreeSearchA2, main and Testing, as well as this readme. Testing is for testing, and the other 3 are the main functionality of the program; without any one of the three the program will NOT work correctly!

How To Run the implementation:

I.
from pycharm 
1.)    run the file called "main.py"
2.)    the program will ask you to enter a sub depth enter integer betweeen 1 and 8 
NOTE: depending on the algorithm you want to chose 8 or 7 might take too long; this is especially true with normal minimax!
3.)    next enter a number between 0 and 3 inclusive; this chooses the algorithm to run; 0 is minimax (no table), 1 is minimax (with table), 2 is Alpha-Beta (no table) and 3 is Alpha-Beta (no table)
4. wait for the results to finish in the console; you'll know when it's done by the info printing out all the moves at the end. You can also see the states by uncommenting 'search.print_out_move_info' on line 34 in main, if you need to.


II.
in terminal: 

enter "python3 main.py", then follow steps 2 and 3 as above in I.

III.
REFERENCES:
Things used/referenced by us in our creation of our implementation:
	-Alpha-Beta pseudocode in the AIMA textbook
	-Alpha-Beta pseduocode from wikipedia
		-https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
	-Code for games from the AIMA python resource
		-https://github.com/aimacode/aima-python/blob/master/games.py
	-Professor Michael Horsch's minmax code and game suite from the AI tutorials:
		-https://moodle.cs.usask.ca/mod/folder/view.php?id=21096