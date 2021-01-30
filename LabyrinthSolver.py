import copy

class Solver:

    """
    The solver is using BFT- Algorith to solve the shortest route in the given map.
    Give walls as "#"-marks, beginning as "^"-mark, exits as "E" and empty space as " ".
    
                        ##E########
                        ##      ###
                        # # ###   #
                        # ### ### #
                        #         #
                        ######^####
    
    Just run the application and enter the whole name of the txt-file when it is asked.
    It will tell you the answer and draw a solved map to you on the same path when you ran this application.

    """
    
    START = [] # Starting position
    END = [] # Found End points
    array = [] # Array where is the map
    solvedarray = [] # Copy of array on top of which is written the solved route
    filename = ""

    # Function for interpreting and writing the map into an array
    @classmethod
    def read_map(cls):
        while True: #Loops until successful
            cls.filename = input("Please write the name of the txt-file e.g. map.txt: ")
            try:
                with open(cls.filename) as mapfile:
                    for line in mapfile:
                        newline = []
                        for ch in line:
                            if ch == "\n":
                                cls.array.append(newline)
                                cls.solvedarray.append(newline.copy())
                            else:
                                if ch == "^":
                                    y = len(cls.array)
                                    x = len(newline)
                                    cls.START = [y, x]
                                elif ch == "E":
                                    y = len(cls.array)
                                    x = len(newline)
                                    cls.END.append([y, x])
                                newline.append(ch)
                break
            except FileNotFoundError:
                print("File could not be found. Try again")
            except PermissionError:
                print("Permission denied. Try again") 
            except OSError:
                print("Invalid agrument")
            except:
                print("Unexpected error occured")

    # Writes the shortest path that was written in solvedarray on to the new text file
    @classmethod
    def write_on_map (cls):
        with open(cls.filename + "solved.txt", 'w') as mapfile:
            i = 0
            for line in cls.solvedarray:
                if i == 0:
                    i = i + 1
                else:
                    mapfile.write("\n")
                for ch in line:
                    mapfile.write(str(ch))

    # Compares which is the shortest route and then backtracks and writes the route on the solvedarray
    @classmethod
    def write_route(cls):
        nearest = []
        shortlength = 999
        for exit in cls.END:
            neighbours = cls.get_neighbours(exit)
            for neighbour in neighbours:
                if cls.array[neighbour[0]][neighbour[1]] == "#":
                    continue
                else:
                    length = cls.array[neighbour[0]][neighbour[1]]
                    if length < shortlength:
                        shortlength = length
                        nearest = exit
        print("Shortest exit: " + str(nearest) + " with length of: " + str(shortlength + 1))
        cls.solvedarray[nearest[0]][nearest[1]] = "O" # Writes "O" to represent the path
        node = nearest
        while shortlength >= 0:
            neighbours = cls.get_neighbours(node)
            for  n in neighbours:
                if cls.array[n[0]][n[1]] == shortlength:
                    cls.solvedarray[n[0]][n[1]] = "O"
                    node = n
            shortlength -= 1

    # Gets the neighbours of the node
    @classmethod
    def get_neighbours(cls, node):
        neighbours = []
        y = node[0]
        x = node[1]
        maY = len(cls.array) - 1
        maX = len(cls.array[0]) - 1

        if x == 0 and y == 0 or x == 0 and y == maX: # Left hand corners
            if y == 0:
                neighbours.append([y, x + 1])
                neighbours.append([y + 1, x])
            elif y == maX:
                neighbours.append([y - 1, x])
                neighbours.append([y, x + 1])
        elif x == maX and y == 0 or x == maX and y == maX: # Right hand corners
            if y == 0:
                neighbours.append([y, x - 1])
                neighbours.append([y + 1, x])
            elif y == maX:
                neighbours.append([y - 1, x])
                neighbours.append([y, x - 1])
        elif x == 0: # Left side
            neighbours.append([y, x + 1])
            neighbours.append([y + 1, x])
            neighbours.append([y - 1, x])        
        elif x == maX: # Right side
            neighbours.append([y, x - 1])
            neighbours.append([y + 1, x])
            neighbours.append([y - 1, x])
        elif y == 0: # Top side
            neighbours.append([y, x - 1])
            neighbours.append([y, x + 1])
            neighbours.append([y + 1, x])
        elif y == maY: # Bottom side
            neighbours.append([y, x - 1])
            neighbours.append([y, x + 1])
            neighbours.append([y - 1, x])
        else: # All the other
            neighbours.append([y, x - 1])
            neighbours.append([y, x + 1])
            neighbours.append([y - 1, x])
            neighbours.append([y + 1, x])
        return neighbours

    # Function that marks and goes through the map
    @classmethod
    def route_mapper(cls):
        exits = [] # Found accessible exits
        visited = [] # Visited nodes
        queue = [] # The Stack
        queue.append(cls.START)

        while not len(queue) == 0:
            node = queue.pop()
            if node in visited: # if the node is already visited it is skipped
                continue
            visited.append(node)
            if cls.array[node[0]][node[1]] == "E": # if the node is way out of maze it is added to the exits
                exits.append(node)
                continue
            neighbours = cls.get_neighbours(node)
            if len(neighbours) != 0:
                lowestcost = 9999999
                for neighbour in neighbours: # Going through individual neighbours and checking which one has the lowest cost
                    if cls.array[neighbour[0]][neighbour[1]] == "#": # Ignoring walls
                        continue
                    try:
                        if lowestcost > cls.array[neighbour[0]][neighbour[1]]:
                            lowestcost = cls.array[neighbour[0]][neighbour[1]]
                    except TypeError:
                        pass
                    if neighbour not in visited: # Ignores visited nodes and accepts unvisited ones
                        queue.insert(0, neighbour)
                if cls.array[node[0]][node[1]] == "^":
                    cls.array[node[0]][node[1]] = 0
                else:
                    cls.array[node[0]][node[1]] = lowestcost + 1 # marking the shortest neighbours path + 1
        return exits

    # Main function
    @classmethod
    def main(cls):
        cls.read_map()
        exits = cls.route_mapper()
        if len(exits) == 0:
            print("There were no exits you can access! You can't get out")
        else:
            cls.write_route()
            cls.write_on_map()

if __name__ == "__main__":
    Solver.main()
            