
# Utils
def load_input():
    with open("day_10.txt", "r") as f:
        INPUT = f.readlines()
    cleaned_input = clean_input(INPUT)
    lines = nested_lists(cleaned_input)
    return lines

# Part 1
OPENING = {"(":")", "[":"]", "{":"}", "<":">"}
CLOSING = {")": 3, "]": 57, "}": 1197, ">": 25137}

clean_input = lambda inp: [line.replace("\n", "") for line in inp]

line_to_list = lambda line: [character for character in line]

def is_line_corrupted(line, closing_stack):
    corrupted, illegal = False, ""
    if not line:
        return corrupted, illegal
    character = line[0]
    line = line[1:]
    if character in OPENING:
        next_close = OPENING[character]
        closing_stack.append(next_close)
    elif closing_stack:
        next_character = closing_stack.pop(len(closing_stack ) - 1)
        if character != next_character:
            corrupted, illegal = True, character
    next_corrupted, next_illegal = is_line_corrupted(line, closing_stack)
    corrupted, illegal = corrupted or next_corrupted, illegal or next_illegal
    return corrupted, illegal
            

_get_all_corrupted = lambda lines: [is_line_corrupted(line, []) for line in lines]
get_all_corrupted = lambda lines: [corrupted[1] for corrupted in _get_all_corrupted(lines) if corrupted[0]]

nested_lists = lambda lines: [line_to_list(line) for line in lines]

score_all_corrupted = lambda lines: sum([CLOSING[corrupted] for corrupted in get_all_corrupted(lines)])


# Part 2
SCORES = {")": 1, "]": 2, "}": 3, ">": 4}

remove_all_corrupted = lambda lines: [line for line in lines if not is_line_corrupted(line, [])[0]]

def get_closing_queue(line, closing_stack):
    if not line:
        return closing_stack
    character = line.pop(0)
    if character in OPENING:
        next_close = OPENING[character]
        closing_stack.append(next_close)
    elif closing_stack:
        closing_stack.pop(len(closing_stack ) - 1)
    return get_closing_queue(line, closing_stack)

get_autocomplete_list = lambda line: get_closing_queue(line, [])
    
score_corrections = lambda xs: [SCORES[x] for x in xs]

score_list = lambda scored: scored[0] + 5 * (score_list(scored[1:])) if scored else 0

complete_and_score = lambda line: score_list(score_corrections(get_autocomplete_list(line)))

complete_and_score_all = lambda lines: sorted([complete_and_score(line) for line in lines])

select_middle = lambda xs: xs[len(xs)//2]

INPUT="<{([([[(<>()){}]>(<<{{"
if __name__ == "__main__":
    lines = load_input()
    score = score_all_corrupted(lines)
    print(f"Corrupted Lines Scored: {score}")
    lines = load_input()
    uncorrupted_lines = remove_all_corrupted(lines)
    middle_score = select_middle(complete_and_score_all(uncorrupted_lines))
    print(f"Middle autocomplete score: {middle_score}")