from time import time


def check_complete(assignment):
    if "." in assignment:
        return False
    return True


def isValid(value, assignment_list_box, assignment_list_row, assignment_list_column):
    if value in assignment_list_box or value in assignment_list_row or value in assignment_list_column:
        return False
    return True


def display(assignment):
    result = ""
    for i in range(81):
        if i % 3 == 0 and i != 0:
            result += " "
        if i % 9 == 0 and i != 0:
            result += "\n"
        if i % 27 == 0 and i != 0:
            result += "\n"
        result += assignment[i] + " "
    return result


def create_assignment_lists(var, l, assignment):
    num = var - (var % 9)
    assignment_list_box = [assignment[j] for j in l[0]]
    assignment_list_row = [assignment[j] for j in range(num, num + 9)]
    assignment_list_column = [assignment[j]
                              for j in range(len(assignment)) if abs(j - var) % 9 == 0]
    return assignment_list_box, assignment_list_row, assignment_list_column


def backtracking_search(assignment, csp_table, variables):
    return recursive_backtracking(assignment, csp_table, variables)


def recursive_backtracking(assignment, csp_table, variables):
    if check_complete(assignment):
        return assignment
    var = assignment.find(".")
    l = [i for i in csp_table if var in i]
    assignment_list_box, assignment_list_row, assignment_list_column = create_assignment_lists(
        var, l, assignment)
    for i in variables:
        if isValid(i, assignment_list_box, assignment_list_row, assignment_list_column):
            assignment = (assignment[0:var] + "z" +
                          assignment[var+1:len(assignment)]).replace("z", i)
            result = recursive_backtracking(assignment, csp_table, variables)
            if result != None:
                return result
            assignment = (assignment[0:var] + "z" +
                          assignment[var+1:len(assignment)]).replace("z", ".")
    return None


def main():
    csp_table = [[0, 1, 2, 9, 10, 11, 18, 19, 20], [3, 4, 5, 12, 13, 14, 21, 22, 23], [6, 7, 8, 15, 16, 17, 24, 25, 26], [27, 28, 29, 36, 37, 38, 45, 46, 47], [30, 31, 32, 39,
                                                                                                                                                                40, 41, 48, 49, 50], [33, 34, 35, 42, 43, 44, 51, 52, 53], [54, 55, 56, 63, 64, 65, 72, 73, 74], [57, 58, 59, 66, 67, 68, 75, 76, 77], [60, 61, 62, 69, 70, 71, 78, 79, 80]]
    variables = "123456789"
    start = time()
    var = input("Type 81 char Sudoku input: ")
    solution = backtracking_search(var, csp_table, variables)
    print("Input State")
    print("-------------------")
    print(display(var))
    print("-------------------")
    print()
    print("Solution")
    print("-------------------")
    print(display(solution))
    print("-------------------")
    print(time() - start)


if __name__ == '__main__':
    main()
