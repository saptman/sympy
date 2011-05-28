from sympy.core import Basic

import random

class GrayCode(Basic):
    """
    A Gray code is essentially a Hamiltonian walk on
    a n-dimensional cube with edge length of one.
    The vertices of the cube are represented by vectors
    whose values are binary. The Hamilton walk visits
    each vertex exactly once. The Gray code for a 3d
    cube is [[0,0,0],[1,0,0],[1,1,0],[0,1,0],[0,1,1],
    [1,1,1],[1,0,1],[0,0,1]].

    The Gray code solves the problem of sequentially
    generating all possible subsets of n objects in such
    a way that each subset is obtained from the previous
    one by either deleting or adding a single object.
    In the above example, 1 indicates that the object is
    present, and 0 indicates that its absent.

    Gray codes have applications in statistics as well when
    we want to compute various statistics related to subsets
    in an efficient manner.

    References:
    [1] Nijenhuis,A. and Wilf,H.S.(1978).
    Combinatorial Algorithms. Academic Press.
    [2] Knuth, D. (2011). The Art of Computer Programming, Vol 4
    Addison Wesley
    """

    reset = False

    def __new__(cls, *args, **kw_args):
        return Basic.__new__(cls, *args, **kw_args)

    @property
    def count_selections(self):
        """
        Returns the number of bit vectors in the
        Gray code.

        Examples:
        >>> from sympy.combinatorics.graycode import GrayCode
        >>> a = GrayCode(3)
        >>> a.count_selections
        8
        """
        return len(list(self.get_next_bitlist()))

    @property
    def get_n(self):
        """
        Returns the number of objects.

        Examples:
        >>> from sympy.combinatorics.graycode import GrayCode
        >>> a = GrayCode(5)
        >>> a.get_n
        5
        """
        return self.args[0]

    def get_next_bitlist(self):
        """
        Gets the next bit list in the
        sequence of Gray code.

        Examples:
        >>> from sympy.combinatorics.graycode import GrayCode
        >>> a = GrayCode(3)
        >>> list(a.get_next_bitlist())
        [['0', '0', '0'], ['0', '0', '1'], ['0', '1', '1'], \
        ['0', '1', '0'], ['1', '1', '0'], ['1', '1', '1'], \
        ['1', '0', '1'], ['1', '0', '0']]
        """
        bits = self.args[0]
        graycode = 0
        for i in xrange(1 << bits):
            retlist = list(bin(graycode))[2:]
            yield ['0'] * (self.get_n - len(retlist)) + retlist
            bbtc = i ^ (i + 1)
            gbtc = bbtc ^ (bbtc >> 1)
            graycode = graycode ^ gbtc

def random_bitlist(n):
    """
    Generates a random bitlist.
    """
    return [random.randint(0, 1) for i in xrange(n)]
