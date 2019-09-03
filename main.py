import ChessVar as Game2
import GameTreeSearchA2 as search

import time as time

def main():
    in_depth = int(input("input the sub depth limit"))
    in_algo  = int(input("input the version you want to use 0 for minimax no ttables5 1 for minimax 2 for alpha beta no ttables 3 for alpha beta"))
    b = Game2.ChessVar(None, player='W')
    b.display()

    start = time.process_time()
    """is this what mike means by only doing 10 moves at a time like do this for loop calling minimax with depth 10"""
    #for each 50 moves we will call minimax
    for i in range(50):
        #depth for searching for each move is limited to 10
        depth = in_depth
        if i+depth > 50:
            depth = 50 - i
        if in_algo == 0:
            result = search.minimax_no_tt(b, depth, i)
        elif in_algo == 1:
            result = search.minimax(b, depth, i)
        elif in_algo == 2:
            result = search.alphaBeta_no_tt(b, depth, ((i % 2) == 0), i)
        else:
            result = search.alphaBeta(b, depth, ((i % 2) == 0), i)
        #search.print_info_preformace(in_algo,i)
        #result = wiki_minimax(b, depth, (i%2==0), i)
        if result is not None:
            score, move_add_1 = result
            #make b the next move in the game
            b = move_add_1
            search.print_out_move_info(score, i + 1, b)
        else:
            break
    end = time.process_time()
    print('Took', end-start, 'seconds to determine the search value')
    search.print_final_performance(in_algo)

if __name__ == '__main__':
    main()
