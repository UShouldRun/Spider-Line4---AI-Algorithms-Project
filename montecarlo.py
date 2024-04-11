from objects import Node
from time import time
from copy import deepcopy
from random import choice
from math import sqrt, log
import networkx as nx
import matplotlib.pyplot as plt

class MCTS:

    """
    Class for Monte Carlo Tree Search (MCTS) algorithm.

    Attributes:
        root_state: The initial state of the MDP.
        delta_time: The time limit for search in seconds.
        cp: The "computer power" limit.
        mdp: The Markov Decision Process (MDP) environment.

    Methods:
        __init__(root, delta_time, max_nodes, mdp): Initializes the MCTS object.
        reset(): Resets the MCTS object.
        get_start() -> int: Returns the start time of the search.
        get_delta_time() -> int: Returns the time limit for search.
        get_time() -> int: Returns the current time.
        get_cp() -> int: Returns the "computer power" limit.
        get_explored_children() -> dict[Node]: Returns the dictionary of explored children.
        resources_left(time, comp_power) -> bool: Checks if resources are left for search.
        create_root_node(state, action) -> Node: Creates the root node.
        find_direct_children(node) -> list[Node]: Finds the direct children of a node.
        find_random_direct_child(node) -> Node: Finds a random direct child of a node.
        uct_select(node, key) -> Node: Selects a child node using UCT algorithm.
        select(starting_node) -> Node: Finds an unexplored descendent of a node.
        expand(node) -> None: Expands the children of a node.
        backpropagate(node, reward) -> None: Backpropagates the reward information in the tree.
        simulate(starting_node) -> float: Simulates a certain universe from a starting branch (node) state.
        mcts(root) -> Node: Runs the MCTS algorithm.
        watch_stats(root) -> None: Prints statistics of the MCTS search.
        draw_graph(root) -> None: Draws the tree graph.
    """
    
    def __init__(self, root, delta_time: int, max_nodes: int, uct_const: int, mdp) -> None:
        self.root_state = root
        self.delta_time, self.cp = delta_time, max_nodes
        self.uct_const = uct_const
        self.mdp = mdp
        self.reset()

    def reset(self):
        self.explored_children = dict()
        self.start = 0
        Node.reset()

    def get_start(self) -> int: return self.start
    def get_delta_time(self) -> int: return self.delta_time
    def get_time(self) -> int: return time()
    def get_cp(self) -> int: return self.cp
    def get_uct_const(self) -> int: return self.uct_const
    def get_explored_children(self) -> dict[Node]: return self.explored_children

    def resources_left(self, time: int, comp_power: int): return time < self.get_start() + self.get_delta_time() and comp_power <= self.get_cp()

    def create_root_node(self, state, action) -> Node: return Node(state, None, action)
    def find_direct_children(self, node) -> list[Node]:
        return [self.mdp.execute(node, action) for action in self.mdp.get_actions(node)]
    def find_random_direct_child(self, node) -> Node:
        if node.get_children(): return choice(list(node.get_children()))
        children = self.find_direct_children(node)
        if not children: return
        return choice(children)

    def uct_select(self, node: Node, key: bool = False) -> Node:
        '''Select a child of node, balancing exploration & exploitation'''
        def uct(node) -> float:
            if node.get_parent().get_visits() == 0: raise ValueError("Parent node has 0 visits")

            n_parent = node.get_parent().get_visits()
            n_i = node.get_visits()

            if n_i == 0: return float("inf")
            v_i = node.get_reward()/n_i

            if self.get_uct_const() > 0:
                if n_i > 1: return v_i + self.get_uct_const() * sqrt(log(n_parent)/log(n_i))
                else: return float("inf")
            return v_i

        return max(node.get_children(), key=uct)

    def select(self, starting_node: Node) -> Node:
        '''Find an unexplored descendent of node'''
        path = []
        node = starting_node
        while True:
            path.append(node)
            if node not in self.get_explored_children() or not self.get_explored_children()[node]: return path[-1]
            unexplored = self.get_explored_children()[node] - self.get_explored_children().keys()
            if unexplored: return unexplored.pop()
            node = self.uct_select(node)

    def expand(self, node: Node) -> None:
        "Update the children dict with the children of node"
        if node in self.get_explored_children(): return  # already expanded
        if not node.get_children(): node.set_children(self.find_direct_children(node))
        self.explored_children[node] = node.get_children()
    
    def backpropagate(self, node: Node, reward: int) -> None:
        '''Restructure the tree according to the new rewards'''
        node.increase_visits()
        node.increase_reward(reward)
        if node.is_root(): return
        self.backpropagate(node.get_parent(), reward)

    def simulate(self, starting_node: Node) -> float:
        '''Simulate a certain universe from a starting branch (node) state'''
        node = self.find_random_direct_child(starting_node)
        while self.mdp.non_terminal(node):
            node1 = self.find_random_direct_child(node)
            if node1 == None: break
            node = node1
        return self.mdp.qfunction(node)

    def mcts(self, root: Node = None) -> Node:
        if root == None: root = self.create_root_node(deepcopy(self.root_state), (self.mdp.action_type, None))

        self.start = time()
        while self.resources_left(self.get_time(), len(self.get_explored_children().keys())):
            leaf = self.select(root)
            if self.mdp.non_terminal(leaf):
                self.expand(leaf)
                reward = self.simulate(leaf)
                self.backpropagate(leaf, reward)

        self.watch_stats(root)
        # self.draw_graph(root)
        return root

    def watch_stats(self, root) -> None:
        # for child in root.get_children(): print(f"Node {child.get_id()}/{child.get_generation()}: {child.get_reward()}/{child.get_visits()}")
        print(f"Total explored nodes: {len(self.get_explored_children().keys())}")
        print(f"Total created nodes: {Node.next_node_id - 1}")
        print("-----------------//----------------")

    def draw_graph(self, root) -> None:
        # Function to recursively add nodes and edges to the graph
        print("loading tree...")
        def add_nodes_edges(G, node, pos=None, level=0):
            if pos is None:
                pos = {node.get_id(): (level, 0)}

            for child in node.get_children():
                G.add_edge(node.get_id(), child.get_id())
                pos[child.get_id()] = (level + 1, len(G) + 1)
                if child.get_generation() < 2:
                    add_nodes_edges(G, counter, child, pos, level + 1)

        # Function to draw the tree graph
        def draw_tree(root):
            G = nx.DiGraph()
            add_nodes_edges(G, root)
            pos = nx.spring_layout(G, seed=42)
            nx.draw(G, pos, with_labels=True, arrows=True)
            plt.show()

        draw_tree(root)

