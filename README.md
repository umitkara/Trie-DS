# Trie (Prefix Tree)

Trie is a data structure that is used to store a set of strings, where each string is a sequence of characters.

It is a k-ary search tree, a tree data structure used for locating specific keys from within a set.

In this repo i tried to implement **Trie** and **Radix Trie** data structures in Python with an efficient way.

API of Trie:

```python
insert(word: str) : None
search(word: str) : bool
keys_with_prefix(prefix: str) : list[str]
pretty_print() : None
```

API of Radix Trie:

```python
insert(word: str) : None
search(word: str) : bool
remove(word: str) : None
longestPrefix(word: str) : str
keysWithPrefix(prefix: str) : list[str]
pretty_print() : None
```

The trie data structure holds the string as a sequence of characters in a tree. Every node of the tree represents a character in the string and the leaf nodes represent the end of the string.

The radix trie data structure is also a trie but instead of storing every charter in different nodes, it compresses the charters that has only one child. With this way we gain some performance in practice.

## Applications of Trie

- Autocomplete
- Spell Checkers
- String similarity search
- String sorting
- T9 predictive text search