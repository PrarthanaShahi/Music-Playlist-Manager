# This file contains the implementation of a doubly linked list for the playlist.
import random

# A node for doubly linked list.
class Node:
    """Node for a doubly linked list, containing a song and pointers to next and previous nodes."""
    def __init__(self, song):
        self.song = song
        self.next = None
        self.prev = None

# The Doubly Linked List for the main playlist.
class DoublyLinkedList:
    """A doubly linked list to manage the playlist
        It allows for efficient insertion, deletion, and traversal (next/previous)."""

    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None # Pointer to the currently playing song
        self.size = 0

    def add_song(self,song):
        """Adds a new song to the end of the playlist"""
        new_node = Node(song)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            self.current = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.size += 1

    def remove_song(self, song_title):
        """Removes a song by its title."""
        if not self.head:
            return False
        
        temp = self.head
        while temp:
            if temp.song.title.lower() == song_title.lower():
                # If it's the head node
                if temp.prev is None:
                    self.head = temp.next
                    if self.head:
                        self.head.prev = None
                    else:
                        self.tail = None # The list is now empty
                # If it is the tail node
                elif temp.next is None:
                    temp.prev.next = None
                    self.tail = temp.prev
                # In the middle
                else:
                    temp.prev.next = temp.next
                    temp.next.prev = temp.prev
                
                # Adjust current pointer if the current song is removed
                if self.current == temp:
                    self.current = temp.next if temp.next else temp.prev
                self.size -= 1
                return True
            temp = temp.next
        return False

    def get_next(self):
        """Moves to the next song in the playlist."""
        if self.current and self.current.next:
            self.current = self.current.next
            return self.current.song
        return None

    def get_previous(self):
        """Moves to the previous song in the playlist."""
        if self.current and self.current.prev:
            self.current = self.current.prev
            return self.current.song
        return None
        
    def shuffle(self):
        """Shuffles the playlist recursively.
        It converts the list to an array, shuffles it, and then rebuilds the linked list."""
        
        if self.size <= 1:
            return

        # Convert linked list to a Python list for easy shuffling
        song_list = []
        temp = self.head
        while temp:
            song_list.append(temp.song)
            temp = temp.next
        
        # Recursive shuffle algorithm
        def recursive_shuffle(arr):
            n = len(arr)
            if n <= 1:
                return arr
            
            # Divide the array in half
            mid = n // 2
            left = recursive_shuffle(arr[:mid])
            right = recursive_shuffle(arr[mid:])
            
            # Combine the shuffled halves
            shuffled_arr = []
            while left and right:
                if random.random() < 0.5:
                    shuffled_arr.append(left.pop(0))
                else:
                    shuffled_arr.append(right.pop(0))
            shuffled_arr.extend(left)
            shuffled_arr.extend(right)
            return shuffled_arr
            
        shuffled_songs = recursive_shuffle(song_list)
        
        # Rebuild the linked list from the shuffled list
        self.head = None
        self.tail = None
        self.current = None
        for song in shuffled_songs:
            self.add_song(song)
        # Reset current pointer to the new head
        self.current = self.head