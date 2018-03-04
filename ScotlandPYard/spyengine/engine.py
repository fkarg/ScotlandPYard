from numpy.random import choice

from .humandetective import HumanDetective
from .humanmrx import HumanMrX


class IllegalMoveException(Exception):
    pass


class GameEngine():
    def __init__(self, spymap, num_detectives=4):
        self.spymap = spymap
        self.graph = spymap.graph
        self.players = [HumanDetective() for i in range(num_detectives)]
        self.turn = 0
        for detective in self.players:
            detective.set_location(choice(self.graph.nodes()))

        self.mrx = HumanMrX(num_players=num_detectives)
        self.players.append(self.mrx)

    def get_game_state(self):
        state = {
            "players_state": [player.get_info() for player in self.players],
            "turn": self.turn
        }
        return state

    def get_valid_nodes(self, player_name, ticket):
        player = None
        for p in self.players:
            if p.name == player_name:
                player = p
                break
        if player is None: return []

        valid_nodes = []
        for u, v, tick in self.graph.edges(nbunch=player.location, data='ticket'):
            if tick == ticket and player.tickets[ticket] > 0:
                valid_nodes.append(v)

        print("Player now at: {}".format(player.location.nodeid))
        print("Available moves by {}: ".format(ticket))
        print([n.nodeid for n in valid_nodes])

        return valid_nodes
