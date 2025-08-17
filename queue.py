# This file contains the implementation of a queue for the "play next" feature.

class PlayNextQueue:
    """A queue to hold songs that are next in line to be played."""
    def __init__(self):
        self.queue = []
    
    def enqueue(self, song):
        """Adds a song to the play next queue."""
        self.queue.append(song)

    def dequeue(self):
        """Removes and returns the next song to be played."""
        if not self.is_empty():
            return self.queue.pop(0)
        return None
    
    def is_empty(self):
        """Checks if the queue is empty."""
        return len(self.queue) == 0

    def view_queue(self):
        """Displays the songs in the play next queue."""
        if self.is_empty():
            print("Play next queue is empty.")
            return
        
        print("\n--- Play Next Queue (Up Next) ---")
        for i, song in enumerate(self.queue):
            print(f"{i+1}. {song}")
        print("-----------------------------------")
