import pygame
import random
from param import *
from board import *
from sprites import *
from collections import deque
from copy import deepcopy


class HeuristicMaker:
    def __init__(self, c1, c2, c3, c4):
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.c4 = c4

    def get_constances(self):
        return [self.c1, self.c2, self.c3, self.c4]


def heuristic(state, heuristicMaker):
    path1 = len(bfs(state.get_player1(), state))
    path2 = len(bfs(state.get_player2(), state))
    shortestPathDiff = path2 - path1
    diffWalls = state.get_player2().get_num_of_walls() - state.get_player1().get_num_of_walls()
    diffOfSideBenefits = sideOfPlayer(state.get_player1()) - sideOfPlayer(state.get_player2())
    diffManhattan = manhattan_distance(state.get_player2()) - manhattan_distance(state.get_player1())
    evaluation = heuristicMaker.get_constances()[0] * shortestPathDiff + heuristicMaker.get_constances()[1] * diffWalls + \
                 heuristicMaker.get_constances()[2] * diffOfSideBenefits + heuristicMaker.get_constances()[
                     3] * diffManhattan

    return evaluation


def manhattan_distance(player):
    shortestManhattanDist = numberOfRows - player.get_player_x()
    normalDist = shortestManhattanDist / numberOfRows
    return normalDist


def sideOfPlayer(player):
    if player.get_player_number() == 1:
        if 0 <= player.get_player_x() <= 8:
            return 0
        if 9 <= player.get_player_x() <= 16:
            return 1
    if player.get_player_number() == 2:
        if 0 <= player.get_player_x() <= 8:
            return 1
        if 9 <= player.get_player_x() <= 16:
            return 0


def make_result(state, move, player, playerNumber):
    if move is not None:
        if get_valid_moves(state.get_state_board(), player).__contains__(move):
            newStateBoard = deepcopy(state.get_state_board())
            newPlayer = Player(player.get_player_number(), player.get_square_number(), 1, newStateBoard)
            newPlayer.set_num_of_walls(player.get_num_of_walls())
            squareNumber = newPlayer.get_square_number()
            # disabling former player square
            if playerNumber == 1:
                if newPlayer.get_player_number() == 1:
                    newPlayer.set_square_number(move, newStateBoard)
                    newState = GameState(newPlayer, state.get_player2(), newStateBoard)

                elif newPlayer.get_player_number() == 2:
                    newPlayer.set_square_number(move, newStateBoard)
                    newState = GameState(state.get_player1(), newPlayer, newStateBoard)

            if playerNumber == 2:
                if newPlayer.get_player_number() == 1:
                    newPlayer.set_square_number(move, newStateBoard)
                    newState = GameState(state.get_player1(), newPlayer, newStateBoard)

                elif newPlayer.get_player_number() == 2:
                    newPlayer.set_square_number(move, newStateBoard)
                    newState = GameState(newPlayer, state.get_player2(), newStateBoard)

            return newState
        # else its a wall move:
        else:
            newStateBoard = deepcopy(state.get_state_board())
            # Horizental Wall
            if newStateBoard[move].get_x() % 2 == 1 and move % 17 != 14:
                newStateBoard[move].set_contaning_beam(True)
                newStateBoard[move + 1].set_contaning_beam(True)
                newStateBoard[move + 2].set_contaning_beam(True)

            # Vertical Wall
            elif move + 34 <= 288:
                newStateBoard[move].set_contaning_beam(True)
                newStateBoard[move + 17].set_contaning_beam(True)
                newStateBoard[move + 34].set_contaning_beam(True)

            newPlayer1 = Player(state.get_player1().get_player_number(), state.get_player1().get_square_number(), 1,
                                newStateBoard)
            newPlayer2 = Player(state.get_player2().get_player_number(), state.get_player2().get_square_number(), 1,
                                newStateBoard)
            newPlayer1.set_num_of_walls(state.get_player1().get_num_of_walls())
            newPlayer2.set_num_of_walls(state.get_player2().get_num_of_walls())
            newState = GameState(newPlayer1, newPlayer2, newStateBoard)
            return newState


