# This file contains the PartyModeQueue class for the Music Playlist Manager.

import heapq

class PartyModeQueue:
    """A priority queue to handle songs in party mode.
    Songs with more upvotes have a higher priority and are played sooner."""

    def __init__(self):
        # A min-heap to store (priority, song) tuples.
       
        self.queue = []
        # A dictionary to quickly find songs in the queue by their title.
        self.song_map = {}

    def enqueue(self, song):
        """Adds a song to the queue with its upvotes as a priority."""
        
        if song.title not in self.song_map:
            new_song = Song(song.title, song.artist)
            new_song.upvotes = song.upvotes
            self.song_map[new_song.title] = new_song
            heapq.heappush(self.queue, (-new_song.upvotes, new_song))
            print(f"'{new_song.title}' added to party mode queue with priority {new_song.upvotes}.")
        else:
            print(f"'{song.title}' is already in the party mode queue.")

    def dequeue(self):
        """Removes and returns the song with the highest priority (most upvotes)."""
        if not self.is_empty():
            # heapq.heappop removes and returns the smallest item from the heap.
           
            priority, song = heapq.heappop(self.queue)
            del self.song_map[song.title]
            return song
        return None
    
    def upvote_song(self, song_title):
        """Increases the upvote count of a song in the queue and updates its priority."""
        if song_title in self.song_map:
            # Get the song object from the map
            song = self.song_map[song_title]
            # Increase the upvote count
            song.upvotes += 1
            temp_list = []
            for item in self.queue:
                temp_list.append(item)
            self.queue = []
            
            for priority, s in temp_list:
                if s.title == song_title:
                    heapq.heappush(self.queue, (-s.upvotes, s))
                else:
                    heapq.heappush(self.queue, (priority, s))
            
            print(f"'{song.title}' upvoted. New upvote count: {song.upvotes}")
            return True
        else:
            print(f"'{song_title}' not found in the party mode queue.")
            return False

    def is_empty(self):
        """Checks if the priority queue is empty."""
        return len(self.queue) == 0

    def view_queue(self):
        """Displays the songs in the priority queue."""
        if self.is_empty():
            print("\nParty mode queue is empty.")
            return
        
        print("\n--- Party Mode Queue (Highest Upvotes First) ---")
        temp_list = sorted(self.queue, key=lambda x: x[0])
        for i, (priority, song) in enumerate(temp_list):
            print(f"{i+1}. {song.title} by {song.artist} (Upvotes: {-priority})")
        print("--------------------------------------------------")

try:
    from song import Song
except ImportError:
    class Song:
        def __init__(self, title, artist):
            self.title = title
            self.artist = artist
            self.upvotes = 0

        def __str__(self):
            return f"{self.title} by {self.artist}"

