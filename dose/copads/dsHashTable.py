"""
Data Structure: Hash Table.
Date created: 30th January 2021
Licence: Python Software Foundation License version 2

Implemented from https://runestone.academy/runestone/books/published/pythonds/SortSearch/Hashing.html#implementing-the-map-abstract-data-type
"""
import typing

class HashTable(object):
    def __init__(self):
        self.size: int = 11
        self.slots: list = [None] * self.size
        self.data: list = [None] * self.size

    def put(self, key: int, data) -> None:
        hash_value: int = self.hash_function(key, len(self.slots))

        if self.slots[hash_value] is None:
            self.slots[hash_value] = key
            self.data[hash_value] = data
        else:
            if self.slots[hash_value] == key:
                self.data[hash_value] = data  # replace
            else:
                next_slot = self.rehash(hash_value, len(self.slots))
                while self.slots[next_slot] is not None and \
                        self.slots[next_slot] != key:
                    next_slot = self.rehash(next_slot, len(self.slots))

                if self.slots[next_slot] is None:
                    self.slots[next_slot] = key
                    self.data[next_slot] = data
                else:
                    self.data[next_slot] = data  # replace

    @staticmethod
    def hash_function(key: int, size: int) -> int:
        return key % size

    @staticmethod
    def rehash(old_hash: int, size: int) -> int:
        return (old_hash + 1) % size

    def get(self, key: int) -> typing.Union[None, str]:
        start_slot: int = self.hash_function(key, len(self.slots))

        data: typing.Union[None, str] = None
        stop: bool = False
        found: bool = False
        position: int = start_slot
        while self.slots[position] is not None and \
                not found and not stop:
            if self.slots[position] == key:
                found: bool = True
                data: typing.Union[None, str] = self.data[position]
            else:
                position: int = self.rehash(position, len(self.slots))
                if position == start_slot:
                    stop: bool = True
        return data

    def __getitem__(self, key: int) -> typing.Optional[str]:
        return self.get(key)

    def __setitem__(self, key: int, data: typing.Union[None, str]) -> None:
        self.put(key, data)