def minimaxAlphaBeta(state, depth, alpha, beta, maxPlayer, heuristicMaker):
    isGameOver = win(state.get_player1()) or win(state.get_player2())

    if depth == 0 or isGameOver:
        state.set_utility_value(heuristic(state, heuristicMaker))

        return state.get_utility_value()

    # player one is max player
    if maxPlayer:
        # merging moving wall and moving a player as "actions"
        # print("max")
        actions = []
        newPlayer1 = Player(state.get_player1().get_player_number(), state.get_player1().get_square_number(), 1,
                            deepcopy(state.get_state_board()))
        newPlayer1.set_num_of_walls(state.get_player1().get_num_of_walls())
        actions = get_valid_moves(state.get_state_board(), newPlayer1)
        if newPlayer1.numberOfWalls != 0:
            actions.extend(
                get_valid_wall_moves(state.get_state_board(), state.get_player1(), state.get_player2(), True))
            # print("all actions: " , actions)
        maxEval = initialMaxEval
        for move in actions:
            # making new state based on child :
            # print("move: " , move)
            newState = make_result(state, move, newPlayer1, state.get_player1().get_player_number())
            if newState is not None and not exploredSetPlayer1.__contains__(tuple(newState.get_state_board())):

                exploredSetPlayer1.add(tuple(newState.get_state_board()))
                eval = minimaxAlphaBeta(newState, depth - 1, alpha, beta, False, heuristicMaker)

                if eval > maxEval:
                    state.nextMove = move
                    maxEval = eval
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

        return maxEval

    else:
        # merging moving wall and moving a player as "actions"
        # print("min")
        actions = []
        # print('player 1 place: ', state.get_player1().get_square_number())
        # print('player 2 place: ', state.get_player2().get_square_number())
        newPlayer2 = Player(state.get_player2().get_player_number(), state.get_player2().get_square_number(), 1,
                            deepcopy(state.get_state_board()))
        newPlayer2.set_num_of_walls(state.get_player2().get_num_of_walls())
        actions = get_valid_moves(state.get_state_board(), newPlayer2)
        if newPlayer2.numberOfWalls != 0:
            actions.extend(
                get_valid_wall_moves(state.get_state_board(), state.get_player1(), state.get_player2(), False))
            # print("all actions: " , actions)
        minEval = initialMinEval
        for move in actions:
            # print("move: " , move)
            newState = make_result(state, move, newPlayer2, state.get_player1().get_player_number())
            if newState is not None and not exploredSetPlayer2.__contains__(tuple(newState.get_state_board())):

                exploredSetPlayer2.add(tuple(newState.get_state_board()))
                eval = minimaxAlphaBeta(newState, depth - 1, alpha, beta, True, heuristicMaker)

                if eval < minEval:
                    minEval = eval
                    state.nextMove = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return minEval


def best_next_move(state, player, heuristicMaker):
    exploredSetPlayer1.clear()
    exploredSetPlayer2.clear()
    minimaxAlphaBeta(state, miniMaxDepth, initialAlpha, initialBeta, player, heuristicMaker)
    return state.nextMove


