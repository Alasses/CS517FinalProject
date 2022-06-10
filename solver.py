from pysmt.shortcuts import Symbol, And, Or, Not, is_sat, get_model
from datetime import datetime
import graph
import generator


def GraphToClause(graph, n, keyList):

    edgeMap = {}
    clause = []

    print("= Start generating clauses.")

    #Start creating the clauses
    for i in range(n):

        print(str(i + 1) + " / " + str(n))

        varAppear = []
        varNoTwice = []
        varOccupy = []
        varNoSamePlace = []
        varExist = []


        #Each node need to appear in the path:
        # i - Represents the node
        # j - Represents each position in path
        for j in range(n):
            symAppear = Symbol("X_" + str(j) + "_" + str(i))
            varAppear.append(symAppear)
        #print(Or(varAppear))
        clause.append(Or(varAppear))


        #No node appear twice in path
        # i - Represents the node
        # j - Represents position A
        # k - Represents position B
        for j in range(n):
            for k in range(j + 1, n):
                if(j != k):
                    symNoTwiceA = Symbol("X_" + str(j) + "_" + str(i))
                    symNoTwiceB = Symbol("X_" + str(k) + "_" + str(i))
                    clause.append(Or(Not(symNoTwiceA), Not(symNoTwiceB)))


        #Every position need to be occupied
        # i - Represents the position
        # j - Represents the possible node
        for j in range(n):
            symOccupy = Symbol("X_" + str(i) + "_" + str(j))
            varOccupy.append(symOccupy)
        clause.append(Or(varOccupy))


        #No two nodes at same position
        # i - Represents the position
        # j - Represents node A
        # k - Represents node B
        for j in range(n):
            for k in range(j + 1, n):
                if(j != k):
                    symNoSamePlaceA = Symbol("X_" + str(i) + "_" + str(j))
                    symNoSamePlaceB = Symbol("X_" + str(i) + "_" + str(k))
                    clause.append(Or(Not(symNoSamePlaceA), Not(symNoSamePlaceB)))


        #Nonadjacent node i and j can not be neighbor
        # i - Represents the position
        # j - Represents node A
        # k - Represents node B
        if i < n - 1:
            for j in range(n):
                for k in range(n):
                    #Check if edge NOT exist
                    if j != k and graph[keyList[j]][keyList[k]] == 0:
                        symExistA = Symbol("X_" + str(i) + "_" + str(j))
                        symExistB = Symbol("X_" + str(i + 1) + "_" + str(k))
                        clause.append(Or(Not(symExistA), Not(symExistB)))

        #input("Anything to continue:")

        #print ("\033[A                             \033[A")

    print("= Finish generating clauses")

    return And(clause)




if __name__ == "__main__":

    #Read the original sequence
    file1 = open("./genome3.txt", "r")
    genome1 = file1.read().replace("\n",'')
    file1.close()

    stop = False
    tries = 1
    while not stop and tries < 11:
        print("== " + str(tries) + "'th try:")
        tries += 1

        #Generate random genome, using the generator.py
        #Two generated results, one strict 5 overlapping,
        #one random between 1 and 5 overlapping

        reads = generator.generateSequence(genome1, "strict", 3, 5, 8)
        #reads = generator.generateSequence(genome1, "random", 8, 9, 20)

        #print(reads_strict)

        #Generate the graph
        g = None
        g = graph.Graph(reads)
        g._construct_graph()
        keyList = list(g.adjacency_dict.keys())

        clause = GraphToClause(g.adjacency_dict, len(keyList), keyList)

        #print(clause)

        print("\n= Result:\n")

        model = None
        model = get_model(clause)
        if(model):
            #print(model)
            print("= Find model")
            orderList = []      #Store the node information
            genomeList = []     #Store the raw genome based on node information

            #Find the node on path
            for element in model:
                if(str(element[1]) == "True"):
                    parseNode = str(element[0]).split("_")
                    orderList.append([int(parseNode[1]), int(parseNode[2])])

            #Order the node based on the order in path
            orderList.sort(key = lambda e: e[0])
            for element in orderList:
                genomeList.append(keyList[element[1]])
            #print(genomeList)

            #Assembly the genome
            originalGenome = genomeList[1]
            for i in range(2, len(genomeList)):
                overlap, _ = g._get_overlap(genomeList[i - 1], genomeList[i])
                originalGenome += genomeList[i][overlap : ]
            print("= Assembly result: " + str(originalGenome == genome1))
            print(originalGenome)
            print(genome1)

            if(originalGenome == genome1):
                stop = True

                writeFile = open("./succeedGeneratedGenome" + str(datetime.now()) + ".txt", "w")
                for subSeq in reads:
                    writeFile.write(subSeq)
                    if(subSeq != reads[-1]):
                        writeFile.write("\n")
                writeFile.close()

        else:
            print("= Identify as SAT: " + str(is_sat(clause, "z3")))
            print("= No solution.")
            writeFile = open("./failedGeneratedGenome" + str(datetime.now()) + ".txt", "w")
            for subSeq in reads:
                writeFile.write(subSeq)
                if(subSeq != reads[-1]):
                    writeFile.write("\n")
            writeFile.close()

        #print(clause)

        #print(is_sat(clause))


