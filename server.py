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
  for i in range(data.width):
    board.append([])
    for j in range(data.height):
      board[i].append(0)

  for snake in data.snakes:
    for bodypart in snake["body"][:-1]:
      board[bodypart["x"]][bodypart["y"]] = 'S'

  return board


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
            "author": "",  # TODO: Your Battlesnake Username
            "color": "#666666",  # TODO: Personalize
            "head": "default",  # TODO: Personalize
            "tail": "default",  # TODO: Personalize
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

        valid_moves = get_valid_moves(data)
        direction = get_direction(data)
        if direction in valid_moves:
          if random.random() < 0.7:
            move = direction
          else:
            move = random.choice(valid_moves)            
        else:
          move = random.choice(valid_moves)

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
