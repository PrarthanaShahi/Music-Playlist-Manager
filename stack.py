# This file contains the implementation of a stack for the playlist history.

class PlaybackHistory:
    """A stack to keep track of recently played songs."""
    def __init__(self):
        self.history = []

    def push(self,song):
        """Adds a song to the history stack."""
        self.history.append(song)

    def pop(self):
        """Removes and returns the last played song from history."""
        if not self.is_empty():
            return self.history.pop()
        return None
    
    def is_empty(self):
        """Checks if the history stack is empty."""
        return len(self.history) == 0

    def view_history(self):
        """Displays the playback history from most recent to oldest."""
        if self.is_empty():
            print("History is empty.")
            return
        
        print("\n--- Playback History (Most Recent First) ---")
        for i, song in enumerate(reversed(self.history)):
            print(f"{i+1}. {song}")
        print("------------------------------------------")   