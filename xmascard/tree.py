
import random

class Tree:

    """ A tree class. Intermediate nodes are stored as lists. Leaves are
    instances of Leaf.
    """

    def __init__(self, data):
        self.data = data
        self.depth = 0
        self._children = []

    def get_leaves(self):
        r = []

        for n in self.foreach_leaf():
            r.append(n)

        return r

    def foreach_leaf(self):

        """ Generator method returning every leaf. """

        if (len(self._children) == 0):
            yield self
        else:
            for n in self._children:
                yield from n.foreach_leaf()

    def add_children(self, *children):

        """ Add children trees to self, also setting their depth. """

        for n in children:
            if (type(n) is not Tree):
                raise TypeError(
                    "Children of Tree must also be Trees, but encountered " + str(type(n)))
            n.depth = self.depth + 1
            self._children.append(n)

    def _get_string(self, indent=0):
        chstr = "[]"

        if (len(self._children) > 0):
            chstr = "["
            first = True

            for n in self._children:
                if (first):
                    first = False
                else:
                    chstr += ", "
                chstr += n._get_string(indent + 1)
            chstr += "]"

        return "{} {}".format(self.data, chstr)

    def __str__(self):
        return self._get_string()
