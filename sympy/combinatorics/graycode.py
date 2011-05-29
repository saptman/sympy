from sympy.core import Basic
from sympy.functions import ceiling, log

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

def get_subset_from_bitlist(super_set, bitlist):
    """
    Gets the subset defined by the bitlist.

    Examples:
    >>> from sympy.combinatorics.graycode import get_subset_from_bitlist
    >>> get_subset_from_bitlist(['a','b','c','d'],['0','0','1','1'])
    ['c', 'd']
    """
    if len(super_set) != len(bitlist):
        raise ValueError("The sizes of the lists are not equal")
    ret_set = super_set[:]
    for i in xrange(len(bitlist)):
        if bitlist[i] == '0':
            ret_set.remove(super_set[i])
    return ret_set

def get_bitlist_from_subset(subset, superset):
    """
    Gets the bitlist corresponding to a subset.

    Examples:
    >>> from sympy.combinatorics.graycode import get_bitlist_from_subset
    >>> get_bitlist_from_subset(['c','d'],['a','b','c','d'])
    ['0', '0', '1', '1']
    """
    bitlist = ['0'] * len(superset)
    for i in subset:
        bitlist[superset.index(i)] = '1'
    return bitlist

def gray_code_subsets(gray_code_set):
    """
    Generates the subsets as enumerated
    by a Gray code.

    Examples:
    >>> from sympy.combinatorics.graycode import gray_code_subsets
    >>> list(gray_code_subsets(['a','b','c']))
    [[], ['c'], ['b', 'c'], ['b'], ['a', 'b'], ['a', 'b', 'c'], \
    ['a', 'c'], ['a']]
    """
    return [get_subset_from_bitlist(gray_code_set, bitlist) for \
            bitlist in list(GrayCode(len(gray_code_set)).get_next_bitlist())]

def rank_gray_code(code):
    """
    Ranks the gray code.

    Examples:
    >>> from sympy.combinatorics.graycode import rank_gray_code
    >>> rank_gray_code(['1','0','0'])
    1
    >>> rank_gray_code(['1','0','1','0','0'])
    6
    """
    if len(code)==0:
        return 0
    elif code[-1]=='0':
        return rank_gray_code(code[:-1])
    else:
        return 2**len(code) - rank_gray_code(code[:-1]) -1

def unrank_gray_code(k, n):
    """
    Unranks an n-bit sized gray code of rank k.

    We generate in reverse order to allow for tail-call
    optimization.

    Examples:
    >>> from sympy.combinatorics.graycode import unrank_gray_code, \
    rank_gray_code
    >>> unrank_gray_code(3, 5)
    ['0', '1', '0', '0', '0']
    >>> rank_gray_code(unrank_gray_code(7, 10))
    7
    """
    def unrank(k, n):
        if n == 1:
            return [str(k % 2)]
        m = 2**(n - 1)
        if k < m:
            return ["0"] + unrank(k, n - 1)
        return ["1"] + unrank(m - (k % m) - 1, n - 1)
    ret_list = unrank(k, n)
    list.reverse(ret_list)
    return ret_list
