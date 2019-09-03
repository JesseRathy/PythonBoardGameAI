# The search space is a tree, but the state space is a graph: there may be several different ways to
# reach a given game state.
#
#
# The transposition table is a dictionary (hash table) that remembers if
# a game state was seen before, and it it was, what its minimax value is.

#collection of scores of each state
#should be the nect move of the game
from math import inf
import time as time

def print_out_move_info(score, turn, board):
    if board.isTerminal():
        score = board.utility()
        print('end of game')
    else:
        score = board.evaulate()
    print("score for move", str(turn) + ":", str(score))
    print("board for move", str(turn))
    board.display()






mm_exp_per_move  = []
mm_tt_nodecount  = []
mm_nodes_created = 0
mm_time_per_move = []

ab_exp_per_move  = []
ab_tt_nodecount  = []
ab_nodes_created = 0
ab_time_per_move = []

def print_final_performance(ver):
    print('preformance info: algo {}'.format(ver,))
    if ver == 0:
        print('average time per turn: ', str(sum(mm_time_per_move)/len(mm_time_per_move)))
        print('average node expanded per turn:', str(sum(mm_exp_per_move)/len(mm_exp_per_move)))
        print('Total nodes expanded: ', str(sum(mm_exp_per_move)))
    elif ver == 1:
        print('average time per turn: ', str(sum(mm_time_per_move) / len(mm_time_per_move)))
        print('average node expanded per turn:', str(sum(mm_exp_per_move) / len(mm_exp_per_move)))
        print('Total nodes expanded: ', str(sum(mm_exp_per_move)))
        print('Total transpositionTable nodes: ', str(sum(mm_tt_nodecount)))
    elif ver == 2:
        print('average time per turn: ', str(sum(ab_time_per_move) / len(ab_time_per_move)))
        print('average node expanded per turn:', str(sum(ab_exp_per_move) / len(ab_exp_per_move)))
        print('Total nodes expanded: ', str(sum(ab_exp_per_move)))
    else:
        print('average time per turn: ', str(sum(ab_time_per_move) / len(ab_time_per_move)))
        print('average node expanded per turn:', str(sum(ab_exp_per_move) / len(ab_exp_per_move)))
        print('Total nodes expanded: ', str(sum(ab_exp_per_move)))
        print('Total transpositionTable nodes: ', str(sum(ab_tt_nodecount)))
    print("------End of function-----\n")

def print_info_preformace(ver, turn):
    print('preformance info: algo {} turn {}'.format(ver, turn))
    if ver == 0:
        print("Time this turn :", str(mm_time_per_move[-1]) )
        print("Nodes searched this turn : ", str(mm_exp_per_move[-1]))
        #print("")
        #print("")
    elif ver == 1:
        print("Time this turn :", str(mm_time_per_move[-1]) )
        print("Nodes searched this turn : ", str(mm_exp_per_move[-1]))
        print("Count of TranspositionTable Nodes in Memory: ", str(mm_tt_nodecount[-1]))
        #print("")
    elif ver == 2:
        print("Time this turn :", str(ab_time_per_move[-1]) )
        print("Nodes searched this turn : ", str(ab_exp_per_move[-1]))
        #print("")
        #print("")
    else:
        print("Time this turn :", str(ab_time_per_move[-1]) )
        print("Nodes searched this turn : ", str(ab_exp_per_move[-1]))
        print("Count of TranspositionTable Nodes in Memory: ", str(ab_tt_nodecount[-1]))
        #print("")
    print("------End of function-----\n")







def minimax_no_tt(start, depth, turns):
    global mm_nodes_created, mm_time_per_move, mm_exp_per_move
    startt = time.process_time()
    """

    MINIMAX returns VALUE
    with TRANSPOSITION TABLE

    :param node:  a Game object responding to the following methods:
        str(): return a unique string describing the state of the game (for use in hash table)
        isTerminal(): checks if the game is at a terminal state
        utility(): obtain the value of a terminal node
        successors(): returns a list of all legal game states that extend this one by one move
        isMinNode(): returns True if the node represents a state in which Min is to move
        isMaxNode(): returns True if the node represents a state in which Max is to move
    :return: the value of the game state
    """
    def do_minimax(node, depthl, turns):
        global mm_nodes_created
        mm_nodes_created += 1
        #end of the game return winner score or draw
        if turns == 50 or node.isTerminal():
            u = node.utility()
        #hit sub depth limit return the eval when we have it made
        elif depthl == 0:
            u = node.evaulate()
        #gen the successors and do min or max
        else:
            vs = [do_minimax(c, depthl - 1, turns + 1) for c in node.successors()]
            # rare catch case
            #if wight u = max score in vs
            if node.isMaxNode():
                u = max(vs)
            # if queen u = min score in vs
            elif node.isMinNode():
                u = min(vs)
            else:
                print("Something went horribly wrong")
                return None
        return u
    is_wight = start.isMaxNode()
    max_best_score = -inf
    min_best_score = inf
    min_best_action = None
    max_best_action = None
    for a in start.successors():
        v = do_minimax(a, depth - 1, turns + 1)
        if is_wight:
            if v > max_best_score:
                max_best_score = v
                max_best_action = a
        else:
            if v < min_best_score:
                min_best_action = a
                min_best_score = v

    end = time.process_time()
    mm_time_per_move.append(end - startt)
    mm_exp_per_move.append(mm_nodes_created)
    mm_nodes_created = 0

    if not is_wight:
        if min_best_action.isTerminal():
            print_out_move_info(min_best_score, turns + 1, min_best_action)
            return None
        return min_best_score, min_best_action
    else:
        if max_best_action.isTerminal():
            print_out_move_info(max_best_score, turns + 1, max_best_action)
            return None
        return max_best_score, max_best_action






