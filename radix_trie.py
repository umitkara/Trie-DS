from __future__ import annotations
from dataclasses import dataclass
from typing import Dict


"""
Radix Trie(aka Radix Tree or Patricia Tree) implementation.

API:
    insert(word: str) : None
    search(word: str) : bool
    remove(word: str) : None
    longestPrefix(word: str) : str
    keysWithPrefix(prefix: str) : list[str]
    pretty_print() : None
"""


@dataclass
class RTEdge:
    """
    Edge of a Radix Trie.
    
    Attributes:
        label: Character or string of characters that represents the edge. The labal holds the information in this implementation.
               A label holds at least one character. If the destination node is a key node, leaf, the label and it's ancestors unite to form a word.
        destination: Node that is the destination of the edge.
    """
    destination: RTNode
    label: str


@dataclass
class RTNode:
    """
    Radix Trie node.
    
    Attributes:
        children: Dictionary of edges. The keys are the characters of the label of the edge. The values are the edges.
                  Dictionary is chosen because of its performance in practice.
        key_node: If the node is a key node, the key_node is the node that holds the word.
    """
    key_node: bool
    children: Dict[str, RTEdge]


class RadixTrie:
    def __init__(self):
        self.root = RTNode(False, {})
    
    def search(self, node: RTNode, word: str) -> bool:
        """
        Search for a word in the trie.

        Args:
            node (RTNode): The node to start searching from.
            word (str): The word to search for.

        Returns:
            bool: True if the word is found, False otherwise.
        """
        if word == '':
            # if word is empty recusion completed. return the key_node of the node.
            return node.key_node
        # match the first edge of the word to the node.
        (edge, commonPrefix, word_suffix, edge_suffix) = self._matchEdge(node, word)
        if edge is not None and edge_suffix == "":
            # if there is a common prefix between edge and word, and there are no remaining suffixes,
            # edge is a part of the word. We look for the word in the subtree of the edge.
            return self.search(node.children[commonPrefix].destination, word_suffix)
        else:
            return False

    def _matchEdge(self, node: RTNode, word: str):
        """
        Match the first edge of the word to the node.
        """
        c = word[0]
        if c not in node.children:
            # if first character of word is not in the node, there is no common prefix.
            return (None, "", word, "")
        else:
            # if first character of word is in the node, we match the edge.
            edge = node.children[c]
            # find the longest common prefix of the edge and the word.
            prefix, word_suffix, edge_suffix = self._longestCommonPrefix(word, edge.label)
            return (edge, prefix, word_suffix, edge_suffix)

    def _longestCommonPrefix(self, word: str, edge: str):
        """
        Find the longest common prefix of two strings.
        """
        i = 0
        while i < len(word) and i < len(edge) and word[i] == edge[i]:
            i += 1
        return (word[:i], word[i:], edge[i:])

    def insert(self, node: RTNode, word:str):
        """
        Insert a word into the trie.

        Args:
            node (RTNode): The node to start inserting from.
            word (str): The word to insert.
        """
        if word == "":
            # if word is empty, recursion completed. Set the key_node of the node to True.
            node.key_node = True
        else:
            # match the first edge of the word to the node.
            (edge, commonPrefix, word_suffix, edge_suffix) = self._matchEdge(node, word)
            if edge is None:
                # if there is no common prefix between edge and word, we create a new edge.
                edge = RTEdge(RTNode(True, {}), word)
                # add the edge to the node.
                node.children[word[0]] = edge
            elif edge_suffix == "":
                # if there is a common prefix between edge and word, and there are no remaining suffixes,
                # edge is a part of the word. We insert the word in the subtree of the edge.
                self.insert(edge.destination, word_suffix)
            else:
                # if there is a common prefix between edge and word, and there are remaining suffixes on the edge's label,
                # we split the edge. We create a bridge node to connect common prefix and remaining suffixes.
                bridge = RTNode(False, {})
                edge = RTEdge(bridge, commonPrefix)
                # update the edge's destination to the bridge node.
                node.children[word[0]] = edge
                # insert the remaining suffixes of the edge's label into the bridge node.
                bridge.children[edge_suffix[0]] = RTEdge(RTNode(False, {}), edge_suffix)
                # insert the remaining suffixes of the word into the bridge node.
                self.insert(bridge, word_suffix)

    def remove(self, node: RTNode, word:str):
        """
        Remove a word from the trie.
        
        Args:
            node (RTNode): The node to start inserting from.
            word (str): The word to insert.
        """
        if word == "":
            # if the word is empty, recursion completed. Set the key_node of the node to False to mark it as an intermediate node.
            node.key_node = False
            # return that the operation was successful and if this node is to be pruned
            return (True, len(node.children) == 0)
        else:
            # check if there is an edge with the first character of the word.
            (edge, _, word_suffix, edge_suffix) = self._matchEdge(node, word)
            if edge is not None and edge_suffix == "":
                # if there is a common prefix between edge and word, and there are no remaining suffixes,
                # edge is a part of the word. We remove the word from the subtree of the edge.
                dest = edge.destination
                # recursively remove to remove the remaining suffixes of the word.
                (deleted, shouldPrune) = self.remove(dest, word_suffix)
                if deleted:
                    # if the word was deleted, we check if the node should be pruned.
                    if shouldPrune:
                        # if the node is leaf and has no children, we prune it.
                        node.children.pop(word[0])
                    elif self._isPassThrough(dest, node):
                        # if the node is pass through, we compress it to a single edge.
                        next_edge = self._getPassThroughEdge(dest)
                        new_edge = RTEdge(next_edge.destination, edge.label+next_edge.label)
                        node.children[word[0]] = new_edge
                return (deleted, False)
            else:
                # if word is not in the trie, we return False.
                return (False, False)
    
    def _isPassThrough(self, node: RTNode, parent: RTNode):
        """
        Check if the node is a pass through node.
        """
        if node.key_node == False and len(node.children) == 1:
            return True
        return False
    
    def _getPassThroughEdge(self, node: RTNode):
        """
        Get the edge that is a pass through node.
        """
        for edge in node.children.values():
            return edge
        return None

    def longestPrefix(self, word: str):
        """
        Find the longest common prefix of two strings.
        """
        return self._longestCommonPrefix(word, word)[0]
    
    def searchNodeWithPrefix(self, node: RTNode, word: str) -> RTNode:
        """
        Search for a node with a given prefix.
        """
        if word == "":
            return node
        (edge, _, word_suffix, edge_suffix) = self._matchEdge(node, word)
        if edge is None:
            return None
        elif edge_suffix == "":
            return self.searchNodeWithPrefix(edge.destination, word_suffix)
        elif word_suffix == "":
            return edge.destination
        else:
            return None
        
    def pretty_print(self):
        """
        Print the trie in a pretty format.
        """
        def print_node(node: RTNode, level: int = 0):
            for _, edge in node.children.items():
                print(" " * level + "└── " + edge.label, end="")
                if node.key_node == True:
                    print(" (word)")
                else:
                    print()
                print_node(edge.destination, level + 1)
        print_node(self.root, 0)
    
    def print_nodes(self, node:RTNode):
        """
        Print the nodes of the trie.
        """
        for _, edge in node.children.items():
            print(edge.label)
            self.print_nodes(edge.destination)


def main():
    trie = RadixTrie()
    trie.insert(trie.root, "an")
    trie.insert(trie.root, "and")
    trie.insert(trie.root, "ant")
    trie.insert(trie.root, "anthem")
    trie.insert(trie.root, "anti")
    trie.insert(trie.root, "antidote")
    trie.insert(trie.root, "antonym")
    trie.insert(trie.root, "antipathy")
    trie.insert(trie.root, "any")
    trie.insert(trie.root, "anybody")
    trie.insert(trie.root, "anyhow")
    trie.insert(trie.root, "anyone")
    trie.pretty_print()
    # trie.remove(trie.root, "antidote")
    # trie.pretty_print()
    same_prefix = trie.searchNodeWithPrefix(trie.root, "ant")
    trie.print_nodes(same_prefix)
    
if __name__ == "__main__":
    main()
