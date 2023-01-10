# Minimax-Algorithm-with-Alpha-Beta-Pruning-to-play-Go-5x5
- For the full project description, please take a look at Project_Description.pdf
- Synopsis: Artificial Intelligence (AI) agent uses the Minimax Algorithm with Alpha-Beta Pruning to play Go-5x5 (Go on a 5x5 board).
- The program takes in an input file and produces an output file. The first line of the input file is a value of 1 or 2 (Black piece == 1, White == 2). The next 5 lines (lines 2-6) describe the previous state of the board and the following 5 lines (lines 7-11) describes the current state of the game board. Similarly, the output file is generated after performing a move and has a similar structure as the input file, except with updated previous and current boards.

Notes:
- My AI agent outperformed random, greedy, aggressive, alpha-beta, and Q-learner agents constructed by course producers.
- The folder myplayer_play consists of host.py (program that facilitates a Go game between 2 agents), read.py and write.py (both used by the host.py to read from input and write to output). This folder was used for developing the foundation of program; it runs my program against the random player (player that chooses random spots on each turn).