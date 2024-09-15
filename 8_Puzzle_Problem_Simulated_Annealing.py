import random
import math
import copy

def manhattan_distance(state, goal):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                x, y = divmod(state[i][j] - 1, 3)
                distance += abs(x - i) + abs(y - j)
    return distance

def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def get_neighbors(state):
    neighbors = []
    x, y = find_blank(state)
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_state = copy.deepcopy(state)
            new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
            neighbors.append(new_state)
    return neighbors

def simulated_annealing(initial_state, goal_state, initial_temp, cooling_rate):
    current_state = initial_state
    current_temp = initial_temp

    while current_temp > 1e-5:
        current_cost = manhattan_distance(current_state, goal_state)
        if current_cost == 0:
            return current_state
        neighbors = get_neighbors(current_state)
        next_state = random.choice(neighbors)
        next_cost = manhattan_distance(next_state, goal_state)
        delta_cost = next_cost - current_cost
        if delta_cost < 0 or random.random() < math.exp(-delta_cost / current_temp):
            current_state = next_state
        current_temp *= cooling_rate

    return current_state

