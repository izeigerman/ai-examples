#!/usr/bin/env python3

# 8-puzzle (https://en.wikipedia.org/wiki/15_puzzle) generator and solver.
# Implemented using the A* algorithm and Manhattan distance heuristics.
# Generates a random puzzle and prints each step of a solution search.

import copy
import random
import uuid
from collections import namedtuple
from queue import PriorityQueue


BOARD_SIZE = 3


def swap(state, r1, c1, r2, c2):
    new_state = copy.deepcopy(state)
    new_state[r1][c1] = state[r2][c2]
    new_state[r2][c2] = state[r1][c1]
    return new_state


def move_right(state, r, c):
    return swap(state, r, c, r, c + 1)


def move_left(state, r, c):
    return swap(state, r, c, r, c - 1)


def move_up(state, r, c):
    return swap(state, r, c, r - 1, c)


def move_down(state, r, c):
    return swap(state, r, c, r + 1, c)


def heuristic_cost(state):
    """Calculates cost of the state using the Manhattan distance algorithm."""
    result = 0
    for row_idx in range(BOARD_SIZE):
        for col_idx in range(BOARD_SIZE):
            value = state[row_idx][col_idx]

            if not value or value < 0:
                value = BOARD_SIZE * BOARD_SIZE

            expected_row = int((value - 1) / BOARD_SIZE)
            vertical_step = abs(expected_row - row_idx)

            expected_col = int((value - BOARD_SIZE * expected_row) - 1)
            horizontal_step = abs(expected_col - col_idx)

            distance = vertical_step + horizontal_step
            result += distance
    return result


def get_available_actions(state):
    """Returns a list of actions that can be performed for the given state."""
    actions = []
    empty_row = 0
    empty_col = 0
    for row_idx in range(BOARD_SIZE):
        for col_idx in range(BOARD_SIZE):
            if state[row_idx][col_idx] is None:
                empty_row = row_idx
                empty_col = col_idx
                break
    if empty_row > 0:
        actions.append(lambda s: move_up(s, empty_row, empty_col))
    if empty_row < BOARD_SIZE - 1:
        actions.append(lambda s: move_down(s, empty_row, empty_col))
    if empty_col > 0:
        actions.append(lambda s: move_left(s, empty_row, empty_col))
    if empty_col < BOARD_SIZE - 1:
        actions.append(lambda s: move_right(s, empty_row, empty_col))
    return actions


def state_to_tuple(state):
    return tuple(map(tuple, state))


StateWithParent = namedtuple('StateWithParent', ['state', 'parent'])


def solve_puzzle(initial_state):
    """Finds the solution for the given initial state using A* search algorithm."""
    queue = PriorityQueue()
    visited_states = set()

    queue.put((0, uuid.uuid4(), StateWithParent(state=initial_state, parent=None)))

    while not queue.empty():
        parent_cost, _, current_state_with_parent = queue.get()

        current_state = current_state_with_parent.state
        visited_states.add(state_to_tuple(current_state))

        actions = get_available_actions(current_state)
        successor_states = map(lambda action: action(current_state), actions)

        for state in successor_states:
            if state_to_tuple(state) not in visited_states:
                new_state_with_parent = StateWithParent(state=state,
                                                        parent=current_state_with_parent)
                cost = heuristic_cost(state)
                if cost == 0:
                    # If the heuristic cost of the given state equals 0, then
                    # the goal state is found and we can return it immediately.
                    return new_state_with_parent
                total_cost = cost + parent_cost

                queue.put((total_cost, uuid.uuid4(), new_state_with_parent))

    return None


def print_state(state):
    for row in state:
        print(' '.join(map(lambda i: str(i) if i else '_', row)))
        print("")


def print_solution(initial_state, solution):
    if not solution:
        print('===NO SOLUTION===')
        print_state(initial_state)
        return

    stack = []
    current = solution
    while current:
        stack.append(current.state)
        current = current.parent

    print('===START===')
    print_state(stack.pop())

    step_number = 1
    while len(stack) > 0:
        print('===STEP {}==='.format(step_number))
        print_state(stack.pop())
        step_number += 1


def is_problem_solvable(values):
    size = len(values)
    inv = 0
    for i in range(size):
        for j in range(i + 1, size):
            if values[i] != size and values[j] != size and values[i] > values[j]:
                inv += 1
    return inv % 2 == 0


def generate_random_problem():
    generated_state = [None] * BOARD_SIZE
    max_value = BOARD_SIZE * BOARD_SIZE

    available_values = list(range(1, max_value + 1))
    random.shuffle(available_values)
    while not is_problem_solvable(available_values):
        random.shuffle(available_values)

    values_idx = 0
    for row_idx in range(BOARD_SIZE):
        generated_state[row_idx] = []
        for col_idx in range(BOARD_SIZE):
            value = available_values[values_idx]
            if value == max_value:
                value = None
            generated_state[row_idx].append(value)
            values_idx += 1
    return generated_state


def run():
    generated_state = generate_random_problem()
    solution = solve_puzzle(generated_state)
    print_solution(generated_state, solution)


if __name__ == '__main__':
    run()
