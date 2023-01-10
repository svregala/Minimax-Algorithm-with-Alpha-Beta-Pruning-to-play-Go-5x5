# Name: Steve Regala
# CSCI 561 Homework 2: AI Solution for GO (5x5)
# Date Due: 10/26/2022

import math
from copy import deepcopy
import random

INPUT_NAME = "input.txt"
OUTPUT_NAME = "output.txt"
N = 5  # size of given board(5x5)
MAX_DEPTH = 4 
PLAYER_CONST = 3
MAX_STEP = N*N-1

start_board = [ [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
]

global_arr = [[-10.0, 0.0, 0.5, 0.0, -10.0], 
            [0.0, 0.5, 1.0, 0.5, 0.0], 
            [0.5, 1.0, 10.0, 1.0, 0.5], 
            [0.0, 0.5, 1.0, 0.5, 0.0], 
            [-10.0, 0.0, 0.5, 0.0, -10.0]
]

# Read in input.txt
# CITATION: Modified version of readInput() from read.py (given source file)
def readInput(path):
   with open(path,'r') as f:
      lines=f.readlines()
      piece_type = int(lines[0])
      previous_board = [[int(x) for x in line.rstrip('\n')] for line in lines[1:N+1]]
      board = [[int(x) for x in line.rstrip('\n')] for line in lines[N+1: 2*N+1]]

      return piece_type, previous_board, board


# Write to output.txt
# CITATION: Modified version of writeOutput() from write.py (given source file)
def writeOutput(result, path):
   with open(path,'w') as f:
      if result=="PASS":
         f.write(result)
      else:
         f.write(str(result[0]) + ',' + str(result[1]))


# Check if chosen move is valid
def valid(piece, x, y, prevBoard, currBoard):
   # see result when placing piece into specified spot
   temp_current = deepcopy(currBoard)
   temp_current[x][y] = piece
   
   # Criteria for what makes a valid move
   captured = captured_stones(PLAYER_CONST-piece, temp_current)
   temp_current = board_after_captured(PLAYER_CONST-piece, temp_current)
   liberty = find_liberty(x,y,temp_current)
   ko_rule = compare_board_KO(prevBoard, temp_current)
   if ((len(captured)>=1 and not ko_rule) or (len(captured)==0 and ko_rule) or (len(captured)==0 and not ko_rule)) and liberty:
      return True


# Remove dead stones in the board and update the board
# CITATION: Modified version of remove_died_pieces from host.py (given source file)
def board_after_captured(piece_type, currBoard):
   died_pieces = captured_stones(piece_type, currBoard)
   if len(died_pieces)==0: return currBoard
   update_board = remove_certain_pieces(died_pieces, currBoard)
   return update_board


# Remove stones of certain locations
# CITATION: Modified version of remove_certain_pieces() from host.py (given source file)
def remove_certain_pieces(positions, currBoard):
   for piece in positions:
      currBoard[piece[0]][piece[1]]=0
   return currBoard


# Compare previous board with current board to determine existence of KO
# CITATION: Modified version of compare_board() from host.py (given source file)
def compare_board_KO(board1, board2):
   for i in range(N):
      for j in range(N):
         if board1[i][j] != board2[i][j]:
            return False
   return True


# Find died stones that has no liberty given piece type
# CITATION: Modified version of find_died_pieces() from host.py (given source file)
def captured_stones(piece_type, currBoard):
   captured = []
   for i in range(N):
      for j in range(N):
         # check if there is a piece at this position
         if currBoard[i][j] == piece_type:
            if [i,j] not in captured:
               liberty = find_liberty(i,j,currBoard)
               # piece dies if it has no liberty
               if(not liberty):
                  captured.append([i,j])            
   return captured


# Detect all the neighbors of a given stone
# CITATION: Modified version of detect_neighbor() from host.py (given source file)
def detect_neighbor(i,j,currBoard):
   neighbors = []
   # Detect borders and add neighbor coordinates
   if i > 0: neighbors.append((i-1, j))
   if i < len(currBoard) - 1: neighbors.append((i+1, j))
   if j > 0: neighbors.append((i, j-1))
   if j < len(currBoard) - 1: neighbors.append((i, j+1))
   return neighbors


# Detect neighbor allies of a given stone
# CITATION: Modified version of detect_neighbor_ally() from host.py (given source file)
def detect_neighbor_ally(i,j,currBoard):
   group_allies = []
   neighbors = detect_neighbor(i,j,currBoard)
   # Iterate through neighbors
   for piece in neighbors:
      # Add allies to list if having the same color
      if currBoard[piece[0]][piece[1]] == currBoard[i][j]:
         group_allies.append(piece)
   return group_allies


# Use DFS to search for all allies of stone
# CITATION: Modified version of ally_dfs() from host.py (given source file)
def ally_dfs(i,j,currBoard):
   stack = [[i,j]]
   ally_members = []
   while stack:
      piece = stack.pop()
      ally_members.append(piece)
      neighbor_allies = detect_neighbor_ally(piece[0], piece[1], currBoard)
      for ally in neighbor_allies:
         if ally not in stack and ally not in ally_members:
            stack.append(ally)
   return ally_members


# Find liberty of a given stone, if group of allied stones has no liberty, they die
# CITATION: Modified version of find_liberty() in host.py (given source file)
def find_liberty(x,y,currBoard):
   liberty = 0
   ally_members = ally_dfs(x,y,currBoard)
   for member in ally_members:
      neighbors = detect_neighbor(member[0],member[1],currBoard)
      for piece in neighbors:
          # If there is empty space around a piece, it has liberty
         if currBoard[piece[0]][piece[1]] == 0:
            liberty += 1
   # If none of the pieces in a allied group has an empty space, it has no liberty
   return liberty

# Minimax Algorithm using alpha-beta pruning for Stage 1
def find_optimal_moves(previous, current, piece, alpha, beta, depth):
   top_score = 0
   results = []
   enemy = PLAYER_CONST - piece
   temp_current = deepcopy(current)

   # First find all possible moves given piece type
   #options = possibilities(previous, current, piece)
   options = []
   for i in range(N):
      for j in range(N):
         if current[i][j]==0:
            valid_move = valid(piece, i, j, previous, current)
            if(valid_move):
               options.append([i,j])

   # Explore each of the possibilities
   for option in options:
      possible_move = possibility(option, current, piece)
      prune = alpha_beta_MIN_value(alpha, beta, depth, enemy, temp_current, possible_move, CURR_STEP+1)*-1

      # if our prune score is greater than our top score so far, clear the results 
      # and append the newer and better option, same goes for if our results is empty
      # if we've reached top score with another option, add that option to the results
      if prune > top_score:
         top_score = prune
         results.clear()
         results.append(option)
         alpha = top_score
      elif top_score == prune:
         results.append(option)
      elif len(results)==0:
         top_score = prune
         results.clear()
         results.append(option)
         alpha = top_score
      
   return results


# Helper function to create the state while exploring an option
def possibility(option, current, piece_type):
   next = PLAYER_CONST-piece_type
   result = deepcopy(current)
   result[option[0]][option[1]] = piece_type
   result = board_after_captured(next, result)
   return result 


# Evaluate the score for the given state; uses the liberty of a given stone/group of stones
# Evaluation function considers the following: (CITATION: Page 36 of http://erikvanderwerf.tengen.nl/pubdown/thesis_erikvanderwerf.pdf)
# (1) maximising the number of stones on the board, (2) maximising the number of liberties,
# (3) avoiding moves on the edge/corners, (4) making eyes
def evaluate_option(piece_type, state): 
   our_turn = True if piece_type == our_piece else False
   temp_pro, final_pro = 0, 0
   temp_con, final_con = 0, 0
   differ_result_pro, differ_result_con = 0, 0
   enemy = PLAYER_CONST - our_piece
   for i in range(N):
      for j in range(N):
         # Enemy
         if state[i][j] == enemy:
            con_liberty_count = find_liberty(i, j, state)   # number of liberties
            con_eye_space = eye_space(i,j,state)   # number of eyes
            temp_con = temp_con + 1   # number of respective pieces
            final_con = final_con + temp_con + con_liberty_count + global_arr[i][j] + con_eye_space # global_arr is used for reason #3
         # Global variable of our piece
         elif state[i][j] == our_piece:
            pro_liberty_count = find_liberty(i, j, state)   # number of liberties
            pro_eye_space = eye_space(i,j,state)   # number of eyes
            temp_pro = temp_pro + 1   # number of respective pieces
            final_pro = final_pro + temp_pro + pro_liberty_count + global_arr[i][j] + pro_eye_space # global_arr is used for reason #3

   differ_result_pro = final_pro - final_con
   differ_result_con = -1 * differ_result_pro
   if not our_turn:
      return differ_result_con
   else:
      return differ_result_pro
   
   #if not our_turn: return final_con
   #else: return final_pro

#############################################################

# Get all the diagonals of a given point on the board
def detect_diagonals(x,y,currBoard):
   diagonals = []
   if x>0 and y>0: diagonals.append((x-1,y-1))
   if x>0 and y<len(currBoard)-1: diagonals.append((x-1,y+1))
   if x<len(currBoard)-1 and y<len(currBoard)-1: diagonals.append((x+1,y+1))
   if x<len(currBoard)-1 and y>0: diagonals.append((x+1,y-1))
   return diagonals

# Returns a count of spots where an eye could be formed, counting the number of diagonally placed unconditionally alive defender stones
# CITATION: Page 39 of http://erikvanderwerf.tengen.nl/pubdown/thesis_erikvanderwerf.pdf
def eye_space(i, j, state):
   result = 0
   diag_members = detect_diagonals(i,j,state)
   for diag in diag_members:
      if state[diag[0]][diag[1]] == state[i][j]:
         result += 1

   return result


#############################################################


# Recursive implementation of Minimax with alpha-beta algorithm
# CITATION: Based off of algorithm on slide 39 from Lecture 6: Game-Playing
def alpha_beta_MAX_value(alpha, beta, depth, piece, old_state, possible_move, current_step):
   # Base case
   top_score = evaluate_option(piece, possible_move)
   if depth == 0 or current_step > MAX_STEP: return top_score
   
   temp_current = deepcopy(possible_move)
   enemy = PLAYER_CONST-piece
   options = []
   for i in range(N):
      for j in range(N):
         if possible_move[i][j]==0:
            valid_move = valid(piece, i, j, old_state, possible_move)
            if valid_move:
               options.append([i,j])

   for option in options:
      branch = possibility(option, possible_move, piece)
      # Recursive call, if prune score is better than current top score, reassign top score to prune
      top_score = max(top_score, alpha_beta_MIN_value(alpha, beta, depth-1, enemy, temp_current, branch, current_step+1)*-1)

      # Prune here:
      # CITATION: Modified version of slide 39 from Lecture 6: Game-Playing
      v = top_score*-1
      if v < beta: return top_score
      if top_score > alpha: alpha = top_score

   return top_score


# Recursive implementation of Minimax with alpha-beta algorithm
# CITATION: Based off of algorithm on slide 39 from Lecture 6: Game-Playing
def alpha_beta_MIN_value(alpha, beta, depth, piece, old_state, possible_move, current_step):
   # Base case
   top_score = evaluate_option(piece, possible_move)
   if depth == 0 or current_step > MAX_STEP: return top_score
   
   temp_current = deepcopy(possible_move)
   enemy = PLAYER_CONST-piece
   options = []
   for i in range(N):
      for j in range(N):
         if possible_move[i][j]==0:
            valid_move = valid(piece, i, j, old_state, possible_move)
            if valid_move:
               options.append([i,j])

   for option in options:
      branch = possibility(option, possible_move, piece)
      # Recursive call, if prune score is better than current top score, reassign top score to prune
      top_score = max(top_score, alpha_beta_MAX_value(alpha, beta, depth-1, enemy, temp_current, branch, current_step+1)*-1)

      # Prune here:
      # CITATION: Modified version of slide 39 from Lecture 6: Game-Playing
      v = top_score*-1
      if v < alpha: return top_score
      if top_score > beta: beta = top_score

   return top_score


# First move advantage, pick center of the 5x5 board
# Important Note: Pick center only if my_player is first(black stones) OR if my_player is second(white stones)
# First and Second refer to turns also
# CITATION: http://erikvanderwerf.tengen.nl/5x5/5x5solved.html
def first_move(piece, current):
   free_center = True
   count_turns = 0
   for i in range(N):
      for j in range(N):
         if current[i][j]!=0: # indicator for being the first move
            if(i==2 and j==2):
               free_center = False
            count_turns+=1

   # first condition: if (1)center is free, (2)piece type is BLACK stones, and (3)0 turns have been performed
   # second condition: if (1)center is free, (2)piece type is WHITE stones, and (3)only 1 turn has been performed
   if((free_center and piece==1 and count_turns==0) or (free_center and piece==2 and count_turns<=1)):
      return True
   return False


# ----------------------------- Run Program -----------------------------
def runProgram(piece, previous, current):
   final_action = []
   if(first_move(piece,current)):
      final_action.append([2,2])
   else:
      final_action = find_optimal_moves(previous, current, piece, -math.inf, math.inf, MAX_DEPTH)

   if len(final_action) == 0:
      writeOutput('PASS', OUTPUT_NAME)
   else:
      rand_num = random.randint(0, len(final_action)-1)
      action = final_action[rand_num]
      writeOutput(action, OUTPUT_NAME)


our_piece, previous_board, current_board = readInput(INPUT_NAME)

def get_current_step():
   # previous board same as starting board indicates that it's the first move
   if previous_board == start_board:
      with open("count_step.txt", 'w') as f:
         f.write(str(2+our_piece))
      return our_piece
   
   # Otherwise, read in count_step.txt to get current step
   with open("count_step.txt", 'r') as f:
      line = f.readlines()
      result_step = int(line[0])
      with open("count_step.txt", 'w') as g:
         g.write(str(2+result_step))
      return result_step

CURR_STEP = get_current_step()
runProgram(our_piece, previous_board, current_board)