def get_valid_wall_moves(stateBoard, p1, p2, maxPlayer):
    validWalls = []
    possibleValidWall = []

    if maxPlayer is not True:
        currentPlace_x = int(p1.get_square_number() / 17)
        currentPlace_y = p1.get_square_number() % 17
        # for player 2 :

        for i in range(-2 * wallRangeCheck, 2 + 1):
            for j in range(-2 * wallRangeCheck, 2 * wallRangeCheck + 1):
                if (0 <= currentPlace_x + i <= 16 and 0 <= currentPlace_y + j <= 16):
                    possibleValidWall.append((currentPlace_x + i) * 17 + (currentPlace_y + j))


    else:
        currentPlace_x = int(p2.get_square_number() / 17)
        currentPlace_y = p2.get_square_number() % 17
        # for player 1:
        for i in range(-2, 2 * wallRangeCheck + 1):
            for j in range(-2 * wallRangeCheck, 2 * wallRangeCheck + 1):
                if (0 <= currentPlace_x + i <= 16 and 0 <= currentPlace_y + j <= 16):
                    possibleValidWall.append((currentPlace_x + i) * 17 + (currentPlace_y + j))

    for wall in possibleValidWall:

        if int(wall / 17) % 2 == 1 and int(wall % 17) % 2 == 1:
            continue

        # Horizontal
        if int(wall / 17) % 2 == 1 and wall + 2 <= 288 and wall >= 0 and wall % 17 != 16:
            if stateBoard[wall].get_contaning_beam() == False and stateBoard[
                wall + 1].get_contaning_beam() == False and stateBoard[
                wall + 2].get_contaning_beam() == False:
                stateBoard[wall].set_contaning_beam(True)
                stateBoard[wall + 1].set_contaning_beam(True)
                stateBoard[wall + 2].set_contaning_beam(True)
                if check_for_not_stulking(p1, stateBoard) == True and check_for_not_stulking(p2, stateBoard) == True:
                    validWalls.append(wall)
                stateBoard[wall].set_contaning_beam(False)
                stateBoard[wall + 1].set_contaning_beam(False)
                stateBoard[wall + 2].set_contaning_beam(False)
        # Vertical
        elif int(wall / 17) % 2 == 0 and wall % 2 == 1 and wall + 34 <= 288 and wall >= 0:
            if stateBoard[wall].get_contaning_beam() == False and stateBoard[
                wall + 17].get_contaning_beam() == False and stateBoard[
                wall + 34].get_contaning_beam() == False:
                stateBoard[wall].set_contaning_beam(True)
                stateBoard[wall + 17].set_contaning_beam(True)
                stateBoard[wall + 34].set_contaning_beam(True)
                if check_for_not_stulking(p1, stateBoard) == True and check_for_not_stulking(p2, stateBoard) == True:
                    validWalls.append(wall)
                stateBoard[wall].set_contaning_beam(False)
                stateBoard[wall + 17].set_contaning_beam(False)
                stateBoard[wall + 34].set_contaning_beam(False)
    return validWalls


def get_valid_moves(state, player):
    currentSquare = player.get_square_number()
    validMoves = []
    # LEFT
    if currentSquare - 2 >= 0:
        nextSquare = currentSquare - 2
        if state[currentSquare - 1].get_contaning_beam() == False and (currentSquare % 17) != 0:
            if state[nextSquare].get_contaning_beam() == False:
                validMoves.append(nextSquare)
            else:
                if state[nextSquare - 1].get_contaning_beam() == True or nextSquare % 17 == 0:
                    if nextSquare + 34 <= 288:
                        if state[nextSquare + 34].get_contaning_beam() == False and state[
                            nextSquare + 17].get_contaning_beam() == False:
                            validMoves.append(nextSquare + 34)
                    if nextSquare - 34 >= 0:
                        if state[nextSquare - 34].get_contaning_beam() == False and state[
                            nextSquare - 17].get_contaning_beam() == False:
                            validMoves.append(nextSquare - 34)
                elif state[nextSquare - 2].get_contaning_beam() == False:
                    validMoves.append(nextSquare - 2)

    # RIGHT
    if (currentSquare % 17) != 16:
        nextSquare = currentSquare + 2
        if state[currentSquare + 1].get_contaning_beam() == False:
            if state[nextSquare].get_contaning_beam() == False:
                validMoves.append(nextSquare)
            else:
                if nextSquare + 1 <= 288 and (
                        state[nextSquare + 1].get_contaning_beam() == True or nextSquare % 17 == 16):
                    if nextSquare + 34 <= 288:
                        if state[nextSquare + 34].get_contaning_beam() == False and state[
                            nextSquare + 17].get_contaning_beam() == False:
                            validMoves.append(nextSquare + 34)
                    if nextSquare - 34 >= 0:
                        if state[nextSquare - 34].get_contaning_beam() == False and state[
                            nextSquare - 17].get_contaning_beam() == False:
                            validMoves.append(nextSquare - 34)
                elif nextSquare + 2 <= 288 and state[nextSquare + 2].get_contaning_beam() == False:
                    validMoves.append(nextSquare + 2)

    # UP
    if currentSquare - 34 >= 0:
        nextSquare = currentSquare - 34
        if state[currentSquare - 17].get_contaning_beam() == False:
            if state[nextSquare].get_contaning_beam() == False:
                validMoves.append(nextSquare)
            else:
                if nextSquare - 34 >= 0:
                    if state[nextSquare - 17].get_contaning_beam() == False and state[
                        nextSquare - 34].get_contaning_beam() == False:
                        validMoves.append(nextSquare - 34)
                    else:
                        if nextSquare - 2 >= 0:
                            if state[nextSquare - 1].get_contaning_beam() == False and state[
                                nextSquare - 2].get_contaning_beam() == False:
                                validMoves.append(nextSquare - 2)
                        if (nextSquare) % 17 != 16:
                            v = state[nextSquare + 2].get_contaning_beam() == False and state[
                                nextSquare + 1].get_contaning_beam() == False
                            if (v):
                                validMoves.append(nextSquare + 2)
    # DOWN
    if currentSquare + 34 <= 288:
        nextSquare = currentSquare + 34
        if state[currentSquare + 17].get_contaning_beam() == False:
            if state[nextSquare].get_contaning_beam() == False:
                validMoves.append(nextSquare)
            else:
                if nextSquare + 34 <= 288:
                    if state[nextSquare + 17].get_contaning_beam() == False and state[
                        nextSquare + 34].get_contaning_beam() == False:
                        validMoves.append(nextSquare + 34)
                    else:
                        if nextSquare - 2 >= 0:
                            if state[nextSquare - 1].get_contaning_beam() == False and state[
                                nextSquare - 2].get_contaning_beam() == False:
                                validMoves.append(nextSquare - 2)
                        if (nextSquare) % 17 != 16:
                            v = state[nextSquare + 2].get_contaning_beam() == False and state[
                                nextSquare + 1].get_contaning_beam() == False
                            if (v):
                                validMoves.append(nextSquare + 2)
    return validMoves

    # -- PlayerMoves --


