from pysmt.shortcuts import Symbol, And, GE, LT, Plus, Equals, Int, get_model
from pysmt.typing import INT


def GraphToClause(edges):

    edgeMap = {}
    clause = []

    for edge in edges:
        var = "X" + str(edge.v1) + str(edge.v2)



if __name__ == "__main__":
    v = 1