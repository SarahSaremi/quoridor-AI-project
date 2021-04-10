import pygame
import random
from param import *
from board import *
from sprites import *
from ai_player import *
from collections import deque
from copy import deepcopy

board = []


def is_wall_clicked():
    for i in walls:
        if i.rect.collidepoint(event.pos):
            return True
    return False


def set_moving_wall():
    for i in walls:
        if i.rect.collidepoint(event.pos):
            moving_wall = i
            break
    return moving_wall


def AI_move_VS_Human(currentBoard):
    newPlayer1 = Player(1, player1.get_square_number(), 1, currentBoard)
    newPlayer2 = Player(2, player2.get_square_number(), 1, currentBoard)
    newPlayer1.set_num_of_walls(player1.get_num_of_walls())
    newPlayer2.set_num_of_walls(player2.get_num_of_walls())
    currentState = GameState(newPlayer1, newPlayer2, currentBoard)
    action = best_next_move(currentState, newPlayer1, HeuristicMaker(finalc1, finalc2, finalc3, finalc4))

    print("best : ", action)
    if action % 2 == 0:
        player1.set_square_number(action, board)
        player1.rect.x = board[player1.get_square_number()].get_rect().x + 8
        player1.rect.y = board[player1.get_square_number()].get_rect().y + 8

    elif int(action / 17) % 2 == 0:
        for i in walls:
            if i.get_player_number() == 1 and i.get_square_number() == -1:
                i.set_square_number(action, board)
                i.rect.x = board[i.get_square_number()].get_rect().x
                i.rect.y = board[i.get_square_number()].get_rect().y
                player1.set_num_of_walls(player1.numberOfWalls - 1)
                break

    elif int(action / 17) % 2 == 1:
        for i in walls:
            if i.get_player_number() == 1 and i.get_square_number() == -1:
                i.rotate_wall(0, 0, 0, 0)
                i.set_square_number(action, board)
                print(i.get_voh())
                i.rect.x = board[i.get_square_number()].get_rect().x
                i.rect.y = board[i.get_square_number()].get_rect().y
                player1.set_num_of_walls(player1.numberOfWalls - 1)
                break


def AI_move_VS_AI(currentBoard, player, opp):
    print("AI turn", mode_ai_turn)
    newPlayer1 = Player(player.get_player_number(), player.get_square_number(), 1, currentBoard)
    newPlayer2 = Player(opp.get_player_number(), opp.get_square_number(), 1, currentBoard)
    newPlayer1.set_num_of_walls(player.get_num_of_walls())
    newPlayer2.set_num_of_walls(opp.get_num_of_walls())
    currentState = GameState(newPlayer1, newPlayer2, currentBoard)
    action = best_next_move(currentState, newPlayer1,  HeuristicMaker(1, 1, 1, 1))

    print("best : ", action)
    if action % 2 == 0:
        player.set_square_number(action, board)
        player.rect.x = board[player.get_square_number()].get_rect().x + 8
        player.rect.y = board[player.get_square_number()].get_rect().y + 8

    elif int(action / 17) % 2 == 0:
        for i in walls:
            if i.get_player_number() == player.get_player_number() and i.get_square_number() == -1:
                i.set_square_number(action, board)
                i.rect.x = board[i.get_square_number()].get_rect().x
                i.rect.y = board[i.get_square_number()].get_rect().y
                player.set_num_of_walls(player.numberOfWalls - 1)
                break

    elif int(action / 17) % 2 == 1:
        for i in walls:
            if i.get_player_number() == player.get_player_number() and i.get_square_number() == -1:
                i.rotate_wall(0, 0, 0, 0)
                i.set_square_number(action, board)
                print(i.get_voh())
                i.rect.x = board[i.get_square_number()].get_rect().x
                i.rect.y = board[i.get_square_number()].get_rect().y
                player1.set_num_of_walls(player1.numberOfWalls - 1)
                break


def is_valid_wall(nextSquare):
    if (int(nextSquare / 17) % 2 == 1 and (nextSquare % 17) % 2 == 0 and moving_wall.get_voh() == 0):
        if board[nextSquare].get_contaning_beam() == False and board[
            nextSquare + 1].get_contaning_beam() == False and \
                board[nextSquare + 2].get_contaning_beam() == False:
            return True
    elif ((nextSquare % 17) % 2 == 1 and moving_wall.get_voh() == 1):
        if (int(nextSquare / 17) % 2 == 1):
            return False
        else:
            if board[nextSquare].get_contaning_beam() == False and board[
                nextSquare + 17].get_contaning_beam() == False and board[
                nextSquare + 34].get_contaning_beam() == False:
                return True
    return False