def minimax(start, depth, turns):
    global mm_nodes_created, mm_time_per_move, mm_tt_nodecount, mm_exp_per_move
    startt = time.process_time()
    """

    MINIMAX returns VALUE
    with TRANSPOSITION TABLE

    :param node:  a Game object responding to the following methods:
        str(): return a unique string describing the state of the game (for use in hash table)
        isTerminal(): checks if the game is at a terminal state
        utility(): obtain the value of a terminal node
        successors(): returns a list of all legal game states that extend this one by one move
        isMinNode(): returns True if the node represents a state in which Min is to move
        isMaxNode(): returns True if the node represents a state in which Max is to move
    :return: the value of the game state
    """
    transpositionTable = dict()
    def do_minimax(node, depthl, turns):
        global mm_nodes_created
        mm_nodes_created += 1
        #unique sting for the transpo table
        s = node.str()
        u = 0
        # already seen this state return the score
        if (s in transpositionTable) and depthl <= transpositionTable[s][1]:
            return transpositionTable[s][0]
        #end of the game return winner score or draw
        elif turns == 50 or node.isTerminal():
            u = node.utility()
        #hit sub depth limit return the eval when we have it made
        elif depthl == 0:
            u = node.evaulate()
        #gen the successors and do min or max
        else:
            vs = [do_minimax(c, depthl - 1, turns + 1) for c in node.successors()]
            # rare catch case
            #if wight u = max score in vs
            if node.isMaxNode():
                u = max(vs)
            # if queen u = min score in vs
            elif node.isMinNode():
                u = min(vs)
            else:
                print("Something went horribly wrong")
                return None
            #set the index to find the node we need to use for next move
            #ind = vs.index(u)
        # add the value score u to trans table
        transpositionTable[s] = u, depthl
        return u
    is_wight = start.isMaxNode()
    max_best_score = -inf
    min_best_score = inf
    min_best_action = None
    max_best_action = None
    for a in start.successors():
        v = do_minimax(a, depth - 1, turns + 1)
        if is_wight:
            if v > max_best_score:
                max_best_score = v
                max_best_action = a
        else:
            if v < min_best_score:
                min_best_action = a
                min_best_score = v
        s = a.str()
        transpositionTable[s] = v, depth
    end = time.process_time()
    mm_time_per_move.append(end - startt)
    mm_tt_nodecount.append(len(transpositionTable))
    mm_exp_per_move.append(mm_nodes_created)
    mm_nodes_created = 0
    if not is_wight:
        if min_best_action.isTerminal():
            print_out_move_info(min_best_score, turns + 1, min_best_action)
            return None
        return min_best_score, min_best_action
    else:
        if max_best_action.isTerminal():
            print_out_move_info(max_best_score, turns + 1, max_best_action)
            return None
        return max_best_score, max_best_action


def alphaBeta_no_tt(node, depth, maxplayer, turns):
    global ab_nodes_created, ab_time_per_move,ab_exp_per_move
    startt = time.process_time()
    def doAlphaBeta(node, depth, alpha, beta, maxplayer, turns):
        global ab_nodes_created
        ab_nodes_created += 1
        if turns == 50 or node.isTerminal():
            v = node.utility()
        elif depth == 0:
            v = node.evaulate()
        elif maxplayer:
            v = -inf
            for child in node.successors():
                v = max(v, doAlphaBeta(child, depth - 1, alpha, beta, False, turns + 1))
                if (beta <= v):
                    return v
                alpha = max(alpha, v)
        else:
            v = inf
            for child in node.successors():
                v = min(v, doAlphaBeta(child, depth - 1, alpha, beta, True, turns + 1))
                if (v <= alpha):
                    return v
                beta = min(beta, v)
        return v


    max_best_score = -inf
    min_best_score = inf
    min_best_action = None
    max_best_action = None
    if node.isMinNode():
        for a in node.successors():
            u = doAlphaBeta(a, depth - 1, max_best_score, min_best_score, not maxplayer, turns + 1)
            if u < min_best_score:
                min_best_action = a
                min_best_score = u
        end = time.process_time()
        ab_time_per_move.append(end - startt)
        ab_exp_per_move.append(ab_nodes_created)
        ab_nodes_created = 0
        if min_best_action.isTerminal():
            print_out_move_info(min_best_score, turns + 1, min_best_action)
            return None
        return min_best_score, min_best_action
    else:
        for a in node.successors():
            u = doAlphaBeta(a, depth - 1, max_best_score, min_best_score, not maxplayer, turns + 1)
            if u > max_best_score:
                max_best_action = a
                max_best_score = u
        end = time.process_time()
        ab_time_per_move.append(end - startt)
        ab_exp_per_move.append(ab_nodes_created)
        ab_nodes_created = 0
        if max_best_action.isTerminal():
            print_out_move_info(max_best_score, turns + 1, max_best_action)
            return None
        return max_best_score, max_best_action





