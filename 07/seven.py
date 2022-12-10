class DirTreeNode:
    def __init__(self, size, parent, name):
        self.name = name
        self._size = int(size)
        self.children = {}
        self.parent = parent

    @property
    def is_root(self):
        return self.parent is None

    @property
    def is_leaf(self):
        return len(self.children) == 0

    @property
    def is_dir(self):
        return not self.is_leaf

    @property
    def size(self):
        if self.is_leaf:
            return self._size
        else:
            return sum([c.size for c in self.children.values()])

    def add_child(self, node):
        self.children[node.name] = node

    def display(self, indent=0):
        if self.is_leaf:
            print(f"{indent*' '}-{self.name} {self.size}")
        else:
            print(f"{indent*' '}dir {self.name} {self.size}")
            for c in self.children.values():
                c.display(indent + 1)

    def get_dir_sizes(self):
        dir_sizes = []
        if self.is_leaf:
            return []
        else:
            dir_sizes.append(self.size)
            for c in self.children.values():
                if c.is_dir:
                    dir_sizes += c.get_dir_sizes()
        return dir_sizes


def build_tree(instructions):
    root_node = DirTreeNode(parent=None, name="/", size=0)
    current_node = root_node
    for line in instructions:
        line = line.strip()
        if line.startswith("$ cd"):
            if line.split(" ")[2] == "..":
                current_node = current_node.parent
            elif not (directory := line.split(" ")[2]) == "/":
                current_node = current_node.children[directory]
        if line.startswith("dir"):
            node = DirTreeNode(parent=current_node, size=0, name=line.split(" ")[1])
            current_node.children[node.name] = node
        if line[0].isdigit():
            node = DirTreeNode(
                parent=current_node, size=line.split(" ")[0], name=line.split(" ")[1]
            )
            current_node.children[node.name] = node

    return root_node


def print_tree(root: DirTreeNode):
    root.display()


def get_sum_for_dirs(dir_size_limit, dirs):
    return sum([d for d in dirs if d <= dir_size_limit])


def get_smalles_big_nuff_dir_size(min_dir_size, dirs):
    return min([dir for dir in dirs if dir > min_dir_size])


if __name__ == "__main__":
    print("tests")
    with open("test_input.dat") as f:
        root = build_tree(f)
        print_tree(root)
        print(get_sum_for_dirs(100000, root.get_dir_sizes()))
        deletion_min_size = abs(70000000 - root.size - 30000000)
        print(get_smalles_big_nuff_dir_size(deletion_min_size, root.get_dir_sizes()))

    print("input")
    with open("input.dat") as f:
        root = build_tree(f)
        # print_tree(root)
        print(get_sum_for_dirs(100000, root.get_dir_sizes()))
        deletion_min_size = abs(70000000 - root.size - 30000000)
        print(get_smalles_big_nuff_dir_size(deletion_min_size, root.get_dir_sizes()))