print("select mode")
print("0) vs AI")
print("1) 2 player")
print("2) 4 player")
print("3) AI vs AI")

mode = int(input())

showPath = False
print("do you also want to see the shortest path to the goal?")
print("0) No")
print("1) Yes")
showPath = int(input())
if mode == 0:
    # playerNumber = (random.choice([1, 2]))
    playerNumber = 2
    if playerNumber == 1:
        print("AI starts")
    else:
        print("You start")
if mode == 1:
    playerNumber = (random.choice([1, 2]))
    print("player " + str(playerNumber) + " starts")

if mode == 2:
    playerNumber = (random.choice([1, 2, 3, 4]))
    print("player " + str(playerNumber) + " starts")

set_board(board)

pygame.init()

clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player1 = Player(1, 8, 2, board)
player2 = Player(2, 280, 2, board)

walls = []
# initialState :
currentState0 = GameState(player1, player2, deepcopy(board))
currentState = GameState(player1, player2, deepcopy(board))

if mode == 0:
    all_sprites.add(player1)
    all_sprites.add(player2)
    board[8].set_contaning_beam(True)
    board[280].set_contaning_beam(True)

    for i in range(1, 11):
        walls.append(WallSprite(1, i, 1, 2))
        walls.append(WallSprite(1, i, 2, 2))

if mode == 1 or mode == 3:
    all_sprites.add(player1)
    all_sprites.add(player2)
    board[8].set_contaning_beam(True)
    board[280].set_contaning_beam(True)

    for i in range(1, 11):
        walls.append(WallSprite(1, i, 1, 2))
        walls.append(WallSprite(1, i, 2, 2))

if mode == 2:
    player1 = Player(1, 8, 2, board)
    player2 = Player(2, 280, 2, board)
    player3 = Player(3, 136, 4, board)
    player4 = Player(4, 152, 4, board)
    board[8].set_contaning_beam(True)
    board[280].set_contaning_beam(True)
    board[136].set_contaning_beam(True)
    board[152].set_contaning_beam(True)

    for i in range(1, 11):
        if i <= 5:
            walls.append(WallSprite(1, i, 1, 4))
            walls.append(WallSprite(1, i, 2, 4))
        elif i <= 10:
            walls.append(WallSprite(0, i, 3, 4))
            walls.append(WallSprite(0, i, 4, 4))

    all_sprites.add(player1)
    all_sprites.add(player2)
    all_sprites.add(player3)
    all_sprites.add(player4)

for wall in walls:
    all_sprites.add(wall)

window = pygame.display.set_mode((windowWidth, windowHeight))
window0 = pygame.display.set_mode((windowWidth, windowHeight))

pygame.display.set_caption("Quoridor")

player_draging = False
wall_draging = False
show_valid_player_moves = 0
run = True
mode_ai_turn = 1

