import os
import re
BLOCKCHAR = "#"
OPENCHAR = "-"
PROTECTEDCHAR = "~"
count = 0
lettersDict = {}


def initialize(height, width, numBlocked, words):
    temp = OPENCHAR*(height*width)
    for word in words:
        pos = word[1] * width + word[2]
        if word[0] == "V":
            for i in word[3]:
                temp = temp[0:pos] + i + temp[pos+1:]
                pos += width
        else:
            for i in word[3]:
                temp = temp[0:pos] + i + temp[pos+1:]
                pos += 1
    if height % 2 != 0 and width % 2 != 0 and numBlocked % 2 != 0:
        center = (height//2)*width+(width//2)
        temp = temp[0:center] + BLOCKCHAR + temp[center+1:]
    puzzle = BLOCKCHAR*(width+3)
    puzzle += (BLOCKCHAR*2).join([temp[p:p+width]
                                  for p in range(0, len(temp), width)])
    puzzle += BLOCKCHAR*(width+3)
    return puzzle


def display(height, width, puzzle):
    thing = ""
    for x in range(len(puzzle)):
        if 0 <= x < width+2 or x % (width+2) == 0 or x % (width+2) == width+1 or (len(puzzle) - width - 2) <= x < len(puzzle):
            continue
        else:
            thing += puzzle[x]
    result = ""
    for x in range(len(thing)):
        if x % (width) == 0:
            result += "\n"
        result += thing[x] + ""
    return result


def palindrome(puzzle):
    temp = puzzle[::-1]
    result = combine(puzzle, temp)
    return result


def combine(str1, str2):
    result = ""
    for x in range(len(str1)):
        if str1[x] is not OPENCHAR:
            result += str1[x]
        elif str2[x] is not OPENCHAR:
            result += str2[x]
        else:
            result += OPENCHAR
    return result


def areafill(puzzle, index, width, height):
    puzzle = puzzle[0:index] + "." + puzzle[index+1:]
    directions = [-1, 1, width+2, -1*width-2]
    for x in directions:
        if puzzle[index+x] == OPENCHAR or puzzle[index+x] == PROTECTEDCHAR:
            puzzle = areafill(puzzle, index+x, width, height)
    return puzzle


def transpose(puzzle, newWidth):
    return "".join([puzzle[col::newWidth] for col in range(newWidth)])


def protected(puzzle, width):
    result = puzzle
    for x in range(len(puzzle)):
        if puzzle[x] is not BLOCKCHAR and puzzle[x] is not OPENCHAR:
            result = result[0:x] + PROTECTEDCHAR + result[x+1:]
    return palindrome(result)


def implied(puzzle, width, height):
    global count
    puzzle = puzzle.replace("#-#-#", "#####")
    puzzle = puzzle.replace("#--#--#", "#######")
    puzzle = puzzle.replace("#-#", "###")
    puzzle = puzzle.replace("#--#", "####")
    puzzle = puzzle.replace("#~--", "#~~~")
    puzzle = puzzle.replace("--~#", "~~~#")
    puzzle = puzzle.replace("#~~-", "#~~~")
    puzzle = puzzle.replace("-~~#", "~~~#")
    puzzle = puzzle.replace("#~-~", "#~~~")
    puzzle = puzzle.replace("~-~#", "~~~#")
    puzzle = transpose(puzzle, width+2)
    count += 1
    if "#-#" in puzzle or "#--#" in puzzle or "#~--" in puzzle or "#~~-" in puzzle or "#~-~" in puzzle:
        puzzle = implied(puzzle, height, width)
    if count % 2 != 0:
        puzzle = transpose(puzzle, height+2)
    count = 0
    return puzzle


def backtracking_search(puzzle, numBlocked, width, height):
    return recursive_backtracking(puzzle, numBlocked, width, height)


def recursive_backtracking(puzzle, numBlocked, width, height):
    illegalRegex = "[{}](.?[{}]|[{}].?)[{}]".format(
        BLOCKCHAR, PROTECTEDCHAR, PROTECTEDCHAR, BLOCKCHAR)
    if puzzle.count("#")-(2*(height+1)+2*(width+1)) > numBlocked:
        return None
    if re.search(illegalRegex, puzzle):
        return None
    if re.search(illegalRegex, transpose(puzzle, width+2)):
        return None
    if "-" in puzzle:
        board = areafill(puzzle, puzzle.find("-"), width, height)
    else:
        board = areafill(puzzle, puzzle.find("~"), width, height)
    if puzzle.count("-") + puzzle.count("~") != board.count("."):
        return None
    if puzzle.count("#")-(2*(height+1)+2*(width+1)) == numBlocked:
        return puzzle
    board = puzzle
    list = [x for x in range(len(puzzle)) if puzzle[x] == "-"]
    for i in list:
        puzzle = puzzle[0:i] + "#" + puzzle[i+1:]
        puzzle = puzzle[0:len(puzzle)-1-i] + "#" + puzzle[len(puzzle)-i:]
        puzzle = implied(puzzle, width, height)
        result = recursive_backtracking(puzzle, numBlocked, width, height)
        if result != None:
            return result
        puzzle = board
    return None


def mostConstrained(patterns, hwords, vwords):
    result = (0, 0, 0, 99999)
    for x in hwords:
        # if "-" in hwords[x]:
        #list = ["" for z in range(len(hwords[x]))]
        aset = set(patterns["-"*len(hwords[x])])
        #alist = patterns["-"*len(hwords[x])]
        # print(alist)
        for y in range(len(hwords[x])):
            if hwords[x][y] != "-":
                pattern = "-"*len(hwords[x])
                pattern = pattern[0:y] + hwords[x][y] + pattern[y+1:]
                if pattern not in patterns:
                    return None
                aset = aset.intersection(set(patterns[pattern]))
                #list[y] = set(patterns[pattern])
                #anotherlist = copy.deepcopy(alist)
                #alist = anotherlist + patterns[pattern]
                # print(alist)
        #aset = aset.intersection(*list)
        # print(aset)
        # print(aset)
        if len(aset) < result[3] and "-" in hwords[x]:
            result = (x, "H", hwords[x], len(aset), aset)
    # print("V")
    for x in vwords:
        # if "-" in vwords[x]:
        #list = ["" for z in range(len(vwords[x]))]
        aset = set(patterns["-"*len(vwords[x])])
        #alist = patterns["-"*len(vwords[x])]
        # print(alist)
        # print(aset)
        for y in range(len(vwords[x])):
            if vwords[x][y] != "-":
                pattern = "-"*len(vwords[x])
                pattern = pattern[0:y] + vwords[x][y] + pattern[y+1:]
                # print(pattern)
                if pattern not in patterns:
                    return None
                #list[y] = set(patterns[pattern])
                aset = aset.intersection(set(patterns[pattern]))
                #anotherlist = copy.deepcopy(alist)
                #alist = anotherlist + patterns[pattern]
        # print(aset)
        #aset = aset.intersection(*list)
        if len(aset) < result[3] and "-" in vwords[x]:
            result = (x, "V", vwords[x], len(aset), aset)
    return result


def horizontal(puzzle, width, dictLines):
    result = {}
    for x in range(len(puzzle)):
        if puzzle[x] is not BLOCKCHAR and puzzle[x-1] is BLOCKCHAR:
            result[x] = ""
            for y in range(x, len(puzzle)):
                if puzzle[y] is BLOCKCHAR:
                    break
                else:
                    result[x] += puzzle[y]
    return result


def vertical(puzzle, width, dictLines):
    result = {}
    for x in range(len(puzzle)):
        if puzzle[x] is not BLOCKCHAR and puzzle[x-width-2] is BLOCKCHAR:
            result[x] = ""
            for y in range(x, len(puzzle), width+2):
                if puzzle[y] is BLOCKCHAR:
                    break
                else:
                    result[x] += puzzle[y]
    return result


def patterns(words):
    result = {}
    for x in words:
        pattern = "-"*len(x)
        if pattern not in result:
            result[pattern] = []
        result[pattern].append(x)
        for y in range(len(x)):
            pattern = "-"*len(x)
            pattern = pattern[0:y] + x[y] + pattern[y+1:]
            if pattern not in result:
                result[pattern] = []
            result[pattern].append(x)
    return result


def addWord(puzzle, word, index, orientation, width):
    temp = puzzle
    if orientation == "V":
        for i in word:
            temp = temp[0:index] + i + temp[index+1:]
            index += width+2
    else:
        for i in word:
            temp = temp[0:index] + i + temp[index+1:]
            index += 1
    return temp


def findGoodWords(word):
    c = 0
    # print(words)
    for x in word:
        c += lettersDict[x]
        #num = 15371*x.count('E') + 10491*x.count('S') + 2*x.count('R') + 2*x.count('A') + 2*x.count('I') + x.count('T')  + x.count('N') + x.count('O') + -2*x.count('V') + -5*x.count('J') + -10*x.count('X') + -10*x.count('Z') + -10*x.count('Q')
        #num = 3*x.count('E') + 2*x.count('S') + 2*x.count('A') + 2*x.count('I') + 2*x.count('T') + 2*x.count('O') + 2*x.count('N') + -3*x.count('X') + -3*x.count('Z') + -3*x.count('Q')
    return c
    # print(result)
    # result.sort(reverse=True)
    # print(result)
    # print(result)
    # return result


def solve_recursive(puzzle, patterns, hwords, vwords, width, height, dictLines):
    return solve_backtracking(puzzle, patterns, hwords, vwords, set(), width, height, dictLines)


def solve_backtracking(puzzle, patterns, hwords, vwords, usedWords, width, height, dictLines):
    print(display(height, width, puzzle))
    # print(dictLines)
    if OPENCHAR not in puzzle:
        return puzzle
    mostC = mostConstrained(patterns, hwords, vwords)
    if mostC == None:
        return None
    goodWords = list(mostC[4])
    # print(goodWords)
    goodWords.sort(key=lambda word: findGoodWords(word), reverse=True)
    # print(goodWords)
    for x in goodWords:
        if x in usedWords:
            continue
        #board = copy.deepcopy(puzzle)
        #temp = copy.deepcopy(usedWords)
        puzzle = addWord(puzzle, x, mostC[0], mostC[1], width)
        hwords = horizontal(puzzle, width, dictLines)
        # print(hwords)
        vwords = vertical(puzzle, width, dictLines)
        # print(vwords)
        for y in hwords.values():
            # if "-" not in y:
            if y not in dictLines and "-" not in y:
                return None
            else:
                usedWords.add(y)
        for y in vwords.values():
            # if "-" not in y:
            if y not in dictLines and "-" not in y:
                return None
            else:
                usedWords.add(y)
        # usedWords.add(x[1])
        result = solve_backtracking(
            puzzle, patterns, hwords, vwords, usedWords, width, height, dictLines)
        if result != None:
            return result
        #puzzle = board
        #usedWords = temp
        usedWords.remove(x)
    # print("NONE")
    return None


def main():
    intTest = [r"^(\d+)x(\d+)$", r"^\d+$", r"^(H|V)(\d+)x(\d+)(.+)$"]
    height, width, numBlocked, dictSeen, words = 4, 4, 0, False, []
    for x in input("File: ").split(" "):
        if x != 0:
            if os.path.isfile(x):
                dictLines = open(x, 'r').read().upper().splitlines()
                letters = "abcdefghijklmnopqrstuvwxyz".upper()
                with open(x, 'r') as myfile:
                    data = myfile.read().upper()
                for x in letters:
                    lettersDict[x] = data.count(x)
                dictSeen = True
                continue
            for num, reg in enumerate(intTest):
                match = re.search(reg, x, re.I)
                if not match:
                    continue
                if num == 0:
                    height, width = int(match.group(1)), int(match.group(2))
                elif num == 1:
                    numBlocked = int(x)
                else:
                    vpos, hpos = int(match.group(2)), int(match.group(3))
                    word = match.group(4).upper()
                    words.append([x[0].upper(), vpos, hpos, word])
    if not dictSeen:
        exit("File not found")
    start = initialize(height, width, numBlocked, words)
    if numBlocked == height*width:
        puzzle = start.replace("-", "#")
    elif numBlocked == 0:
        puzzle = start
    else:
        print(display(height, width, start))
        puzzle = protected(start, width)
        print(display(height, width, puzzle))
        puzzle = implied(puzzle, width, height)
        if "-" in puzzle:
            board = areafill(puzzle, puzzle.find("-"), width, height)
        else:
            board = areafill(puzzle, puzzle.find("~"), width, height)
        if puzzle.count("-") + puzzle.count("~") != board.count("."):
            pos = board.find("-")
            puzzle = puzzle[0:pos] + "#" + puzzle[pos+1:]
            puzzle = palindrome(puzzle)
        puzzle = implied(puzzle, width, height)
        print(display(height, width, puzzle))
        puzzle = backtracking_search(puzzle, numBlocked, width, height)
        puzzle = puzzle.replace("~", "-")
        puzzle = combine(puzzle, start)
    print(display(height, width, puzzle))
    hwords = horizontal(puzzle, width, dictLines)
    vwords = vertical(puzzle, width, dictLines)
    allPatterns = patterns(dictLines)
    # print(lettersDict)
    #print(sorted(lettersDict.items(), reverse=True, key = lambda kv:(kv[1], kv[0])))
    # print(patterns(dictLines))
    puzzle = solve_recursive(puzzle, allPatterns, hwords,
                             vwords, width, height, dictLines)
    print(display(height, width, puzzle))
    #print(mostConstrained(dict, hwords, vwords))


if __name__ == '__main__':
    main()
