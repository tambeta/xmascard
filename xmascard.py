#!/usr/bin/env python3

import random
from warnings import warn

from PIL import Image, ImageDraw
from xmascard import Tree

N_ITERATIONS        = 950
DEF_IMAGE_W         = 640
DEF_IMAGE_H         = 480
BORDER_W            = 2
BALANCE_LAMBDA      = 0.75
RANDSEED            = None
SPECIAL_COLOR_RATIO = 0.035
FILL_COLOR          = None

PALETTE_MODERN      = (("#DBC999", "#96A735", "#526C2D"), ("#F83D14",))
PALETTE_HIPSTER     = (("#A7ECA5", "#FFFFFF"), ("#B41F23", "#F7C5D1"))
PALETTE_PASTEL      = (("#A8E0C4", "#DAD8D8"), ("#FFB3C0",))
PALETTE             = PALETTE_MODERN



class PartitionDimensionError(Exception):
    pass

def partition(tree):

    """ Pick a random leaf from the tree, preferring leaves with lower
    depth to ensure stability, and partition it, i.e. add two children with
    the leaf becoming an intermediate node and the children becoming new
    leaves.
    """

    leaves = tree.get_leaves()
    n_leaves = len(leaves)

    leaves.sort(key=lambda x: x.depth)
    leaf = leaves[int(n_leaves * get_exp_rndval(BALANCE_LAMBDA))]

    (x, y, w, h) = leaf.data["rect"]

    def check_dim(dim):
        min_dim = BORDER_W + 1
        if (dim < min_dim):
            raise PartitionDimensionError("Encountered partition resulting in an " +
                "element with one dimension of size {}, discarding".format(dim))

    if (w > h):
        halfw = w / 2
        check_dim(halfw)
        n1 = Tree({ "rect" : (x, y, halfw, h) })
        n2 = Tree({ "rect" : (x + halfw, y, halfw, h) })
    else:
        halfh = h / 2
        check_dim(halfh)
        n1 = Tree({ "rect" : (x, y, w, halfh) })
        n2 = Tree({ "rect" : (x, y + halfh, w, halfh) })

    leaf.add_children(n1, n2)

def output(tree, fn):
    img = Image.new("RGB", (DEF_IMAGE_W, DEF_IMAGE_H), color=FILL_COLOR)
    draw = ImageDraw.Draw(img)
    colors = PALETTE

    leaves = tree.get_leaves()
    n_leaves = len(leaves)

    for leaf in random.sample(leaves, int(n_leaves * SPECIAL_COLOR_RATIO)):
        leaf.data["special"] = True

    for leaf in leaves:
        (x, y, w, h) = leaf.data["rect"]
        far_x = x + w - (1 + BORDER_W)
        far_y = y + h - (1 + BORDER_W)

        draw.rectangle((x, y, far_x, far_y), fill=
            random.choice(colors[1] if ("special" in leaf.data) else colors[0]))

    img.save(fn)

def get_exp_rndval(_lambda):

    """ Return a value [0 .. 1) from the exponential distribution with a
    given lambda.
    """

    rnd = random.expovariate(_lambda) / 5
    rnd = rnd if (rnd < 1.0) else 1.0 - 1e-6
    return rnd

def main():
    randseed = RANDSEED or random.randint(1, 10000)
    tree = Tree({ "rect" : (0, 0, DEF_IMAGE_W, DEF_IMAGE_H) })
    
    print("Using random seed", randseed)
    random.seed(randseed)

    for i in range(0, N_ITERATIONS):
        try:
            partition(tree)
        except PartitionDimensionError as e:
            warn(e)

    output(tree, "out.png")

main()
