board_pos = [(1, 1),(1, 2),(1, 3),(1, 4),(1, 5),(2, 1),(2, 2),(2, 3),(2, 4),(2, 5),(3, 1),(3, 2),(3, 3),(3, 4),(3, 5),(4, 1),(4, 2),(4, 3),(4, 4),(4, 5),(5, 1),(5, 2),(5, 3),(5, 4),(5, 5)]
class ChessVar:
    # Represent the gamestate for tic tac toe.
    #  Minimax assumes objects that respond to the following methods:
    #     str(): return a unique string describing the state of the game (for use in hash table)
    #     isTerminal(): checks if the game is at a terminal state
    #     successors(): returns a list of all legal game states that extend this one by one move
    #     isMinNode(): returns True if the node represents a state in which Min is to move
    #     isMaxNode(): returns True if the node represents a state in which Max is to move

    def __init__(self, state, player):
        """
        Create a new object
        :param state: a description of the board for the current state
        :param player: whose turn it isto play in the current state
        :return:
        """
        if state is None:
            self.gameState = dict()
            for i in range(1, 6):
                self.gameState[5,i] = 'W'
            self.gameState[1,3] = 'Q'
            self.gameState[2,2] = 'D'
            self.gameState[2,3] = 'D'
            self.gameState[2,4] = 'D'
        else:
            self.gameState = state
        self.whoseTurn = player
        self.cachedWin = False  # set to True in winFor() if
        self.cachedWinner = None

    def str(self):
        """ *** needed for search ***
        Translate the board description into a string.  Could be used as for a hash table...
        :return: A string that describes the board in the current state.
        """
        return ''.join([self.gameState[i] if i in self.gameState else '.' for i in board_pos])+str(self.whoseTurn=='W')


    def isMinNode(self):
        """ *** needed for search ***
        :return: True if it's Min's turn to play
        """
        return self.whoseTurn == 'Q'


    def isMaxNode(self):
        """ *** needed for search ***
        :return: True if it's Max's turn to play
        """
        return self.whoseTurn == 'W'


    def isTerminal(self):
        """ *** needed for search ***
        :param node: a game tree node with stored game state
        :return: a boolean indicating if node is terminal
        """
        return self.winFor('W') or self.winFor('Q') or self.wight_move_count() == 0

    def move(self, cord1, cord2):
        """
        Create a new board description adding the given move.
        :param where: Where the move was
        :param who: who moved there
        :return: a copy of the current state with the additional move included
        """
        gs = self.gameState.copy()
        gs[cord2] = gs[cord1]
        gs.pop(cord1)
        return gs

    def wight_cap_v2(self, lr, cord1, cord2):
        if lr and (cord2 in self.gameState and self.gameState[cord2] != 'W'):
            return ChessVar(self.move(cord1, cord2), 'Q')
        else:
            return None

    def wight_move_v2(self, cord1, cord2):
        if cord2 not in self.gameState:
            return ChessVar(self.move(cord1, cord2), 'Q')
        else:
            return None

    def wight_successors(self):
        # moves for wights
        nodes = []
        # moving wights posistions
        app = nodes.append
        for k, v in self.gameState.items():
            if v == 'W':
                # store x and y
                yp, xp = k
                # check if a wight can move up down left and right
                up = yp > 1
                down = yp < 5
                left = xp > 1
                right = xp < 5
                # make moves in the up directions and check for captures
                if up:
                    un  = self.wight_move_v2(k,        (yp - 1, xp))
                    uln = self.wight_cap_v2 (left,  k, (yp - 1, xp - 1))
                    urn = self.wight_cap_v2 (right, k, (yp - 1, xp + 1))
                    if un is not None:
                        app(un)
                    if uln is not None:
                        app(uln)
                    if urn is not None:
                        app(urn)
                # make moves in the down directions and check for captures
                if down:
                    dn  = self.wight_move_v2(k,        (yp + 1, xp))
                    dln = self.wight_cap_v2 (left,  k, (yp + 1, xp - 1))
                    drn = self.wight_cap_v2 (right, k, (yp + 1, xp + 1))
                    if dn is not None:
                        app(dn)
                    if dln is not None:
                        app(dln)
                    if drn is not None:
                        app(drn)
                # make moves left or right
                if right:
                    rn = self.wight_move_v2(k, (yp, xp + 1))
                    if rn is not None:
                        app(rn)
                if left:
                    ln = self.wight_move_v2(k, (yp, xp - 1))
                    if ln is not None:
                        app(ln)
        return nodes

    def queendrag_move_v2(self, cord1, cord2):
        if cord2 not in self.gameState or (self.gameState[cord2] != 'D' and self.gameState[cord2] != 'Q'):
            return ChessVar(self.move(cord1, cord2), 'W')
        else:
            return None


    def queens_successors(self):
        nodes = []
        # moving pos for dragons and queen
        app = nodes.append
        for k, v in self.gameState.items():
            # x and y stored
            if v != 'W':
                yp, xp = k
                # find directiosn that can move
                up = yp > 1
                down = yp < 5
                left = xp > 1
                right = xp < 5

                # set up the bounds for the for loops
                row_s = yp - 1 if up else yp
                row_e = yp + 2 if down else yp + 1
                col_s = xp - 1 if left else xp
                col_e = xp + 2 if right else xp + 1
                # iterate over the eight squares

                for r in range(row_s, row_e):
                    for c in range(col_s, col_e):
                        new_node = self.queendrag_move_v2(k, (r, c))
                        if new_node is not None:
                            app(new_node)
                        #nodes = self.queendrag_move(k, (r, c),nodes)
        return nodes

    def successors(self):
        """ *** needed for search ***
        :param node:  a game tree node with stored game state
        :return: a list of game tree nodes that are the next possible states
        """
        #queen moves
        if self.whoseTurn == 'W':
            return self.wight_successors()
        else:
            return self.queens_successors()

    def utility(self):
        """ *** needed for search ***
        :return: 1 if win for X, -1 for win for O, 0 for draw
        """
        if self.winFor('W'):
            return 2000
        elif self.winFor('Q'):
            return -2000
        else:
            return 0


    # all remaining methods are to assist in the calculatiosn

    def winFor(self, player):
        """
        Check if it's a win for player.
        Note the use of a cache.  This prevents re-computation in functions isTerminal() and utility()
        :param player: either 'W' or 'Q'
        :return: True if player appears 3 in a row, column, diagonal
        """
        if self.cachedWin is False:
            # rows columns diagonals
            won = False
            #Check wight win condition
            if player == 'W':
                #If the queen isn't in dictionary, queen was captured
                #If queen is gone, wights win
                won = 'Q' not in [v for k, v in self.gameState.items()]
            #Check DragonQueen win condition
            else:
                #check if the first value of the tuple (the y value is equal to 5 (wight area), if it is,get the value
                #if that value is Q, won == true, false otherwise
                won = 'Q' in [v for k, v in self.gameState.items() if list(k)[0] == 5]
            if won:
                self.cachedWin = True
                self.cachedWinner = player
                return True
            else:
                return False
        else:
            return player == self.cachedWinner



    def togglePlayer(self,p):
        """
        :param p: either 'W' or 'Q'
        :return:  the other player's symbol
        """
        if p == 'W':
            return 'Q'
        else:
            return 'W'

    def wight_cap_blank(self, lr, cord2):
        if lr and (cord2 in self.gameState and self.gameState[cord2] != 'W'):
            return 1
        else:
            return 0

    def wight_move_blank(self, cord2):
        if cord2 not in self.gameState:
            return 1
        else:
            return 0

    def wight_move_count(self):
        """
        :return: a list of available places to put a marker
        """
        counter = len([k for k, v in self.gameState.items() if v == 'W'])
        if counter == 0:
            return 0
        else:
            for k, v in self.gameState.items():
                if v =='W':
                    #store x and y
                    yp, xp = k

                    # check if a wight can move up down left and right
                    up    = yp > 1
                    down  = yp < 5
                    left  = xp > 1
                    right = xp < 5
                    #make moves in the up directions and check for captures
                    if up:
                        if self.wight_move_blank((yp - 1, xp)) == 1:
                            return 1
                        if self.wight_cap_blank(left,  (yp - 1, xp - 1)) == 1:
                            return 1
                        if self.wight_cap_blank(right, (yp - 1, xp + 1)) == 1:
                            return 1
                            #make moves in the down directions and check for captures
                    if down:
                        if self.wight_move_blank((yp + 1, xp)) == 1:
                            return 1
                        if self.wight_cap_blank(left,  (yp + 1, xp - 1)) == 1:
                            return 1
                        if self.wight_cap_blank(right, (yp + 1, xp + 1)) == 1:
                            return 1
                        #make moves left or right
                    if right:
                        if self.wight_move_blank((yp, xp + 1)) == 1:
                            return 1
                    if left:
                        if self.wight_move_blank((yp, xp - 1)) == 1:
                            return 1
        return 0

    def testBoard(self):
        testState = dict()
        testState[2, 2] = 'W'
        testState[2, 3] = 'W'
        testState[2, 4] = 'W'
        testState[3, 4] = 'W'
        testState[4, 4] = 'W'
        testState[4, 3] = 'W'
        testState[4, 2] = 'W'
        testState[3, 2] = 'W'
        testState[3, 3] = 'Q'
        tmpBoard1 = ChessVar(testState, 'W')
        tmpBoard2 = ChessVar(testState, 'Q')
        tmp1 = tmpBoard1.successors()
        tmp2 = tmpBoard2.successors()
        print("showing successors when wights moves")
        for i in tmp1:
            print()
            print()
            print()
            i.display()
        print("showing successors when queen moves")
        for i in tmp2:
            print()
            print()
            print()
            i.display()

    def testBoard2(self):
        testState = dict()
        testState[2, 2] = 'D'
        testState[2, 3] = 'D'
        testState[2, 4] = 'D'
        testState[3, 4] = 'D'
        testState[4, 4] = 'D'
        testState[4, 3] = 'D'
        testState[4, 2] = 'D'
        testState[3, 2] = 'D'
        testState[3, 3] = 'W'
        tmpBoard1 = ChessVar(testState, 'W')
        tmpBoard2 = ChessVar(testState, 'Q')
        tmp1 = tmpBoard1.successors()
        tmp2 = tmpBoard2.successors()
        print("showing successors when wights moves")
        for i in tmp1:
            print()
            print()
            print()
            i.display()
        print("showing successors when queen moves")
        for i in tmp2:
            print()
            print()
            print()
            i.display()


    def display(self):
        """
        A pleasant view of the current game state
        :return: nothing
        """
        print(self.whoseTurn+"'s turn to move")
        print(" __________\n")
        for r in range(1, 6):
            for c in range(1, 6):
                if (r, c) in self.gameState:
                    print('',self.gameState[r,c], end="")
                else:
                    print(' .', end="")
            print('\n')
        print(" __________")
        print()
        print()
        print()




    def evaulate(self):#call the other evaluation functions with some multipliers and some scalers whoa
        a, b, c, d = 1, 1, 1, 1
        return a*self.queenDangerEvaluate() + b*self.wightGroupEval() + c*self.pieceBoardEval() + d*self.dist_queen_goal()

    def dist_queen_goal(self):
        for k, v in self.gameState.items():
            if v == 'Q':
                y, x = k
                return (y)*-400
        return 0

    def queenDangerEvaluate(self):
        queenDangerValue = 500
        x = False
        for k,v in self.gameState.items():
            #print(v)
            if v == 'Q':
                yp, xp = k
                ul = (yp - 1, x - 1)
                ur = (yp - 1, x + 1)
                bl = (yp + 1, x - 1)
                br = (yp + 1, x + 1)
                #print("[",str(yp),",",str(xp),"]")
                ##If queen can be captured upward
                if (ul in self.gameState and self.gameState[ul] == 'W') or (ur in self.gameState and self.gameState[ur] == 'W'):
                    return queenDangerValue if self.whoseTurn == 'W' else -queenDangerValue
                if (bl in self.gameState and self.gameState[bl] == 'W') or (br in self.gameState and self.gameState[br] == 'W'):
                    return queenDangerValue if self.whoseTurn == 'W' else -queenDangerValue
                #Otherwise, this is untrue
                else:
                    return 0

    def wightGroupEval(self):
        wightDiagValue = 400
        wightSideValue = 200
        sumValues = 0
        wights = {k:v for k, v in self.gameState.items() if v == 'W'}
        donewight = dict()
        '''
        for k, v in self.gameState.items():
            #print(v)
            ##Get all the wight positions, put them in a dictionary
            if v == 'W':
                wights[k] = v
            
                xp,yp = k
                up = yp > 1
                down = yp < 5
                left = xp > 1
                right = xp < 5
                print("[" + yp + "," + xp + "]")
        '''
        for k, v in wights.items():
            yp, xp = k
            u  = (yp - 1, xp)
            d  = (yp + 1, xp)
            l  = (yp    , xp - 1)
            r  = (yp    , xp + 1)
            ul = (yp - 1, xp - 1)
            ur = (yp - 1, xp + 1)
            dl = (yp + 1, xp - 1)
            dr = (yp + 1, xp + 1)
            # Then check the cardinal directions; give them less value but still give them value if they're around
            if u in wights and u not in donewight:
                sumValues += wightSideValue
            if d in wights and d not in donewight:
                sumValues += wightSideValue
            if l in wights and l not in donewight:
                sumValues += wightSideValue
            if r in wights and r not in donewight:
                sumValues += wightSideValue
            #Then check the diagonals
            if ul in wights and ul not in donewight:
                sumValues += wightDiagValue
            if ur in wights and ur not in donewight:
                sumValues += wightDiagValue
            if dl in wights and dl not in donewight:
                sumValues += wightDiagValue
            if dr in wights and dr not in donewight:
                sumValues += wightDiagValue
            donewight[k] = v
        return sumValues

    def pieceBoardEval(self):
        sumPieceValues = 0
        dragonValue = -200
        queenValue = -300
        wightValue = 150
        rSum = sum([wightValue if v == 'W' else dragonValue if v == 'D' else queenValue for k, v in self.gameState.items()])
        '''
        for k, v in self.gameState.items():
            if v == 'W':
                sumPieceValues += wightValue
            elif v == 'D':
                sumPieceValues += dragonValue
            elif v == 'Q':
                sumPieceValues += queenValue
            else:
                print("Problem!")
        '''
        return rSum