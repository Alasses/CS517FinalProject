import os
import numpy as np
import difflib



reads = ['tagg', 'catt', 'gga', 'tta', 'gagtat']

class Graph():
    '''
    Constructs a directed (asymmetric) graph with nodes
    as the individual reads/small strings of the genome
    and weights calculated based on the overlap between
    the strings.
    Parameters:
    reads: (list) of small strings also known as reads.
    Output:
    adjacency_dict : (dict) keys are individual elements
    of the `reads` list and values are another (dict) 
    with its keys as the `reads` and values as the `weights`
    of the graph.
    This is similar to adjacency matrix but in (dict) format
    for easy access.
    '''
    def __init__(self, reads):
        self.reads = reads # vertices
        self.source = ""   # special 'source' vertex
        self.reads.append(self.source)
        self.adjacency_dict = {}
        for k in self.reads:
            self.adjacency_dict[k] = {}

    def _get_overlap(self, str_i, str_j):
        '''
            intersection between last k characters
            of `str_i` and first k characters of 
            `str_j`, where k <= min(len(str_i),len(str_j))
        '''
        s = difflib.SequenceMatcher(None, str_i, str_j)
        pos_a, pos_b, size = s.find_longest_match(0, len(str_i), 0, len(str_j)) 
        return len(str_i[pos_a:pos_a+size]), str_j[pos_b:pos_b+size] 

    def _get_weight(self, str_i, str_j):
        overlap_len, overlap_str = self._get_overlap(str_i, str_j)
        if not str_j.startswith(overlap_str):
            overlap_len = 0

        return len(str_j) - overlap_len

    def _construct_graph(self):
        for i in self.adjacency_dict.keys():
            for j in self.adjacency_dict.keys():
                if i is not j:
                    if i is self.source:
                        self.adjacency_dict[i][j] = len(j)
                    elif j is self.source:
                        self.adjacency_dict[i][j] = 0
                    else:
                        self.adjacency_dict[i][j] = self._get_weight(i, j)

if __name__ == "__main__":
    g = Graph(reads)
    g._get_overlap(g.reads[0], g.reads[2])
    g._construct_graph()