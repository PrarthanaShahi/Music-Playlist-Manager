# This file defines the song class, a simple data object.

class Song:
    """Represents a single song with a title and artist."""
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist
        self.upvotes = 0 #Added upvote counter for party mode

    def __str__(self):
        """String representation of the song."""
        return f"{self.title} by {self.artist} (Upvotes: {self.upvotes})"