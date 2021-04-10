import random
import string
import pygame
import random
from param import *
from board import *
from sprites import *
from ai_player import *
from collections import deque
from copy import deepcopy
from itertools import combinations


class Agent:
    def __init__(self, length):
        self.DNA = []
        for i in range(0, length):
            self.DNA.append(random.uniform(0.0, 1.0))
        self.fitness = 0

    def __str__(self):
        return 'DNA: ' + str(self.DNA) + ' | Fitness: ' + str(self.fitness)


population = initialNumberOfPopulation
generations = initialNumberOfGenerations
numberOfLeagues = initialNumberOfleagues


def geneticAlgorithm():
    agents = init_agents(numberOfHeuristicComponents)

    log = open("log.txt","w")
    log.write("")
    log.close()

    for generation in range(generations):
        print('Generation: ' + str(generation) + '\n')
        log = open("log.txt", "a")
        log.write('Generation: ' + str(generation) + '\n')
        log.close()

        agents = fitness(agents)
        agents = selection(agents)
        agents = crossover(agents)
        agents = mutation(agents)

    finalAgent = agents[0]
    finalc1 = finalAgent.DNA[0]
    finalc2 = finalAgent.DNA[1]
    finalc3 = finalAgent.DNA[2]
    finalc4 = finalAgent.DNA[3]


def init_agents(length):
    return [Agent(length) for __ in range(population)]


def fitness(agents):
    log = open("log.txt", "a")
    log.write("im in fitness bro" + '\n')
    log.close()
    # TO DO
    # making three leagues :
    for i in range(0, numberOfLeagues):
        players = agents[i * int(population / numberOfLeagues): i * int(population / numberOfLeagues) + numberOfLeagues]
        players = list(combinations(players, 2))
        play_game(players)

    return agents


def selection(agents):
    log = open("log.txt", "a")
    log.write("im in selection bro" + '\n')
    log.close()
    agents = sorted(agents, key=lambda agent: agent.fitness, reverse=True)
    # print all agents
    log = open("log.txt", "a")
    log.write('\n'.join(map(str, agents)))
    log.close()
    # select top 20 %
    agents = agents[:int(0.2 * len(agents))]
    return agents


def crossover(agents):
    offspring = []
    log = open("log.txt", "a")
    log.write("crossovering bro" + '\n')
    log.close()
    for _ in range(int((population - len(agents)) / 2)):
        parent1 = random.choice(agents)
        parent2 = random.choice(agents)
        child1 = Agent(numberOfHeuristicComponents)
        child2 = Agent(numberOfHeuristicComponents)

        split = random.randint(0, numberOfHeuristicComponents)
        child1.DNA = parent1.DNA[0:split] + parent2.DNA[split:numberOfHeuristicComponents]
        child2.DNA = parent2.DNA[0:split] + parent1.DNA[split:numberOfHeuristicComponents]

        offspring.append(child1)
        offspring.append(child2)

    agents.extend(offspring)

    return agents


def mutation(agents):
    log = open("log.txt", "a")
    log.write("mutating niggas" + '\n')
    log.close()
    for agent in agents:
        for idx in range(0, numberOfHeuristicComponents):
            if random.uniform(0.0, 1.0) <= 0.1:
                agent.DNA[idx] = random.uniform(0.0, 1.0)
    return agents


rungen = False


def play_game(players):
    for game in players:
        heuristic1 = HeuristicMaker(game[0].DNA[0], game[0].DNA[1], game[0].DNA[2], game[0].DNA[3])
        heuristic2 = HeuristicMaker(game[1].DNA[0], game[1].DNA[1], game[1].DNA[2], game[1].DNA[3])
        rungen = True

        board = []
        walls = []
        set_board(board)

        pygame.init()

        clock = pygame.time.Clock()
        all_sprites = pygame.sprite.Group()
        player1 = Player(1, 8, 2, board)
        player2 = Player(2, 280, 2, board)

        all_sprites.add(player1)
        all_sprites.add(player2)
        board[8].set_contaning_beam(True)
        board[280].set_contaning_beam(True)

        for i in range(1, 11):
            walls.append(WallSprite(1, i, 1, 2))
            walls.append(WallSprite(1, i, 2, 2))

        for wall in walls:
            all_sprites.add(wall)

        window = pygame.display.set_mode((windowWidth, windowHeight))
        pygame.display.set_caption("Quoridor")

        player_draging = False
        wall_draging = False
        show_valid_player_moves = 0
        mode_ai_turn = 1
        numberOfActions = 0
        while bool(rungen):

            pygame.time.delay(100)

            if mode_ai_turn == 1:
                AI_move_VS_AI(player1, player2, board, walls, player1, player2, heuristic1, heuristic2)
                mode_ai_turn = 0
                numberOfActions = numberOfActions + 1
            else:
                AI_move_VS_AI(player2, player1, board, walls, player1, player2, heuristic1, heuristic2)
                mode_ai_turn = 1
                numberOfActions = numberOfActions + 1
            # winning
            if win(player1):
                print("Player1 won!")
                game[0].fitness = game[0].fitness + 1

            if win(player2):
                print("Player2 won!")
                game[0].fitness = game[0].fitness + 1

            if win(player1) or win(player2) or numberOfActions >= 45:
                if numberOfActions >= 45:
                    finalGameState = GameState(player1, player2, board)
                    path1 = len(bfs(player1, finalGameState))
                    path2 = len(bfs(player2, finalGameState))
                    log = open("log.txt", "a")
                    log.write('time limit reached! path1: ' + str(path1) + ', path2: ' + str(path2) + '\n')
                    log.close()

                    if path1 > path2:
                        game[0].fitness = game[0].fitness + 1

                    else:
                        game[1].fitness = game[1].fitness + 1

                rungen = False
                heuristic1 = None
                heuristic2 = None

            pygame.draw.rect(window, backGroundColor, (0, 0, windowWidth, windowHeight))
            draw_board(board, window)

            all_sprites.update()
            all_sprites.draw(window)

            pygame.display.update()

    # rungen = True


def AI_move_VS_AI(player, opp, board, walls, player1, player2, heuristic1, heuristic2):
    newPlayer1 = Player(player.get_player_number(), player.get_square_number(), 1, deepcopy(board))
    newPlayer2 = Player(opp.get_player_number(), opp.get_square_number(), 1, deepcopy(board))
    newPlayer1.set_num_of_walls(player.get_num_of_walls())
    newPlayer2.set_num_of_walls(opp.get_num_of_walls())
    currentState = GameState(newPlayer1, newPlayer2, deepcopy(board))
    if newPlayer1.get_player_number() == 1:
        action = best_next_move(currentState, newPlayer1, heuristic1)
    if newPlayer1.get_player_number() == 2:
        action = best_next_move(currentState, newPlayer1, heuristic2)

    # print("best : ", action)
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
                i.rect.x = board[i.get_square_number()].get_rect().x
                i.rect.y = board[i.get_square_number()].get_rect().y
                if i.get_player_number() == 1:
                    player1.set_num_of_walls(player1.numberOfWalls - 1)
                if i.get_player_number() == 2:
                    player2.set_num_of_walls(player2.numberOfWalls - 1)
                break


if __name__ == '__main__':
    geneticAlgorithm()
