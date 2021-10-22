import heapq
import random
import time
import math


class PriorityQueue():
    def __init__(self):
        self.queue = []
        current = 0

    def next(self):
        if self.current >= len(self.queue):
            self.current
            raise StopIteration

        out = self.queue[self.current]
        self.current += 1

        return out

    def __iter__(self):
        return self

    __next__ = next

    def isEmpty(self):
        return len(self.queue) == 0

    def remove(self, index):
        queue = self.queue
        del queue[index]
        return queue

    def pop(self):
        return heapq.heappop(self.queue)

    def push(self, value):
        return heapq.heappush(self.queue, value)

    def peek(self):
        return self.queue[0]


def inversion_count(new_state, width, N=4):
    inv = 0
    temp = new_state.index('_')
    for i in range(len(new_state)):
        for j in range(i + 1, len(new_state)):
            if (new_state[i] > new_state[j]):
                inv += 1
    if N % 2 == 1 and inv % 2 == 0:
        return True
    else:
        if (temp == 0 or temp == 1 or temp == 2 or temp == 3 or temp == 8 or temp == 9 or temp == 10 or temp == 11) and inv % 2 == 0:
            return True
        elif (temp == 4 or temp == 5 or temp == 6 or temp == 7 or temp == 12 or temp == 13 or temp == 14 or temp == 15) and inv % 2 == 1:
            return True
    return False


def check_inversion():
    t1 = inversion_count("_42135678", 3, 3)
    f1 = inversion_count("21345678_", 3, 3)
    t2 = inversion_count("4123C98BDA765_EF", 4)
    f2 = inversion_count("4123C98BDA765_FE", 4)

    return t1 and t2 and not (f1 or f2)


def getInitialState(sample, size):
    sample_list = list(sample)
    random.shuffle(sample_list)
    new_state = ''.join(sample_list)
    while not inversion_count(new_state, size, size):
        random.shuffle(sample_list)
        new_state = ''.join(sample_list)
    return new_state


def swap(n, i, j):
    l = list(n)
    temp = l[i]
    l[i] = l[j]
    l[j] = temp
    return ''.join(l)


def generateChild(n, size):
    num = n.index('_')
    length = len(n)
    l = []
    up = num-4
    down = num+4
    left = num-1
    right = num+1
    if(up >= 0):
        # l.append(state[num-3])
        l.append(swap(n, num, up))
    if(down <= length-1):
        # l.append(state[num+3])
        l.append(swap(n, num, down))
    if(right is not 4 and right is not 8 and right is not 12 and right <= length-1):
        # l.append(state[num+1])
        l.append(swap(n, num, right))
    if(left is not 3 and left is not 7 and left is not 11 and left >= 0):
        # l.append(state[num-1])
        l.append(swap(n, num, left))
    return l


def display_path(path_list, size):
    for n in range(size):
        for i in range(len(path_list)):
            print(path_list[i][n*size:(n+1)*size], end=" "*size)
        print()
    print("\nThe shortest path length is :", len(path_list))
    return ""


''' You can make multiple heuristic functions '''


def dist_heuristic(start, goal, size):
    result = 0
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
    for i in range(len(start)):
        if start[i] is not '_':
            num2 = goal.index(start[i])
            x1 = i % 4
            y1 = i/size
            x2 = num2 % 4
            y2 = num2/size
            result += abs(x1-x2) + abs(y1-y2)
    return result


def check_heuristic():
    a = dist_heuristic("152349678_ABCDEF", "_123456789ABCDEF", 4)
    b = dist_heuristic("8936C_24A71FDB5E", "_123456789ABCDEF", 4)
    return (a < b)


def a_star(start, goal="_123456789ABCDEF", heuristic=dist_heuristic, size=4):
    frontier = PriorityQueue()
    if start == goal:
        return []
    x = heuristic(start, goal, size)
    explored = {start: x}
    frontier.push((x, start, [start]))
    while frontier.isEmpty() == False:
        cost, current, path = frontier.pop()
        if current == goal:
            return path
        for a in generateChild(current, size):
            f = heuristic(a, goal, size) + len(path)
            if (a in explored and f < explored[a]) or (a not in explored):
                frontier.push((f, a, path + [a]))
                explored[a] = f
    return None


def main():
    print("Inversion works?:", check_inversion())
    print("Heuristic works?:", check_heuristic())
    initial_state = input("Type initial state: ")
    cur_time = time.time()
    path = (a_star(initial_state))
    if path != None:
        display_path(path, 4)
    else:
        print("No Path Found.")
    print("Duration: ", (time.time() - cur_time))


if __name__ == '__main__':
    main()


'''
SAMPLE INITIAL STATES

Initial State: 152349678_ABCDEF
Initial State: 2_63514B897ACDEF
Initial state: 8936C_24A71FDB5E

'''
