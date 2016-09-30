#!/usr/bin/env python
# -*- coding: utf-8 -*-

from io import open

from unitex import *

_LOGGER = logging.getLogger(__name__)



class FSAConstants:

    EPSILON = "<E>"

    DEPTH_FIRST_SEARCH = "dfs"
    BREADTH_FIRST_SEARCH = "bfs"



class Edge:

    def __init__(self, label, targets=None, source=None):
        self.__label = label

        self.__source = source

        self.__targets = targets
        if self.__targets is not None:
            self.__tids = set([target.get_id() for target in targets])

    def __len__(self):
        return len(self.__targets)

    def __str__(self):
        return self.get_label()

    def __hash__(self):
        return hash(self.get_label())

    def __cmp__(self, e):
        return cmp(self.get_label(), self.get_label())

    def __iter__(self):
        for target in self.__targets:
            yield target

    def __contains__(self, target):
        return True if target.get_id() in self.__tids else False

    def __getitem__(self, i):
        return self.__targets[i]

    def get_label(self):
        return self.__label

    def get_source(self):
        return self.__source

    def set_source(self, source):
        self.__source = source

    def get_targets(self):
        return self.__targets

    def set_targets(self, targets):
        self.__targets = targets
        self.__tids = set([target.get_id() for target in targets])

    def add_target(self, target):
        if target.get_id() in self.__tids:
            return
        self.__targets.append(target)

    def del_target(self, target):
        if target.get_id() not in self.__tids:
            return

        self.__tids.remove(target.get_id())

        for i in range(len(self.__targets)):
            _target = self.__targets[i]
            if _target.get_id() == target.get_id():
                del self.__targets[i]
                break



class Node:

    def __init__(self, _id, final=False):
        self.__id = _id

        self.__final = final
        self.__edges = {}

        self.__depth = 0

        self.__visited = False

    def __len__(self):
        return len(self.__edges)

    def __contains__(self, label):
        return label in self.__edges

    def __getitem__(self, label):
        return self.__edges.get(label, None)

    def __iter__(self):
        for label in self.__edges:
            yield label

    def __str__(self):
        s = "NODE[%s]" % str(self.get_id())

        if self.is_final():
            s += " -- FINAL"

        for label in self:
            targets = " | ".join([str(target.get_id()) for target in self[label]])
            s += "\n\t%s -> (%s)" % (label, targets)

        return s

    def get_id(self):
        return self.__id

    def set_id(self, i):
        self.__id = i

    def is_deterministic(self):
        if FSAConstants.EPSILON in self.__edges:
            return False

        for label in self.__edges:
            if len(self[label]) > 1:
                return False

        return True

    def exists(self, label, node=None):
        if not label in self:
            return False

        if node is not None and node not in self[label]:
            return False

        return True

    def add(self, label, target):
        if self.exists(label, target) is True:
            return

        if self.exists(label) is False:
            edge = Edge(label, [target], self)
            self.__edges[label] = edge
        else:
            self[label].add_target(target)

    def delete(self, label, node=None):
        if not self.exists(label, node):
            raise UnitexException("Edge not found: %s" % label)

        if node is None:
            del self.__edges[label]
        else:
            self[label].del_target(node)

    def set_depth(self, depth):
        self.__depth = depth

    def get_depth(self):
        return self.__depth

    def is_visited(self):
        return self.__visited

    def set_visited(self, visited=True):
        self.__visited = visited

    def is_final(self):
        return self.__final

    def set_final(self, final=True):
        self.__final = final



class NodeSets:

    def __init__ (self):
        self.__sets = {}

    def __getitem__(self, _id):
        return self.__sets[_id]

    def __contains__(self, s):
        return s in self.all()

    def __iter__ (self):
        return iter(self.all())

    def all(self):
        return set([tuple(l) for l in self.__sets.values()])

    def add(self, s):
        _set = tuple(sorted(set(s)))
        for _id in s:
            self.__sets[_id] = _set



