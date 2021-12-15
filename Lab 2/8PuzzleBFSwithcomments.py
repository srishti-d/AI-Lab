import numpy as np  # Used to store the digits in an array
import os  # Used to delete the file created by previous running of the program


class Node:
    def __init__(self, node_no, data, parent, act, cost):#similar to constructors in C++
        self.data = data
        self.parent = parent
        self.act = act
        self.cost = cost


def get_initial():
    print("Please enter number from 0-8, no number should be repeated or be out of this range")
    initial_state = np.zeros(9) #makes all the elements in array initial_state zero. 
    #part of numpy. 9 refers to number of elements in the array
    for i in range(9):#for i=0 to 8
        states = int(input("Enter the " + str(i + 1) + " number: "))#states variable stores the input given
        if states < 0 or states > 8:#checks for valid input
            print("Please only enter states which are [0-8], run code again")
            exit(0)
        else:
            initial_state[i] = np.array(states)#array initial_state[] has all the states stored in it now
    return np.reshape(initial_state, (3, 3)) #gives a new shape to the array without changing data. part of numpy
    #makes it like [[1,2,3]
                   #[4,5,6]
                   #[7,8,0]

def find_index(puzzle):
    i, j = np.where(puzzle == 0) #The numpy.where() function returns 
                    #the indices of elements in an input array where the given condition is satisfied.
    i = int(i) 
    j = int(j)
    return i, j #returns i, j, i.e, row and column numbers


def move_left(data): #moves the 0 to the left!
    i, j = find_index(data) #finds i and j when data is given
    if j == 0: #if j=0, it is in column 0. therefore, it can't move to the left
        return None
    else:
        temp_arr = np.copy(data) #copy returns an array copy of the given object. copy of data is stored in temp_arr
        temp = temp_arr[i, j - 1] #temp stores the value to the left of 0
        temp_arr[i, j] = temp #the 0 is replced with temp
        temp_arr[i, j - 1] = 0 #the position to the left of temp is replaced with 0
        return temp_arr #modified array is returned
def move_right(data): #moves 0 to the right 
    i, j = find_index(data) #finds i and j values for given data
    if j == 2: #if j=2, it is in column 2. therefore, there is no right to move to
        return None
    else:
        temp_arr = np.copy(data) #copies entire array into temp_arr 
        temp = temp_arr[i, j + 1] #temp stores the value of the number to the right of 0
        temp_arr[i, j] = temp #the 0 is replaced with temp 
        temp_arr[i, j + 1] = 0 #the position to the right of temp becomes 0
        return temp_arr
def move_up(data):
    i, j = find_index(data)
    if i == 0: #its in row 1. cant move up
        return None
    else:
        temp_arr = np.copy(data)
        temp = temp_arr[i - 1, j]
        temp_arr[i, j] = temp
        temp_arr[i - 1, j] = 0
        return temp_arr


def move_down(data):
    i, j = find_index(data)
    if i == 2:
        return None
    else:
        temp_arr = np.copy(data)
        temp = temp_arr[i + 1, j]
        temp_arr[i, j] = temp
        temp_arr[i + 1, j] = 0
        return temp_arr


def move_tile(action, data): #determines which action has to be done 
    if action == 'up':
        return move_up(data)
    if action == 'down':
        return move_down(data)
    if action == 'left':
        return move_left(data)
    if action == 'right':
        return move_right(data)
    else:
        return None


def print_states(list_final):  # To print the final states on the console
    print("printing final solution")
    for l in list_final:
        print("Move : " + str(l.act) + "\n" + "Result : " + "\n" + str(l.data) + "\t")


def path(node):  # To find the path from the goal node to the starting node
    p = []  # Empty list
    p.append(node) #The append() method in python adds a single item to the existing list. 
    #It doesn't return a new list of items but will modify the original list by adding the item to the end of the list. 
    #After executing the method append on the list the size of the list increases by one.
    parent_node = node.parent
    while parent_node is not None:
        p.append(parent_node)
        parent_node = parent_node.parent
    return list(reversed(p))


def exploring_nodes(node):
    print("Exploring Nodes")
    actions = ["down", "up", "left", "right"]
    goal_node = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    node_q = [node] #initially your array 
    final_nodes = []
    visited = []
    final_nodes.append(node_q[0].data.tolist())  # Only writing data of nodes in seen
    #tolist() is used to convert the data elements of an array into a list.
    #final_nodes 
    node_counter = 0  # To define a unique ID to all the nodes formed

    while node_q:
        current_root = node_q.pop(0)  # Pop the element 0 from the list
        if current_root.data.tolist() == goal_node.tolist(): #if current array = goal array 
            print("Goal reached")
            return current_root, final_nodes, visited

        for move in actions:
            temp_data = move_tile(move, current_root.data)
            if temp_data is not None:
                node_counter += 1
                child_node = Node(node_counter, np.array(temp_data), current_root, move, 0)  # Create a child node

                if child_node.data.tolist() not in final_nodes:  # Add the child node data in final node list
                    node_q.append(child_node)
                    final_nodes.append(child_node.data.tolist())
                    visited.append(child_node)
                    if child_node.data.tolist() == goal_node.tolist():
                        print("Goal_reached")
                        return child_node, final_nodes, visited
    return None, None, None  # return statement if the goal node is not reached


def check_correct_input(l):
    array = np.reshape(l, 9) # makes array into one long line of 9 elements like 0,1,2,3..8
    for i in range(9): #for i=0 to 8
        counter_appear = 0
        f = array[i] 
        for j in range(9):
            if f == array[j]:
                counter_appear += 1 #counter_appear=counter_appear+1
        if counter_appear >= 2:
            print("invalid input, same number entered 2 times")
            exit(0)


def check_solvable(g):
    arr = np.reshape(g, 9)
    counter_states = 0
    for i in range(9): #for i=0 to 8 
        if not arr[i] == 0: #if arr[i]!=0 
            check_elem = arr[i] #check_elem is a variable storing arr[i]
            for x in range(i + 1, 9):  
                if check_elem < arr[x] or arr[x] == 0: #memorize condition 
                    continue
                else:
                    counter_states += 1 #increment counter_states by 1 
    if counter_states % 2 == 0: #counter_states should be divisible by 2 
        print("The puzzle is solvable, generating path")
    else:
        print("The puzzle is insolvable, still creating nodes")


# Final Running of the Code
k = get_initial()

check_correct_input(k)
check_solvable(k)

root = Node(0, k, None, None, 0) #self, node_no, data, parent, act, cost

# BFS implementation call
goal, s, v = exploring_nodes(root)

if goal is None and s is None and v is None:
    print("Goal State could not be reached, Sorry")
else:
    # Print and write the final output
    print_states(path(goal))
