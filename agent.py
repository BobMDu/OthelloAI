"""
An AI player for Othello.
"""

import random
import sys
import time

#caching dictionary
cache = {}

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)

# Method to compute utility value of terminal state
def compute_utility(board, color):
    #IMPLEMENT'
    disks = get_score(board)

    if color == 1:
        return disks[0] - disks[1]
    elif color == 2:
        return disks[1] - disks[0]

# Better heuristic value of board
def compute_heuristic(board, color): #not implemented, optional
    #IMPLEMENT
    return 0 #change this!

############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0):
    #IMPLEMENT
    if color == 1:
        opponent_color = 2
    elif color == 2:
        opponent_color = 1
    moves = get_possible_moves(board, opponent_color)
    if not moves or limit == 0:
        return (None, compute_utility(board, color))
    else:
        best_move = (None, float("Inf"))
        for move in moves:
            new_board = play_move(board, opponent_color, move[0], move[1])
            if caching:
                if new_board in cache:
                    move_utility = (move, cache[new_board])
                else:
                    move_utility = (move, minimax_max_node(new_board, color, limit-1, caching)[1])
                    cache[new_board] = move_utility[1]
            else:
                move_utility = (move, minimax_max_node(new_board, color, limit-1, caching)[1])
            if best_move[1] > move_utility[1]:
                best_move = move_utility
        return best_move

def minimax_max_node(board, color, limit, caching = 0): #returns highest possible utility
    #IMPLEMENT
    moves = get_possible_moves(board, color)
    if not moves or limit == 0:
        return (None, compute_utility(board, color))
    else:
        best_move = (None, float("-Inf"))
        for move in moves:
            new_board = play_move(board, color, move[0], move[1])
            if caching:
                if new_board in cache:
                    move_utility = (move, cache[new_board])
                else:
                    move_utility = (move, minimax_min_node(new_board, color, limit-1, caching)[1])
                    cache[new_board] = move_utility[1]
            else:
                move_utility = (move, minimax_min_node(new_board, color, limit-1, caching)[1])
            if best_move[1] < move_utility[1]:
                best_move = move_utility
        return best_move

def select_move_minimax(board, color, limit, caching = 0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    """
    #IMPLEMENT
    return minimax_max_node(board, color, limit, caching)[0] #change this!

############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    #IMPLEMENT
    if color == 1:
        opponent_color = 2
    elif color == 2:
        opponent_color = 1
    moves = get_possible_moves(board, opponent_color)
    if ordering:
        moves = sort_moves(board, color, opponent_color, moves)
    if not moves or limit == 0:
        return (None, compute_utility(board, color))
    else:
        best_move = (None, float("Inf"))
        for move in moves:
            new_board = play_move(board, opponent_color, move[0], move[1])
            if caching:
                if new_board in cache:
                    move_utility = (move, cache[new_board])
                else:
                    move_utility = (move, alphabeta_max_node(new_board, color, alpha, beta, limit-1, caching, ordering)[1])
                    cache[new_board] = move_utility[1]
            else:
                move_utility = (move, alphabeta_max_node(new_board, color, alpha, beta, limit-1, caching, ordering)[1])
            if best_move[1] > move_utility[1]:
                best_move = move_utility
            if beta > best_move[1]:
                beta = best_move[1]
                if beta <= alpha:
                    break
        return best_move

def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    #IMPLEMENT
    moves = get_possible_moves(board, color)
    if ordering:
        moves = sort_moves(board, color, color, moves)
    if not moves or limit == 0:
        return (None, compute_utility(board, color))
    else:
        best_move = (None, float("-Inf"))
        for move in moves:
            new_board = play_move(board, color, move[0], move[1])
            if caching:
                if new_board in cache:
                    move_utility = (move, cache[new_board])
                else:
                    move_utility = (move, alphabeta_min_node(new_board, color, alpha, beta, limit-1, caching, ordering)[1])
                    cache[new_board] = move_utility[1]
            else:
                move_utility = (move, alphabeta_min_node(new_board, color, alpha, beta, limit-1, caching, ordering)[1])
            if best_move[1] < move_utility[1]:
                best_move = move_utility
            if alpha < best_move[1]:
                alpha = best_move[1]
                if beta <= alpha:
                    break
        return best_move

def sort_moves(board, color, turn_color, moves):
    sorted = []
    for move in moves:
        new_board = play_move(board, turn_color, move[0], move[1])
        sorted.append((move, compute_utility(new_board, color)))

    if turn_color == color:
        for i in range(len(sorted)):
            max_utility = i
            for j in range(i+1, len(sorted)):
                if sorted[max_utility][1] < sorted[j][1]:
                    max_utility = j
            sorted[i], sorted[max_utility] = sorted[max_utility], sorted[i]
    else:
        for i in range(len(sorted)):
            min_utility = i
            for j in range(i+1, len(sorted)):
                if sorted[min_utility][1] > sorted[j][1]:
                    min_utility = j
            sorted[i], sorted[min_utility] = sorted[min_utility], sorted[i]

    result = []
    for move in sorted:
        result.append(move[0])
    return result

def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations.
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations.
    """
    #IMPLEMENT

    return alphabeta_max_node(board, color, float("-Inf"), float("Inf"), limit, caching, ordering)[0] #change this!

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI") # First line is the name of this AI
    arguments = input().split(",")

    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light.
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)

            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
