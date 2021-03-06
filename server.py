import os
import random

import cherrypy
from variables import Variables

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


def get_board(data):
    board = []
    for i in range(data.width + 2):
        board.append([])
        for j in range(data.height + 2):
            if i == 0 or i == data.width+1:
                board[i].append('W')
            elif j == 0 or j == data.height+1:
                board[i].append('W')
            else:
                board[i].append(0)

    for snake in data.snakes:
        for bodypart in snake["body"][:-1]:
            board[bodypart["x"]][bodypart["y"]] = 'S'

    return board


def get_closest_food(data):
    best_food = {}
    smallest_dist = 1000
    for food in data.food:
        dist = abs(food["x"] - data.you_x) + abs(food["y"] - data.you_y)
        if dist < smallest_dist:
            best_food = food
            dist = smallest_dist

    return best_food


def seek_food(data):
    food = get_closest_food(data)
    moves = get_valid_moves(data)

    dx = food["x"] - data.you_x
    dy = food["y"] - data.you_y

    food_moves = []
    if dx > 0:
        food_moves.append("right")
    elif dx < 0:
        food_moves.append("left")

    if dy > 0:
        food_moves.append("up")
    elif dy < 0:
        food_moves.append("down")

    for move in food_moves:
        if move in moves:
            return move

    return random.choice(moves)


def move_randomly(data):
    valid_moves = get_valid_moves(data)
    direction = get_direction(data)

    if direction in valid_moves:
        if random.random() < 0.75:
            move = direction
        else:
            move = random.choice(valid_moves)
    else:
        move = random.choice(valid_moves)

    return move


def get_direction(data):
    body_x = data.you_body[1]["x"]
    body_y = data.you_body[1]["y"]
    head_x = data.you_x
    head_y = data.you_y

    if body_x < head_x:
        return "right"
    elif head_x < body_x:
        return "left"
    elif body_y < head_y:
        return "up"
    else:
        return "down"


def get_valid_moves(data):
    board = get_board(data)
    valid_moves = []

    if data.you_x != 0:
        if board[data.you_x - 1][data.you_y] == 0:
            valid_moves.append("left")

    if data.you_x != data.width - 1:
        if board[data.you_x + 1][data.you_y] == 0:
            valid_moves.append("right")

    if data.you_y != 0:
        if board[data.you_x][data.you_y - 1] == 0:
            valid_moves.append("down")

    if data.you_y != data.height - 1:
        if board[data.you_x][data.you_y + 1] == 0:
            valid_moves.append("up")

    if len(valid_moves) == 0:
        return ["up"]
    else:
        return valid_moves


class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            "apiversion": "1",
            "author": "Chooboo",  # TODO: Your Battlesnake Username
            "color": "#800000",  # TODO: Personalize
            "head": "caffeine",  # TODO: Personalize
            "tail": "skinny",  # TODO: Personalize
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        data = cherrypy.request.json

        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        data_raw = cherrypy.request.json
        data = Variables(data_raw)

        if data.you_health < 55:
            move = seek_food(data)
        else:
            move = move_randomly(data)

        print(f"MOVE: {move}")
        return {"move": move,
                "taunt": "hello"}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        print("END")
        return "ok"


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")), }
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
