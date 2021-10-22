def terminal_test(state, tc):
    empty_spot = state.find(".")
    if empty_spot < 0:
        return True
    for li in tc:
        check_li = [state[x] for x in li]
        if len(set(check_li)) == 1 and check_li[0] != ".":
            return True
    return False


def utility(turn, tc, state):
    # return 1 (turn wins), -1 (turn loses), or 0 (tie)
    for x in tc:
        check_x = [state[y] for y in x]
        if len(set(check_x)) == 1 and check_x[0] != ".":
            if check_x[0] == turn:
                return 1
            else:
                return -1
    return 0


def minimax(state, turn, tc, goal_turn):
    if turn == goal_turn:
        v, s = max_value(state, turn, tc)
    else:
        v, s = min_value(state, turn, tc)
    return s


def max_value(state, turn, tc):
    # return value and state
    if terminal_test(state, tc):
        return utility(turn, tc, state), state
    v = -9999
    new = "O"
    if turn == "O":
        new = "X"
    for s in generateChildren(state, turn):
        num, cs = min_value(s, new, tc)
        if v < num:
            v = num
            state = s
    return (v, state)


def min_value(state, turn, tc):
    # return value and state
    if terminal_test(state, tc):
        return -1 * utility(turn, tc, state), state
    v = 9999
    new = "X"
    if turn == "X":
        new = "O"
    for s in generateChildren(state, turn):
        num, cs = max_value(s, new, tc)
        if v > num:
            v = num
            state = s
    return (v, state)


def generateChildren(state, turn):
    final = [state[0:i] + turn + state[i + 1:]
             for i in range(len(state)) if state[i] == "."]
    return final


def get_turn(state):
    c_x, c_o = 0, 0
    for s in state:
        if s == "O":
            c_o += 1
        elif s == "X":
            c_x += 1
    if c_x > c_o:
        return "O"
    return "X"


def conditions_table(n=3, n2=9):
    ret = [[] for i in range(n * 2 + 2)]
    for i in range(n2):
        ret[i // n].append(i)
        ret[n + i % n].append(i)
        if i // n == i % n:
            ret[n + n].append(i)
        if i // n == n - i % n - 1:
            ret[n + n + 1].append(i)
    return ret


def display(state, n=3, n2=9):
    str = ""
    for i in range(n2):
        str += state[i] + " "
        if i % n == n - 1:
            str += "\n"
    return str


def human_play(s, n, turn):
    index_li = [x for x in range(len(s)) if s[x] == "."]
    for i in index_li:
        print("[%s] (%s, %s)" % (i, i // n, i % n))
    index = ""
    while index.isnumeric() is False or 0 > int(index) or int(index) > 8 or s[int(index)] != ".":
        index = input("What's your input? ")
    state = s[0: int(index)] + turn + s[int(index) + 1:]
    return state


def main():
    X = ""
    while X != "h" and X != "a":
        X = input("Is X a human or AI? (h: human, a: AI) ")
    O = ""
    while O != "h" and O != "a":
        O = input("Is O a human or AI? (h: human, a: AI) ")
    state = "........."
    turn = get_turn(state)
    tc = conditions_table(3, 9)
    print("Game start!")
    print(display(state, 3, 9))
    while terminal_test(state, tc) == False:
        if turn == "X":
            print(f"{turn}'s turn:")
            if X == "a":
                state = minimax(state, turn, tc, "X")
            else:
                state = human_play(state, 3, turn)
            print(display(state, 3, 9))
            turn = "O"
        else:
            print(f"{turn}'s turn:")
            if O == "a":
                state = minimax(state, turn, tc, "O")
            else:
                state = human_play(state, 3, turn)
            print(display(state, 3, 9))
            turn = "X"

    if utility(turn, tc, state) == 0:
        print("Game over! Tie!")
    else:
        if turn == "O":
            turn = "X"
        else:
            turn = "O"
        print(f"Game over! {turn} won!")


if __name__ == "__main__":
    main()
