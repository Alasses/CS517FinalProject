import random
from datetime import datetime

#   This function generate random genome sequence from the given main genome
#   with a fixed or random overlapping.
#
#   @sequence: 
#   @mode:  "strict" for exact overlapping 
#           "random" for random overlapping, at least 1 
#   @overlapping:   If in "strict" mode, this will be exactly overlapping
#                   If in "random" mode, this will be max possible overlapping
#   @minLen, maxLen:    The minimum and maximum length of generated sequence
#
def generateSequence(sequence, mode, overlapping = 3, minLen = 5, maxLen = 20):
    random.seed(datetime.now())
    subSeq = []
    start = 0
    end = 0

    if(minLen <= overlapping):
        print("Minimum length must greater than overlapping length!")
        return []
    if(maxLen <= minLen):
        print("Maximum length can't smaller than minimum length!")
        return []

    print("= Generating genome sequences.")

    while(end < len(sequence)):

        end = start + random.randint(minLen, maxLen)
        if(end > len(sequence)):
            end = len(sequence)

        subSeq.append(sequence[start:end])

        if(mode == "strict"):
            start = end - overlapping
        elif(mode == "random"):
            start = end - random.randint(1, overlapping)
        else:
            print("Wrong mode!")
            return []

    print("= Generated " + str(len(subSeq)) + " sequences.")
    return subSeq


if __name__ == '__main__':
    file1 = open("./genome1.txt", "r")
    file2 = open("./genome2.txt", "r")
    genome1 = file1.read().replace("\n",'')     #Remove all new line character
    genome2 = file2.read().replace("\n",'')
    file1.close()
    file2.close()
    print("Genome seq 1:\n" + genome1 + "\n")
    #print("Genome seq 2:\n" + genome2 + "\n")

    result = generateSequence(genome1, "strict", 5, 8, 20)

    writeFile = open("./generatedGenome.txt", "w")
    for subSeq in result:
        writeFile.write(subSeq)
        if(subSeq != result[-1]):
            writeFile.write("\n")
    writeFile.close()