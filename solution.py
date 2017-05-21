assignments = []


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]


rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diagonal_units = [[row + col for row, col in zip(rows, cols)],
                  [row + col for row, col in zip(rows, sorted(cols, reverse=True))]]
unitlist = row_units + column_units + square_units + diagonal_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)  # contains diagonal
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)  # contains diagonal peers


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
        # print("*************")
        # display(assignments[-1])
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unitlist:
        naked_twins_list = []

        # Find all instances of naked twins in a unit
        for box in unit:
            value = values[box]
            if len(value) == 2:
                naked_twins_list.append(value)

        naked_twins_list = sorted(naked_twins_list)  # sort and twins will be adjacent

        len_list = len(naked_twins_list)
        for i in range(len_list):
            # test if there are twins adjacent
            if i + 1 < len_list and naked_twins_list[i] == naked_twins_list[i + 1]:
                # Eliminate the naked twins as possibilities in the unit
                twins = naked_twins_list[i]
                n1, n2 = twins
                for box in unit:
                    value = values[box]
                    if len(value) > 1 and value != twins:
                        value = value.replace(n1, "")
                        value = value.replace(n2, "")
                        assign_value(values, box, value)
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    d = {}
    for i, x in enumerate(grid):
        if x == ".":
            x = "123456789"
        d[boxes[i]] = x
    return d


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    solved_values = dict(filter(lambda x: len(x[1]) == 1, values.items()))  # box with only one possibility remains

    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            # eliminate its peers
            peer_value = values[peer]
            peer_value = peer_value.replace(digit, '')
            assign_value(values, peer, peer_value)
    return values


def only_choice(values):
    for unit in unitlist:
        for num in "123456789":
            # find how many box contains the number
            num_boxs = [box for box in unit if num in values[box]]

            # if there is only one then assign
            if len(num_boxs) == 1:
                assign_value(values, num_boxs[0], num)
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        values = eliminate(values)

        # Use the Naked twins Eliminate Strategy
        values = naked_twins(values)

        # Use the Only Choice Strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    # First, reduce the puzzle using the previous function
    reduced_values = reduce_puzzle(values)
    if reduced_values == False:
        return False

    # choose min values of box
    min_value = "123456789"
    min_box = None
    for box, value in reduced_values.items():
        if 1 < len(value) < len(min_value):
            min_box = box

    # deep first search recursion
    if min_box:
        for value in reduced_values[min_box]:
            new_sudoku = reduced_values.copy()
            assign_value(new_sudoku, min_box, value)
            output = search(new_sudoku)
            if output:
                return output
    else:  # no min_box greater than 1 means solved, recursion ends.
        return reduced_values


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    # change form
    values = grid_values(grid)

    # reduce it
    values = search(values)
    if values:
        return values
    else:
        return False  # failed


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
