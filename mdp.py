class MDP:
    """
    Markov Decision Process (MDP) is a mathematical framework for modeling decision-making
    in situations where outcomes are partly random and partly under the control of a decision-maker. 
    It provides a formalism for modeling sequential decision-making problems where an agent interacts
    with an environment. MDPs are characterized by states, actions, transition probabilities,
    and rewards. The agent selects actions based on the current state and aims to maximize the
    cumulative rewards over time.

    For more detailed information about Markov Decision Process (MDP), you can visit the Wikipedia page:
    https://en.wikipedia.org/wiki/Markov_decision_process

    Args:
        get_actions (function): A function that returns the possible actions for a given state.
        state_analysis (function): A function that analyzes the state and returns whether it's terminal or not.
        execute (function): A function that executes an action in the environment and returns the resulting state.
        qfunction (function): A function representing the Q-function used for policy evaluation.
    
    Attributes:
        _get_actions (function): A function that returns the possible actions for a given state.
        state_analysis (function): A function that analyzes the state and returns whether it's terminal or not.
        execute (function): A function that executes an action in the environment and returns the resulting state.
        qfunction (function): A function representing the Q-function used for policy evaluation.
        action_type (None or str): Type of action, if any.

    Methods:
        get_actions(node): Returns the possible actions for a given state.
        non_terminal(node): Checks if the given state is non-terminal.
    """
    def __init__(self, get_actions, state_analysis, execute, qfunction):
        self._get_actions = get_actions
        self.state_analysis = state_analysis
        self.execute = execute
        self.qfunction = qfunction
        self.action_type = None

    def get_actions(self, node):
        """Returns the possible actions for a given state."""
        return self._get_actions(node, self.action_type)

    def non_terminal(self, node):
        """Checks if the given state is non-terminal."""
        return not self.state_analysis(node)
