# Part 1

# Parses input grid into a list
parse_input_grid = lambda grid: [[int(character) for character in row] for row in grid]

# Cleans grid to remove newline characters
clean_grid = lambda grid: [line.replace("\n", "") for line in grid]

# Get width and height of grid
get_width = lambda grid: len(grid[0])
get_height = lambda grid: len(grid)

# Adjusts edge cases to ensure they are inside the grid
adjust_edge_case = lambda x, n: 0 if x < 0 else n-1 if x >= n else x

# Gets value of point in grid
get_value = lambda grid, row, column: grid[row][column]

# For a given point, gets all surrounding points
diffs = [-1, 0, 1]
_get_surrounding_coords = lambda row, column: [[(row + row_diff, column + column_diff) for row_diff in diffs if (row_diff == 0 or column_diff == 0)] for column_diff in diffs]
get_surrounding_coords = lambda row, column: sum(_get_surrounding_coords(row, column), [])
get_adjusted_surrounding_coords = lambda row, column, width, height: [(adjust_edge_case(point[0], height), adjust_edge_case(point[1], width)) for point in get_surrounding_coords(row, column)]
get_surrounding_points = lambda row, column, width, height: [point for point in get_adjusted_surrounding_coords(row, column, width, height) if point != (row, column)]
get_surrounding_point_values = lambda grid, row, col: [get_value(grid, point_row, point_col) for point_row, point_col in get_surrounding_points(row, col, get_width(grid), get_height(grid))]

# Determines if point is lower than all surrounding points
is_low_point = lambda grid, row, column: get_value(grid, row, column) < min(get_surrounding_point_values(grid, row, column))

# Method to get coordinates of all low points
_find_low_points = lambda grid: [[(row, column) for column, _ in enumerate(columns) if is_low_point(grid, row, column)] for row, columns in enumerate(grid)]
find_low_points = lambda grid: sum(_find_low_points(grid), [])

# Method to find risks of all low points
risk_all_low_points = lambda grid: [get_value(grid, row, column) + 1 for row, column in find_low_points(grid)]

# Part 2
# Gets surrounding basin member points
get_surrounding_basin_points = lambda grid, row, col, included: [point for point in get_surrounding_points(row, col, get_width(grid), get_height(grid)) if get_value(grid, point[0], point[1]) < 9 and point not in included]

# Get all points in a basin - due to type issues with list comprehensions couldn't use a lambda (also woefully inefficient)
def get_basin_points(grid, row, col, points_in_basin):
    surrounding = get_surrounding_basin_points(grid, row, col, points_in_basin)
    if not surrounding:
        return points_in_basin
    points_in_basin = points_in_basin + surrounding
    for point in surrounding:
        adjacent_basin_points = get_basin_points(grid, point[0], point[1], points_in_basin)
        points_in_basin = points_in_basin + adjacent_basin_points
    return list(set(points_in_basin))

# Get basin sizes
get_basin_size = lambda grid, row, col: len(get_basin_points(grid, row, col, []))
get_all_basin_sizes = lambda grid: [get_basin_size(grid, low[0], low[1]) for low in find_low_points(grid)]

# Get top n basin sizes
get_n_basin_sizes = lambda grid, n: sorted(get_all_basin_sizes(grid), reverse=True)[:n]

# Function to multiply lists
multiply_list = lambda xs: xs[0] * multiply_list(xs[1:]) if xs else 1



if __name__ == "__main__":

    with open("day_9.txt", "r") as f:
        INPUT = f.readlines()
    
    grid = clean_grid(INPUT)
    heightmap = parse_input_grid(grid)
    sum_of_low_points = sum(risk_all_low_points(heightmap))
    print(f"Sum of all low points: {sum_of_low_points}")
    biggest_basins = get_n_basin_sizes(heightmap, 3)
    print(f"Multiplied 3 biggets basins: {multiply_list(biggest_basins)}")