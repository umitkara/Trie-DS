from __future__ import annotations
from dataclasses import dataclass
from typing import Dict

"""
Trie data structure implementation.

This is a simple implementation of a trie data structure.
API:
    insert(word: str) : None
    search(word: str) : bool
    keys_with_prefix(prefix: str) : list[str]
    pretty_print() : None
    
Performance:
n = number of words, m = length of longest word
    insert: O(n)
    search: O(n)
    keys_with_prefix: O(n+m) on average
"""


@dataclass
class TrieNode:
    is_word: bool
    children: Dict[str, TrieNode]


class Trie:
    def __init__(self):
        self.root = TrieNode(False, {})

    def insert(self, word: str):
        """
        Insert a word into the trie.
        """
        node = self.root
        for letter in word:
            if letter not in node.children:
                node.children[letter] = TrieNode(False, {})
            node = node.children[letter]
        node.is_word = True

    def search(self, word: str) -> bool:
        """
        Search for a word in the trie.
        """
        node = self.root
        for letter in word:
            if letter not in node.children:
                return False
            node = node.children[letter]
        return node.is_word

    def keys_with_prefix(self, prefix: str) -> list[str]:
        node = self.root
        for letter in prefix:
            if letter not in node.children:
                return []
            node = node.children[letter]
        return self.get_words(node, prefix)

    def get_words(self, node: TrieNode, prefix: str) -> list[str]:
        words = []
        temp_word = prefix
        if node.is_word:
            words.append(temp_word)
        for letter, child in node.children.items():
            temp_word += letter
            words += self.get_words(child, temp_word)
            temp_word = temp_word[:-1]
        return words

    def pretty_print(self):
        """
        Print the trie in a pretty format.
        """
        def print_node(node: TrieNode, level: int = 0):
            for letter, child in node.children.items():
                print(" " * level + "└── " + letter, end="")
                if child.is_word:
                    print(" (word)")
                else:
                    print()
                print_node(child, level + 1)
        print_node(self.root, 0)


def main():
    trie = Trie()
    trie.insert("an")
    trie.insert("and")
    trie.insert("ant")
    trie.insert("anthem")
    trie.insert("anti")
    trie.insert("antidote")
    trie.insert("antonym")
    trie.insert("antipathy")
    trie.insert("any")
    trie.insert("anybody")
    trie.insert("anyhow")
    trie.insert("anyone")
    print(trie.keys_with_prefix("ant"))
    trie.pretty_print()


if __name__ == "__main__":
    main()
