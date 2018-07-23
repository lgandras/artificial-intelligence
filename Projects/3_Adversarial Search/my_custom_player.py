
from sample_players import DataPlayer
import math, random, time
from isolation import StopSearch

class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.

    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.

    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """
    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller will be responsible
        for cutting off the function after the search time limit has expired.

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE: 
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        #print("Starting...")
        # update context
        if self.context is not dict:
            self.context = {
                'state': state,
                'action': None,
                'children': None,
                'explored': False,
                'currentBestChild': None,
                'visits': 0,
                'reward': 0
            }
        else:
            self.context = self.get_child_node_from_state(state)
        # search
        while True:
            #print("Searching...")
            node = self.search()
            #print(node['state'])
            #print(node['action'])
            try:
                self.queue.put(node['action'])
            except StopSearch:
                #print("Stop")
                return
            #print("Ended search.")

    def get_child_node_from_state(self, state):
        #print(self.__dict__)
        for childNode in self.get_children(self.context['currentBestChild']):
            if state == childNode['state']:
                #print(childNode)
                return childNode
        #print(self.__dict__)
        raise Exception("Unexpected state to visit: {}".format(state))

    def search(self):
        if not self.context['explored']:
            self.visit(self.context)
        self.context['currentBestChild'] = self.select(self.context, root=True)
        return self.context['currentBestChild']

    def visit(self, node):
        if node['state'].terminal_test():
            reward = self.calculate_reward(node['state'])
            node['explored'] = True
        elif node['children'] is None:
            childNode = self.select(node, root=False)
            reward = self.simulate(childNode)
            node['explored'] = all(childNode['explored'] for childNode in node['children'])
        else:
            childNode = self.select(node, root=False)
            reward = self.visit(childNode)
            node['explored'] = all(childNode['explored'] for childNode in node['children'])

        node['visits'] += 1
        node['reward'] += reward
        return reward

    def select(self, node, root=True):
        bestNode = None
        bestUcb1 = None
        for childNode in self.get_children(node):
            # from the root, we want the best instead of exploring the optimal new path
            if childNode['explored'] and not root:
                continue
            if 0 == childNode['visits']:
                bestNode = childNode
                break
            ucb1 = childNode['reward'] / childNode['visits'] + (0 if root else 1) * math.sqrt(2 * math.log(childNode['visits']) / float(node['visits']))
            if bestUcb1 is None or bestUcb1 < ucb1:
                bestNode = childNode
                bestUcb1 = ucb1
        return bestNode

    def get_children(self, node):
        if node['children'] is None:
            node['children'] = []
            actions = node['state'].actions()
            random.shuffle(actions)
            for action in actions:
                node['children'].append({
                    'state': node['state'].result(action),
                    'action': action,
                    'children': None,
                    'explored': False,
                    'currentBestChild': None,
                    'visits': 0,
                    'reward': 0
                })
        return node['children']

    def simulate(self, node):
        state = node['state']
        while not state.terminal_test():
            state = state.result(random.choice(state.actions()))
        return self.calculate_reward(state)

    def calculate_reward(self, state):
        player = self.context['state'].player()
        #print(state)
        val = len(state.liberties(state.locs[player])) - len(state.liberties(state.locs[player ^ 1]))
        #print("Val={}".format(val))
        return val

    #@staticmethod
    #def calculate_reward(state, player):
    #    return len(state.liberties(state.locs[player]))

"""
    @staticmethod
    def calculate_reward(state, player):
        print(state)
        val = 1 if 0 < state.utility(player) else 0
        print("Val={}".format(val))
        return val
"""