import random
import copy

def manhattan_distance(state, goal):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                x, y = divmod(state[i][j] - 1, 3)
                distance += abs(x - i) + abs(y - j)
    return distance

def fitness(state, goal):
    return -manhattan_distance(state, goal)

def is_valid_state(state):
    flat_state = sum(state, [])
    return sorted(flat_state) == list(range(9))

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

def crossover(parent1, parent2):
    child = copy.deepcopy(parent1)
    
    crossover_point = random.randint(1, 2)
    child[crossover_point:] = parent2[crossover_point:]
    
    flat_child = sum(child, [])
    missing_numbers = set(range(9)) - set(flat_child)
    
    for i in range(9):
        if flat_child.count(flat_child[i]) > 1:
            flat_child[i] = missing_numbers.pop()
    

    return [flat_child[i:i + 3] for i in range(0, 9, 3)]


def mutate(state):
    neighbors = get_neighbors(state)
    return random.choice(neighbors)

def genetic_algorithm(initial_population, goal_state, population_size, generations, mutation_rate):
    population = initial_population
    
    for generation in range(generations):
        population.sort(key=lambda state: fitness(state, goal_state), reverse=True)
        
        if fitness(population[0], goal_state) == 0:
            return population[0], generation
        
        next_generation = population[:population_size // 2]
        
        while len(next_generation) < population_size:
            parents = random.sample(next_generation[:population_size // 4], 2)
            child = crossover(parents[0], parents[1])
            next_generation.append(child)
        
        for i in range(len(next_generation)):
            if random.random() < mutation_rate:
                next_generation[i] = mutate(next_generation[i])
        
        population = next_generation
    
    return population[0], generations

initial_state = [[1, 2, 3], [4, 0, 5], [7, 8, 6]]
goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

def generate_initial_population(population_size):
    population = []
    for _ in range(population_size):
        flat_state = random.sample(range(9), 9)
        new_state = [flat_state[i:i + 3] for i in range(0, 9, 3)]
        population.append(new_state)
    return population

population_size = 100
generations = 500
mutation_rate = 0.1

initial_population = generate_initial_population(population_size)
solution, generation_found = genetic_algorithm(initial_population, goal_state, population_size, generations, mutation_rate)

print(f"Solution found in generation {generation_found}:")
for row in solution:
    print(row)
