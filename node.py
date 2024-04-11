from collections import defaultdict

class Node:
    next_node_id = 0
    visits = defaultdict(lambda: 0)

    def reset() -> None:
        Node.next_node_id = 0
        Node.visits = defaultdict(lambda: 0)

    def __init__(self, state, parent = None, action = None, reward: float = .0):
        self.state = state
        self.parent = parent
        self.children = set()

        self.reward = reward
        self.action = action

        self.id = Node.next_node_id
        Node.next_node_id += 1

    def is_root(self) -> bool: return self.get_parent() == None

    def get_id(self) -> int: return self.id
    def get_visits(self) -> int: return Node.visits[self.get_state()]
    def get_reward(self) -> float: return self.reward

    def get_parent(self): return self.parent
    def get_children(self) -> set: return self.children
    def get_generation(self) -> int:
        node = self
        generation = 0
        while node.get_parent() != None:
            node = node.get_parent()
            generation += 1
        return generation

    def get_state(self): return self.state
    def get_action(self): return self.action

    def increase_visits(self, amount: int = 1) -> None: Node.visits[self.get_state()] += amount
    def increase_reward(self, amount: float = 1) -> None: self.reward += amount

    def set_action(self, action) -> None: self.action = action
    def set_children(self, children: set) -> None: self.children = children
