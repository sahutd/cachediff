import sys


def process():
    v = 100 #size of matrix. update as necessary
    array = []
    print(v)
    for i in range(v):
        array.append(list(map(int, input().split())))
    adjacency_list = []
    for row in array:
        adjacent = []
        for i in range(v):
            if row[i] == 1:
                adjacent.append(i)
        adjacency_list.append(adjacent)
    for row in adjacency_list:
        sys.stdout.write(str(len(row)) + ' ')
        for i in row:
            sys.stdout.write(str(i) + ' ')
        print()


if __name__ == '__main__':
    process()
