# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

class Node: #Linked List
    def __init__(self, state, prev, action, priority=0):
        self.state = state #vị trí node
        self.prev = prev #node trc do liên kết với nó
        self.action = action #node có thể đi qua từ node trước đó
        self.priority = priority
    def __repr__(self):
        return "State: {0}, Action: {1}".format(self.state, self.action)

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    closed = set() #lưu lại danh sách các ô đã đi qua
    fringe = util.Stack() # Tạo ra 1 danh sách lưu các ô ngã rẽ có thể đi được.
    # Các ô trong danh sách sẽ tìm đường đến khi không đi được nữa sẽ quay lại nhánh rẽ
    fringe.push(Node(problem.getStartState(), None, None)) #Điểm bắt đầu = vị trí của Pacman
    while fringe.isEmpty() is not True:
        node = fringe.pop() # Lần lượt lấy ra các ô trong fringe nếu vẫn còn.
        if problem.isGoalState(node.state) is True:
            actions = list()
            while node.action is not None:
                actions.append(node.action)
                node = node.prev # Thêm action vào list khi lấy lần lượt các node đi từ GoalState đến vị trí bắt đầu.
            actions.reverse() # Sau đó đảo ngược kết quả để có đường đi đúng.
            return actions

        if node.state not in closed: #Nếu node tiếp theo chưa thuộc danh sách đã đi qua thì thêm vào
            closed.add(node.state)
            for s in problem.getSuccessors(node.state):
                fringe.push(Node(s[0], node, s[1])) #Thêm vào fringe các node bên cạnh
                # s0 là vị trí kế tiếp, node là vị trí hiện tại, s1 là hướng đi từ node đến s0 (action)
    return list()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    closed = set()
    fringe = util.Queue()
    fringe.push(Node(problem.getStartState(), None, None))
    while fringe.isEmpty() is not True:
        node = fringe.pop()
        if problem.isGoalState(node.state) is True:
            actions = list()
            while node.action is not None:
                actions.append(node.action)
                node = node.prev
            actions.reverse()
            return actions
        if node.state not in closed:
            closed.add(node.state)
            for s in problem.getSuccessors(node.state):
                fringe.push(Node(s[0], node, s[1]))
    return list()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    closed = set()
    fringe = util.PriorityQueue()
    fringe.push(Node(problem.getStartState(), None, None), 0)
    while fringe.isEmpty() is not True:
        node = fringe.pop()
        if problem.isGoalState(node.state) is True:
            actions = list()
            while node.action is not None:
                actions.append(node.action)
                node = node.prev
            actions.reverse()
            return actions
        if node.state not in closed:
            closed.add(node.state)
            for s in problem.getSuccessors(node.state):
                fringe.push(Node(s[0], node, s[1], s[2] + node.priority),\
                            s[2] + node.priority)
    return list()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    closed = set()
    fringe = util.PriorityQueue()
    start_state = problem.getStartState()
    fringe.push(Node(start_state, None, None, \
                     heuristic(start_state, problem)), \
                heuristic(start_state, problem))
    while fringe.isEmpty() is not True:
        node = fringe.pop()
        if problem.isGoalState(node.state) is True:
            actions = list()
            while node.action is not None:
                actions.append(node.action)
                node = node.prev
            actions.reverse()
            return actions
        if node.state not in closed:
            closed.add(node.state)
            for s in problem.getSuccessors(node.state):
                fringe.push(Node(s[0], node, s[1], s[2] + node.priority), \
                            s[2] + node.priority + \
                            heuristic(s[0], problem))
    return list()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
