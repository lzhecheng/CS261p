from SNode import *


class SplayTree:
    root = None
    empty = True
    counter = 0
    height = 0

    def __init__(self):
        self.empty = True

    def rotate_right(self, parent):
        self.counter += 1
        # mark parent's parent
        pp = parent.parent
        if pp is not None:
            lor = parent is pp.rightChild

        # rotate
        v = parent.leftChild
        parent.leftChild = v.rightChild
        if parent.leftChild is not None:
            parent.leftChild.parent = parent
        v.rightChild = parent
        parent.parent = v

        # update v's parent
        if pp is not None:
            v.parent = pp
            if lor:
                pp.rightChild = v
            else:
                pp.leftChild = v
        else:
            self.root = v
            v.parent = None

    def rotate_left(self, parent):
        self.counter += 1
        # mark parent's parent
        pp = parent.parent
        if pp is not None:
            lor = parent is pp.rightChild

        # rotate
        v = parent.rightChild
        parent.rightChild = v.leftChild
        if parent.rightChild is not None:
            parent.rightChild.parent = parent
        v.leftChild = parent
        parent.parent = v

        # update parent
        if pp is not None:
            v.parent = pp
            if lor:
                pp.rightChild = v
            else:
                pp.leftChild = v
        else:
            self.root = v
            v.parent = None

    def splay(self, node):
        self.counter += 1
        if node is None:
            return
        while node.parent is not None:
            self.counter += 1
            if node.parent.parent is None:
                # zig
                if node is node.parent.leftChild:
                    self.rotate_right(node.parent)
                else:
                    self.rotate_left(node.parent)
            elif node is node.parent.leftChild and node.parent is node.parent.parent.leftChild:
                # zig-zig left
                self.rotate_right(node.parent.parent)
                self.rotate_right(node.parent)
            elif node is node.parent.rightChild and node.parent is node.parent.parent.rightChild:
                # zig-zig right
                self.rotate_left(node.parent.parent)
                self.rotate_left(node.parent)
            elif node is node.parent.rightChild and node.parent is node.parent.parent.leftChild:
                # zig-zag left
                self.rotate_left(node.parent)
                self.rotate_right(node.parent)
            elif node is node.parent.leftChild and node.parent is node.parent.parent.rightChild:
                # zig-zag right
                self.rotate_right(node.parent)
                self.rotate_left(node.parent)

    def search(self, k):
        results = [None] * 2
        self.counter = 1
        node = self.root
        if self.root is not None:
            last = node
            while node is not None:
                self.counter += 1
                last = node
                if k < node.value:
                    node = node.leftChild
                elif k > node.value:
                    node = node.rightChild
                else:
                    break
            if node is not None:
                self.splay(node)
            else:
                self.splay(last)
        results[0] = True if node is not None else False
        results[1] = self.counter
        return results

    def insert(self, k):
        results = [None] * 2
        self.counter = 1
        new_node = SNode(k, None)
        if self.root is None:
            self.empty = False
            self.root = new_node
        else:
            # insert new node
            node = self.root
            parent = None
            lor = 0
            h1 = True
            h = 0
            while node is not None:
                h += 1
                self.counter += 1
                parent = node
                if k < node.value:
                    lor = 0
                    node = node.leftChild
                elif k > node.value:
                    lor = 1
                    node = node.rightChild
                else:
                    # already exist
                    h1 = False
                    break
            self.height = max(self.height, h)
            if h1:
                # on the left or right side of parent
                if lor == 0:
                    parent.leftChild = new_node
                else:
                    parent.rightChild = new_node
                new_node.parent = parent

                # splay
                self.splay(new_node)
            else:
                self.splay(node)
        results[1] = self.counter
        return results

    def delete(self, k):
        results = [None] * 2
        self.counter = 1
        success = False
        if self.root is not None:
            node = self.root
            last = None
            while node is not None:
                self.counter += 1
                last = node
                if k < node.value:
                    node = node.leftChild
                elif k > node.value:
                    node = node.rightChild
                else:
                    success = True
                    break
            if success:
                # find it, then delete it
                p = node.parent
                self.true_delete(node)
                self.splay(p)
            else:
                self.splay(last)
        results[0] = success
        results[1] = self.counter
        return results

    def true_delete(self, node):
        self.counter += 1
        # if it is the root
        is_root = False
        dummy = SNode(0, None)
        if node.parent is None:
            is_root = True
            dummy.leftChild = node
            node.parent = dummy

        # 3 cases
        if node.leftChild is None and node.rightChild is None:
            # if node is a leaf node
            if node is node.parent.leftChild:
                node.parent.leftChild = None
            else:
                node.parent.rightChild = None
        else:
            # if node is not a leaf node
            lor = node is node.parent.rightChild
            parent = node.parent
            if node.leftChild is None and node.rightChild is None:
                if node is node.parent.leftChild:
                    node.parent.leftChild = None
                else:
                    node.parent.rightChild = None
            elif node.leftChild is not None and node.rightChild is None:
                if not lor:
                    parent.leftChild = node.leftChild
                    parent.leftChild.parent = parent
                else:
                    parent.rightChild = node.leftChild
                    parent.rightChild.parent = parent
            elif node.leftChild is None and node.rightChild is not None:
                if not lor:
                    parent.leftChild = node.rightChild
                    parent.leftChild.parent = parent
                else:
                    parent.rightChild = node.rightChild
                    parent.rightChild.parent = parent
            else:
                # find the max one in left subtree
                max_left = node.leftChild
                while max_left.rightChild is not None:
                    self.counter += 1
                    max_left = max_left.rightChild
                node.value = max_left.value
                self.true_delete(max_left)

        # if it is the root, remove dummy
        if is_root:
            dummy.leftChild.parent = None
