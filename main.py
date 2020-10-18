#!/usr/bin/env python3
from functools import partial


def play(field: list, winsize: int, step_count: int = 0):
    print_state(field, step_count)
    player = 'o' if step_count % 2 else 'x'

    row, column = get_step(player, field)
    field[row][column] = player
    next_step(field, winsize, step_count, player, coordinate=(row, column))


def next_step(field: list, winsize: int, step_count: int, player: str, coordinate: tuple = ()):
    column = [i[coordinate[1]] for i in field]
    row = field[coordinate[0]]
    slash = find_slash(field, winsize, coordinate)
    back_slash = find_slash(field, winsize, coordinate, back=True)
    check_line_partial = partial(check_line, winsize * player)
    if any(map(check_line_partial, (column, row, slash, back_slash))):
        print_win(field, player, step_count)
    elif step_count + 1 == len(field) ** 2:
        print_standoff(field)
    else:
        play(field, winsize, step_count=step_count + 1)


def print_win(filed: list, player: str, step_count: int):
    print_field(filed)
    print("Congratulation!")
    print(f"Player '{player}' WIN on step {step_count}")


def print_standoff(field: list):
    print_field(field)
    print("All wins!")


def find_slash(field: list, winsize: int, coordinate: tuple, back=False) -> list:
    y, x = coordinate
    line = []
    c = 0
    start_x = x - winsize + 1
    if back:
        start_y = y - winsize + 1
    else:
        start_y = y + winsize - 1
    while c <= winsize * 2 - 1:
        new_y = start_y + c if back else start_y - c
        new_x = start_x + c
        if new_y < 0 or new_x < 0:
            c += 1
            continue
        try:
            d = field[new_y][new_x]
        except IndexError:
            continue
        finally:
            c += 1
        line.append(d)

    return line


def check_line(test_line: str, line: list) -> bool:
    return test_line in ''.join(map(str, line))


def print_state(field: list, step_count: int):
    print("=" * 10)
    print(f"Step: {step_count}")
    print_field(field)


def print_field(f: list):
    n = len(f[0])
    print("  {}".format(' '.join(str(x) for x in range(n))))
    for i, raw in enumerate(f):
        print(f"{i} {' '.join(f[i])}")


def get_step(player: str, field: list):
    field_size = len(field)
    coord_column = input(f"Select next step for '{player}' column: ")
    coord_row = input(f"Select next step for '{player}' row: ")
    try:
        coord_column = int(coord_column)
        coord_row = int(coord_row)
    except ValueError:
        print(f"Coordinates must be a number")
        return get_step(player, field)

    if 0 <= coord_column <= field_size and 0 <= coord_row <= field_size:
        return coord_row, coord_column
    else:
        print(f"Coordinate must be in 0 - {field_size}")

    if field[coord_row][coord_column] == 'x' or field[coord_row][coord_column] == 'o':
        print("This cell is already occupied")
    return get_step(player, field)


def init_field() -> tuple:
    """
    Initial playground

    :return: tuple: field list and line size for win
    """
    n = get_field_size()
    return [['-'] * n for _ in range(n)], get_win_size(n)


def get_field_size() -> int:
    n = input("Select field size NxN (begin from 3): ")
    try:
        n = int(n)
    except ValueError:
        print("Size must be a number")
        n = get_field_size()
    if n < 3:
        print("Size must be >= 3")
        n = get_field_size()
    return n


def get_win_size(n) -> int:
    win = input(f"Select win size from 3 to {n}: ")
    try:
        win = int(win)
    except ValueError:
        print(f"Win size must be a number")
        win = get_win_size(n)
    if win < 3 or win > n:
        print(f"Win size from 3 to {n}:")
        win = get_win_size(n)
    return win


if __name__ == '__main__':
    print(f"Welcome")
    play(*init_field())