while bool(run):
    pygame.time.delay(100)
    if mode == 3:
        if mode_ai_turn == 1:
            AI_move_VS_AI(deepcopy(board), player1, player2)
            mode_ai_turn = 0
        else:
            AI_move_VS_AI(deepcopy(board), player2, player1)
            mode_ai_turn = 1
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                LEFT_CLICK = True
                # -- move player --
                if mode == 0:
                    if player2.rect.collidepoint(event.pos):
                        if playerNumber == 2:
                            moving_player = player2
                            show_valid_player_moves = 2
                            player_draging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = moving_player.rect.x - mouse_x
                            offset_y = moving_player.rect.y - mouse_y

                    elif player1.rect.collidepoint(event.pos):
                        print("Don't touch the AI")

                elif mode == 1:
                    if player1.rect.collidepoint(event.pos) or player2.rect.collidepoint(event.pos):
                        if player1.rect.collidepoint(event.pos):
                            if playerNumber == 1:
                                moving_player = player1
                                show_valid_player_moves = 1
                                player_draging = True
                                mouse_x, mouse_y = event.pos
                                offset_x = moving_player.rect.x - mouse_x
                                offset_y = moving_player.rect.y - mouse_y
                            else:
                                print("not your turn")

                        if player2.rect.collidepoint(event.pos):
                            if playerNumber == 2:
                                moving_player = player2
                                show_valid_player_moves = 2
                                player_draging = True
                                mouse_x, mouse_y = event.pos
                                offset_x = moving_player.rect.x - mouse_x
                                offset_y = moving_player.rect.y - mouse_y

                            else:
                                print("not your turn")

                elif mode == 2:
                    if player1.rect.collidepoint(event.pos) or player2.rect.collidepoint(
                            event.pos) or player3.rect.collidepoint(event.pos) or player4.rect.collidepoint(
                        event.pos):
                        if player1.rect.collidepoint(event.pos):
                            if playerNumber == 1:
                                moving_player = player1
                                show_valid_player_moves = 1
                                player_draging = True
                                mouse_x, mouse_y = event.pos
                                offset_x = moving_player.rect.x - mouse_x
                                offset_y = moving_player.rect.y - mouse_y
                            else:
                                print("not your turn")

                        if player2.rect.collidepoint(event.pos):
                            if playerNumber == 2:
                                moving_player = player2
                                show_valid_player_moves = 2
                                player_draging = True
                                mouse_x, mouse_y = event.pos
                                offset_x = moving_player.rect.x - mouse_x
                                offset_y = moving_player.rect.y - mouse_y
                            else:
                                print("not your turn")

                        if player3.rect.collidepoint(event.pos):
                            if playerNumber == 3:
                                moving_player = player3
                                show_valid_player_moves = 3
                                player_draging = True
                                mouse_x, mouse_y = event.pos
                                offset_x = moving_player.rect.x - mouse_x
                                offset_y = moving_player.rect.y - mouse_y
                            else:
                                print("not your turn")

                        if player4.rect.collidepoint(event.pos):
                            if playerNumber == 4:
                                moving_player = player4
                                show_valid_player_moves = 4
                                player_draging = True
                                mouse_x, mouse_y = event.pos
                                offset_x = moving_player.rect.x - mouse_x
                                offset_y = moving_player.rect.y - mouse_y
                            else:
                                print("not your turn")

                        mouse_x, mouse_y = event.pos
                        offset_x = moving_player.rect.x - mouse_x
                        offset_y = moving_player.rect.y - mouse_y

                        # -- move wall --
                if is_wall_clicked():
                    moving_wall = set_moving_wall()
                    if moving_wall.get_player_number() == playerNumber and moving_wall.get_square_number() == -1:
                        mouse_x, mouse_y = event.pos
                        offset_x = moving_wall.rect.x - mouse_x
                        offset_y = moving_wall.rect.y - mouse_y
                        wall_draging = True
                    else:
                        print("don't touch this wall!")

            if event.button == 3 and LEFT_CLICK and wall_draging:
                moving_wall.rotate_wall(mouse_x, offset_x, mouse_y, offset_y)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if player_draging:
                    for s in board:
                        if s.get_rect().collidepoint(event.pos):
                            newSquareNumber = s.get_number()
                            if (is_valid_move(moving_player, newSquareNumber, board)):
                                moving_player.set_square_number(newSquareNumber, board)
                                moving_player.rect.x = board[moving_player.get_square_number()].get_rect().x + 8
                                moving_player.rect.y = board[moving_player.get_square_number()].get_rect().y + 8
                                if mode == 0:
                                    AI_move_VS_Human(deepcopy(board))
                                if mode == 1:
                                    playerNumber = moving_player.get_player_number() % 2 + 1
                                if mode == 2:
                                    playerNumber = moving_player.get_player_number() % 4 + 1

                        else:
                            moving_player.rect.x = board[moving_player.get_square_number()].get_rect().x + 8
                            moving_player.rect.y = board[moving_player.get_square_number()].get_rect().y + 8
                    player_draging = False
                    show_valid_player_moves = 0
                    LEFT_CLICK = False

                if wall_draging:
                    for s in board:
                        if s.get_rect().collidepoint(event.pos):
                            newSquareNumber = s.get_number()
                            if (is_valid_wall(newSquareNumber)):
                                moving_wall.set_square_number(newSquareNumber, board)
                                placed_wall = True
                                moving_wall.rect.x = board[moving_wall.get_square_number()].get_rect().x
                                moving_wall.rect.y = board[moving_wall.get_square_number()].get_rect().y
                                if mode == 0:
                                    if check_for_not_stulking(player1, board) == False or check_for_not_stulking(
                                            player2, board) == False:
                                        if moving_wall.get_voh() != moving_wall.initial_voh():
                                            moving_wall.rotate_wall(mouse_x, offset_x, mouse_y, offset_y)
                                        moving_wall.set_square_number(-1, board)
                                        print("invalid wall placement")
                                        placed_wall = False
                                        moving_wall.rect.x = moving_wall.get_x()
                                        moving_wall.rect.y = moving_wall.get_y()

                                elif mode == 1:
                                    if check_for_not_stulking(player1, board) == False or check_for_not_stulking(
                                            player2, board) == False:
                                        if (moving_wall.get_voh() != moving_wall.initial_voh()):
                                            moving_wall.rotate_wall(mouse_x, offset_x, mouse_y, offset_y)
                                        moving_wall.set_square_number(-1, board)
                                        print("invalid wall placement")
                                        placed_wall = False
                                        moving_wall.rect.x = moving_wall.get_x()
                                        moving_wall.rect.y = moving_wall.get_y()
                                elif mode == 2:
                                    if check_for_not_stulking(player1, board) == False or check_for_not_stulking(
                                            player2, board) == False or check_for_not_stulking(
                                        player3, board) == False or check_for_not_stulking(
                                        player4, board) == False:
                                        if (moving_wall.get_voh() != moving_wall.initial_voh()):
                                            moving_wall.rotate_wall(mouse_x, offset_x, mouse_y, offset_y)
                                        moving_wall.set_square_number(-1, board)
                                        print("invalid wall placement")
                                        placed_wall = False
                                        moving_wall.rect.x = moving_wall.get_x()
                                        moving_wall.rect.y = moving_wall.get_y()

                                if placed_wall == True:

                                    if mode == 0:
                                        AI_move_VS_Human(deepcopy(board))

                                    if mode == 1:
                                        playerNumber = moving_wall.get_player_number() % 2 + 1

                                    if mode == 2:
                                        playerNumber = moving_wall.get_player_number() % 4 + 1

                            else:
                                if (moving_wall.get_voh() != moving_wall.initial_voh()):
                                    print("not valid")
                                    moving_wall.rotate_wall(mouse_x, offset_x, mouse_y, offset_y)
                                moving_wall.set_square_number(-1, board)
                                moving_wall.rect.x = moving_wall.get_x()
                                moving_wall.rect.y = moving_wall.get_y()

                    wall_draging = False

        elif event.type == pygame.MOUSEMOTION:
            if player_draging:
                mouse_x, mouse_y = event.pos
                moving_player.rect.x = mouse_x + offset_x
                moving_player.rect.y = mouse_y + offset_y
            if wall_draging:
                mouse_x, mouse_y = event.pos
                moving_wall.rect.x = mouse_x + offset_x
                moving_wall.rect.y = mouse_y + offset_y

    pygame.draw.rect(window, backGroundColor, (0, 0, windowWidth, windowHeight))
    draw_board(board, window)
    newPlayer1 = Player(1, player1.get_square_number(), 1, deepcopy(board))
    newPlayer2 = Player(2, player2.get_square_number(), 1, deepcopy(board))
    newState = GameState(newPlayer1, newPlayer2, deepcopy(board))
    if showPath == True:
        for i in bfs(player1, newState):
            pygame.draw.rect(window, (255, 255, 255), board[i].get_rect())

    if show_valid_player_moves == 1 or mode == 0:
        show_valid_moves(player1, window, board)
    if show_valid_player_moves == 2:
        show_valid_moves(player2, window, board)
    if show_valid_player_moves == 3:
        show_valid_moves(player3, window, board)
    if show_valid_player_moves == 4:
        show_valid_moves(player4, window, board)
    all_sprites.update()
    all_sprites.draw(window)

    # winning
    if win(player1):
        print("Player1 won!")
        run = False
    if win(player2):
        print("Player2 won!")
        run = False
    if mode == 2:
        if win(player3):
            print("Player3 won!")
            run = False
        if win(player4):
            print("Player4 won!")
            run = False

    pygame.display.update()