class Automaton:

    def __init__(self, name="Automaton"):
        self.__name = name

        self.__nodes = []

        self.__initial = 0
        self.__finals = []

        self.__nodes.append(Node(self.__initial, False))

    def __len__(self):
        return len(self.__nodes)

    def __getitem__(self, _id):
        try:
            return self.__nodes[_id]
        except IndexError:
            return None

    def __iter__(self):
        for node in self.__nodes:
            yield node

    def __str__(self):
        title = "# FSA -- %s #" % self.get_name()

        s = "%s\n%s\n%s\n\n" % ("#" * len(title), title, "#" * len(title))

        for node in self:
            s += "%s\n\n" % node

        return s

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_depth(self):
        depth = 0
        for nid in self.__finals:
            final = self.__nodes[nid]

            if final.get_depth() > depth:
                depth = final.get_depth()

        return depth

    def get_initial(self):
        return self.__initial

    def set_initial(self, initial):
        self.__initial = initial

    def get_finals(self):
        return self.__finals

    def set_finals(self, finals):
        self.__finals = finals

    def get_nodes(self):
        return self.__nodes

    def set_nodes(self, nodes):
        self.__nodes = nodes

    def add_edge(self, label, sid, tid):
        source = self[sid]
        target = self[tid]

        target.set_depth(source.get_depth() + 1)

        source.add(label, target)

    def add_node(self, initial=False, final=False):
        if initial is True:
            return self.__initial
        elif final is True:
            self.__finals.append(len(self.__nodes))
            self.__nodes.append(Node(self.__finals[-1], True))
            return self.__finals[-1]

        nid = len(self.__nodes)

        self.__nodes.append(Node(nid, final))

        return nid

    def add_path(self, path):
        if len(path) == 0:
            raise UnitexException("Empty path!")
        sid = self.add_node(initial=True, final=False)

        for label in path[:-1]:
            tid = self.add_node(initial=False, final=False)
            self.add_edge(label, sid, tid)

            sid = tid
        else:
            self.add_edge(path[-1], sid, self.add_node(initial=False, final=True))

    def get_alphabet(self):
        alphabet = set()

        for node in self:
            for label in node:
                alphabet.add(label)

        return tuple(alphabet)

    def is_deterministic(self):
        for node in self:
            if not node.is_deterministic():
                return False
        return True

    def __closure(self, nid):
        stack = [nid]
        result = set(stack)

        while len(stack) > 0:
            current = stack.pop()

            if FSAConstants.EPSILON in self[current]:
                edge = self[current][FSAConstants.EPSILON]
                if edge not in result:
                    stack.append(edge)
                    result.add(edge)

        return tuple(result)

    def determinize(self):
        dfa = Automaton("DETERMINIZED(%s)" % self.get_name())

        alphabet = self.get_alphabet()

        initials = self.__closure(self.get_initial())

        hid = dfa.add_node(initial=True, final=False)

        visited = {}
        visited[initials] = hid

        stack = [initials]
        while len(stack) > 0:
            current = stack.pop()

            for label in alphabet:
                new = set()
                for node in current:
                    if not label in self[node]:
                        continue
                    for next in self[node][label]:
                        new.update(self.__closure(next.get_id()))
                new = tuple(new)

                if len(new) == 0:
                    continue

                if new not in visited:
                    stack.append(new)

                    final = True in [self[_id].is_final() for _id in new]
                    nid = dfa.add_node(final=final)

                    visited[new] = nid

                dfa.add_edge(label, visited[current], visited[new])

        self.set_name(dfa.get_name())

        self.set_initial(dfa.get_initial())
        self.set_finals(dfa.get_finals())

        self.set_nodes(dfa.get_nodes())

    def minimize(self):
        min = Automaton("MINIMIZED(%s)" % self.get_name())

        alphabet = self.get_alphabet()

        nodetoset = {}
        settonode = {}

        sets = NodeSets()

        rest, final = [], []
        for node in self:
            if node.is_final():
                final.append(node.get_id())
            else:
                rest.append(node.get_id())

        sets.add(rest)
        sets.add(final)

        stack = [s for s in sets if len(s) > 1]

        def target_set(_id, label):
            edge = self[_id][label]

            if edge is None:
                return None
            else:
                return sets[edge[0].get_id()]

        while len(stack) > 0:
            current = stack.pop()

            for label in alphabet:
                target = target_set(current[0], label)

                one, two = [current[0]], []
                for _id in current[1:]:
                    if target_set(_id, label) == target:
                        one.append(_id)
                    else:
                        two.append(_id)

                if len(two) > 0:
                    sets.add(one)
                    sets.add(two)

                    if len(one) > 1:
                        stack.append(one)
                    if len(two) > 1:
                        stack.append(two)

                    break

        for s in sets:
            initial = self.get_initial() in s
            final = True in [self[_id].is_final() for _id in s]

            _id = min.add_node(initial=initial, final=final)

            nodetoset[_id] = s
            settonode[s] = _id

        for node in min:
            done = set()

            s = nodetoset[node.get_id()]

            source = self[s[0]]
            for label in source:
                edge = source[label]

                if label in done:
                    continue
                done.add(label)

                for target in edge:
                    t = sets[target.get_id()]
                    min.add_edge(label, node.get_id(), settonode[t])

        self.set_name(min.get_name())

        self.set_initial(min.get_initial())
        self.set_finals(min.get_finals())

        self.set_nodes(min.get_nodes())

    def reset(self):
        for node in self:
            node.set_visited(False)

    def __expand(self, source):
        L = []

        source.set_visited(True)
        for label in source:
            edge = source[label]
            for target in source[label]:
                L.append((edge.get_label(), source.get_id(), target.get_id()))

        return L

    def iter(self, iter_type=None):
        if iter_type is None:
            iter_type = FSAConstants.BREADTH_FIRST_SEARCH

        if len(self[self.get_initial()]) == 0:
            raise UnitexException("Empty FSA")

        i = None
        if iter_type == FSAConstants.DEPTH_FIRST_SEARCH:
            i = -1
        elif iter_type == FSAConstants.BREADTH_FIRST_SEARCH:
            i = 0
        else:
            raise UnitexException("Unknown iter type: %s" % iter_type)

        root = self[self.get_initial()]
        if root.is_visited():
            self.reset()

        L = self.__expand(root)
        while L:
            edge, sid, tid = L.pop(i)
            yield (edge, sid, tid)

            if not self[tid].is_visited():
                L += self.__expand(self[tid])

    def save(self, file, encoding=None):
        if encoding is None:
            encoding = UnitexConstants.DEFAULT_ENCODING

        with open(file, "w", encoding=encoding) as output:
            output.write("digraph Automaton {\n\n")
            output.write("\tcenter = 1;\n")
            output.write("\tcharset = \"%s\";\n" % encoding)
            output.write("\trankdir = LR;\n")
            output.write("\tranksep = 1;\n")
            output.write("\tedge [arrowhead = vee];\n\n")

            nodes = set()
            edges = set()

            for node in self:
                sid = node.get_id()
                n1 = "node%s" % sid

                if not sid in nodes:
                    nodes.add(sid)

                    if node.get_id() == self.get_initial():
                        output.write("\t%s[shape = circle, label = \"\"];\n" % n1)
                    elif node.is_final():
                        output.write("\t%s[shape = doublecircle, label = \"\"];\n" % n1)
                    else:
                        output.write("\t%s[shape = point, label = \"\"];\n" % n1)

                for label in node:
                    for target in node[label]:
                        if (node.get_id(), label, target.get_id()) in edges:
                            continue
                        edges.add((node.get_id(), label, target.get_id()))

                        tid = target.get_id()
                        n2 = "node%s" % tid

                        if not tid in nodes:
                            nodes.add(tid)

                            if target.get_id() == self.get_initial():
                                output.write("\t%s[shape = circle, label = \"\"];\n" % n2)
                            elif target.is_final():
                                output.write("\t%s[shape = doublecircle, label = \"\"];\n" % n2)
                            else:
                                output.write("\t%s[shape = point, label = \"\"];\n" % n2)

                        output.write("\t%s -> %s [label = \"%s\"];\n" % (n1, n2, label))

                output.write("\n")

            output.write("}\n")