def is_valid_move(player, nextSquare, board):
    moveList = get_valid_moves(board, player)
    for i in moveList:
        if i == nextSquare:
            return True
    return False


def win(player):
    if player.get_player_number() == 1:
        for i in range(16 * 17, 16 * 18 + 1, 2):
            if i == player.get_square_number():
                # print(player.get_square_number())
                return True

    if player.get_player_number() == 2:
        for i in range(0, 17, 2):
            if i == player.get_square_number():
                # print("player 2 won")
                return True

    if player.get_player_number() == 4:
        for i in range(0, 16 * 17 + 1, 34):
            if player.get_square_number() == i:
                # print("player 4 won")
                return True

    if player.get_player_number() == 3:
        for i in range(16, 16 * 18 + 1, 34):
            if player.get_square_number() == i:
                # print("player 3 won")
                return True


def check_for_not_stulking(player, stateBoard):
    if win(player):
        return True
    exoloredSet = set()
    exoloredSet.add(player.get_player_number())
    frontier = [player]
    while True:
        if len(frontier) == 0:
            return False
        node = frontier.pop()

        for i in get_valid_moves(stateBoard, node):
            if not exoloredSet.__contains__(i):
                exoloredSet.add(i)
                temp = Player(player.get_player_number(), i, 2, stateBoard)
                if win(temp):
                    return True
                frontier.append(temp)


def bfs(player, gameState):
    exoloredSet = set()
    exoloredSet.add(player.get_square_number())
    frontier = deque()
    frontier.append(player)
    parent = dict()
    dist = dict()
    parent[player.get_square_number()] = None
    dist[player.get_square_number()] = 0
    result_dist = 100000000000
    dest_node = 0
    while len(frontier) != 0:
        node = frontier.popleft()
        node_number = node.get_square_number()
        if win(node):
            result_dist = dist[node_number]
            dest_node = node_number
            break

        for i in get_valid_moves(gameState.get_state_board(), node):
            if not exoloredSet.__contains__(i):
                exoloredSet.add(i)
                temp = Player(player.get_player_number(), i, 2, gameState.get_state_board())
                parent[temp.get_square_number()] = node_number
                dist[temp.get_square_number()] = dist[node_number] + 1
                frontier.append(temp)
    path = []
    while dest_node != 0 and dest_node != None:
        path.append(dest_node)
        dest_node = parent[dest_node]
    return path


def show_valid_moves(player, window, board):
    if player.get_player_number() == 1:
        color = player1moves
    if player.get_player_number() == 2:
        color = player2moves
    if player.get_player_number() == 3:
        color = player3moves
    if player.get_player_number() == 4:
        color = player4moves

    validMoves = get_valid_moves(board, player)

    for i in validMoves:
        pygame.draw.rect(window, color, board[i].get_rect())
    return validMoves