def alphaBeta(node, depth, maxplayer, turns):
    global ab_nodes_created, ab_time_per_move, ab_tt_nodecount,ab_exp_per_move
    startt = time.process_time()
    mem_set = dict()
    def doAlphaBeta(node, depth, alpha, beta, maxplayer, turns):
        global ab_nodes_created
        ab_nodes_created += 1
        s = node.str()
        if s in mem_set and depth <= mem_set[s][1]:
            return mem_set[s][0]
        elif turns == 50 or node.isTerminal():
            v = node.utility()
        elif depth == 0:
            v = node.evaulate()
        elif maxplayer:
            v = -inf
            for child in node.successors():
                v = max(v, doAlphaBeta(child, depth - 1, alpha, beta, False, turns + 1))
                if (beta <= v):
                    return v
                alpha = max(alpha, v)
        else:
            v = inf
            for child in node.successors():
                v = min(v, doAlphaBeta(child, depth - 1, alpha, beta, True, turns + 1))
                if (v <= alpha):
                    return v
                beta = min(beta, v)
        mem_set[s] = v, depth
        return v


    max_best_score = -inf
    min_best_score = inf
    min_best_action = None
    max_best_action = None
    if node.isMinNode():
        for a in node.successors():
            u = doAlphaBeta(a, depth - 1, max_best_score, min_best_score, not maxplayer, turns + 1)
            if u < min_best_score:
                min_best_action = a
                min_best_score = u
            s = a.str()
            mem_set[s] = u, depth
        end = time.process_time()
        ab_time_per_move.append(end - startt)
        ab_tt_nodecount.append(len(mem_set))
        ab_exp_per_move.append(ab_nodes_created)
        ab_nodes_created = 0
        if min_best_action.isTerminal():
            print_out_move_info(min_best_score, turns + 1, min_best_action)
            return None
        return min_best_score, min_best_action
    else:
        for a in node.successors():
            u = doAlphaBeta(a, depth - 1, max_best_score, min_best_score, not maxplayer, turns + 1)
            if u > max_best_score:
                max_best_action = a
                max_best_score = u
            s = a.str()
            mem_set[s] = u, depth
        end = time.process_time()
        ab_time_per_move.append(end - startt)
        ab_tt_nodecount.append(len(mem_set))
        ab_exp_per_move.append(ab_nodes_created)
        ab_nodes_created = 0
        if max_best_action.isTerminal():
            print_out_move_info(max_best_score, turns + 1, max_best_action)
            return None
        return max_best_score, max_best_action




'''

def wiki_minimax(start, depth, maxi, turns):
    transpositionTable = dict()
    def do_wiki_minimax(node, depth, maxi, turns):
        s = node.str()
        u = 0
        # already seen this state return the score
        if s in transpositionTable:
            return transpositionTable[s]
        elif turns == 50 or node.isTerminal():
            u = node.utility()
        #hit sub depth limit return the eval when we have it made
        elif depth == 0:
            u = node.evaulate()
        elif maxi:
            bestVal = -inf
            for a in node.successors():
                u = do_wiki_minimax(a, depth - 1, False, turns + 1)
                bestVal = max(bestVal, u)
            u = bestVal
        else:
            bestVal = inf
            for a in node.successors():
                u = do_wiki_minimax(a, depth - 1, True, turns + 1)
                bestVal = min(bestVal, u)
            u = bestVal
        transpositionTable[s] = u
        return u
    max_best_score = -inf
    min_best_score = inf
    min_best_action = None
    max_best_action = None
    for a in start.successors():
        v = do_wiki_minimax(a, depth - 1, not maxi, turns + 1)
        if v > max_best_score:
            max_best_score = v
            max_best_action = a
        if v < min_best_score:
            min_best_action = a
            min_best_score = v
    if start.isMinNode():
        if min_best_action.isTerminal():
            print_out_move_info(min_best_score, turns + 1, min_best_action)
            return None
        return min_best_score, min_best_action
    else:
        if max_best_action.isTerminal():
            print_out_move_info(max_best_score, turns + 1, max_best_action)
            return None
        return max_best_score, max_best_action
'''
