# This is the main file that runs the Music Playlist Manager application.

from song import Song
from doubly_linked_list import DoublyLinkedList
from stack import PlaybackHistory
from queue import PlayNextQueue
from priority_queue import PartyModeQueue

class MusicManager:
    """The main class for music app. It holds all the different data structures (playlist, history, queues)
    and handles all the user interactions through a menu."""

    def __init__(self):
        """Initializes the MusicManager with our starting song library and
        creates an instance of each data structure we'll be using."""
        # Our main list of songs that the user can pick from.
        self.song_library = [
            Song("Stay", "Blackpink"),
            Song("Dynamite", "BTS"),
            Song("World", "Seventeen"),
            Song("Love", "Wave to Earth"),
            Song("Blue", "Yung Kai"),
            Song("Die with a smile", "Bruno Mars"),
            Song("August", "Taylor Swift"),
            Song("Birds of a Feather","Billie Eilish"),
            Song("Pretty","JVKE"),
            Song("Best Part","Daniel Caesar")
        ]
        
        # This is our main playlist, which is a doubly linked list.
        self.playlist = DoublyLinkedList()
        # This stack will keep track of songs we've played to go back to them.
        self.history = PlaybackHistory()
        # This is the queue for songs the user wants to play right after the current one.
        self.play_next_queue = PlayNextQueue()
        # This is the special priority queue for party mode.
        self.party_queue = PartyModeQueue()

    def display_menu(self):
        """Prints the main menu to the user, showing all available options."""
        print("\n--- Music Playlist Manager ---")
        print("1. View Song Library")
        print("2. Add Song to Playlist")
        print("3. View Current Playlist")
        print("4. Play Next Song")
        print("5. Play Previous Song")
        print("6. Shuffle Playlist")
        print("7. Add to Play Next Queue")
        print("8. View Playback History")
        print("9. Remove Song from Playlist")
        print("10. Add to Party Mode Queue")
        print("11. Upvote a Song")
        print("12. View Party Mode Queue")
        print("13. Exit")
        print("------------------------------")

    def run(self):
        """It runs a loop that continuously
        displays the menu and processes the user's choices."""
        print("Welcome to the Music Playlist Manager!")
        self.add_initial_songs()

        while True:
            self.display_menu()
            choice = input("Enter your choice: ")

            # Use an if/elif chain to handle each menu choice.
            if choice == '1':
                self.view_song_library()
            elif choice == '2':
                self.add_song_to_playlist()
            elif choice == '3':
                self.view_playlist()
            elif choice == '4':
                self.play_next_song()
            elif choice == '5':
                self.play_previous_song()
            elif choice == '6':
                self.shuffle_playlist()
            elif choice == '7':
                self.add_to_play_next_queue()
            elif choice == '8':
                self.history.view_history()
            elif choice == '9':
                self.remove_song_from_playlist()
            elif choice == '10':
                self.add_to_party_queue()
            elif choice == '11':
                self.upvote_song()
            elif choice == '12':
                self.party_queue.view_queue()
            elif choice == '13':
                print("Thank you for using the Music Player. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def add_initial_songs(self):
        """A simple helper method to add a few songs to the playlist when the app starts."""
        print("\nAdding a few songs to your playlist to get you started...")
        for song in self.song_library[:3]:
            self.playlist.add_song(song)
        print("Playlist created!")

    def view_song_library(self):
        """Displays all the songs available in our library."""
        print("\n--- Song Library ---")
        for i, song in enumerate(self.song_library):
            print(f"{i+1}. {song}")
        print("--------------------")

    def add_song_to_playlist(self):
        """Allows the user to select and add a song to their main playlist."""
        self.view_song_library()
        try:
            song_index = int(input("Enter the number of the song to add: ")) - 1
            if 0 <= song_index < len(self.song_library):
                song_to_add = self.song_library[song_index]
                
                # Check for duplicates before adding the song
                is_duplicate = False
                current = self.playlist.head
                while current:
                    if current.song.title == song_to_add.title:
                        is_duplicate = True
                        break
                    current = current.next

                if is_duplicate:
                    print(f"'{song_to_add.title}' is already in the playlist. Duplicates are not allowed.")
                else:
                    self.playlist.add_song(song_to_add)
                    print(f"'{song_to_add.title}' has been added to the playlist.")
            else:
                print("Invalid song number.")
        except ValueError:
            print("Please enter a valid number.")

    def view_playlist(self):
        """Displays the current playlist, marking the song that is currently playing
        with an asterisk (*)."""
        if not self.playlist.head:
            print("\nYour playlist is empty. Add some songs!")
            return
        
        print("\n--- Current Playlist ---")
        temp = self.playlist.head
        count = 1
        while temp:
            prefix = "* " if temp == self.playlist.current else "   "
            print(f"{prefix}{count}. {temp.song}")
            temp = temp.next
            count += 1
        print("------------------------")

    def play_next_song(self):
        """Plays the next song by checking our different queues in order of priority:
        1. The Party Mode Queue
        2. The Play Next Queue
        3. The main playlist"""
        song_to_play = None
        # Check the party mode queue first (it has the highest priority).
        if not self.party_queue.is_empty():
            song_to_play = self.party_queue.dequeue()
            print(f"\nPlaying from party mode queue: {song_to_play}")
        # If the party queue is empty, check the regular "play next" queue.
        elif not self.play_next_queue.is_empty():
            song_to_play = self.play_next_queue.dequeue()
            print(f"\nPlaying from regular queue: {song_to_play}")
        # If both queues are empty, play the next song from the main playlist.
        else:
            current_song = self.playlist.current.song if self.playlist.current else None
            
            if current_song:
                self.history.push(current_song)

            song_to_play = self.playlist.get_next()
            if song_to_play:
                print(f"\nPlaying: {song_to_play}")
            else:
                print("\nEnd of playlist. No more songs to play.")
                if self.playlist.current and not self.playlist.current.next:
                     self.history.push(self.playlist.current.song)

    def play_previous_song(self):
        """Plays the previous song in the playlist and adds the current song to history."""
        if not self.playlist.current:
            print("\nNo song is currently playing.")
            return

        previous_song = self.playlist.get_previous()
        if previous_song:
            print(f"\nPlaying previous: {previous_song}")
            self.history.push(self.playlist.current.song)
        else:
            print("\nStart of playlist. No previous song to play.")

    def shuffle_playlist(self):
        """Randomizes the order of the songs in the main playlist."""
        if self.playlist.size < 2:
            print("\nCannot shuffle a playlist with less than two songs.")
            return
        self.playlist.shuffle()
        print("\nPlaylist shuffled!")
        self.view_playlist()

    def remove_song_from_playlist(self):
        """Removes a song from the playlist by its title."""
        song_title = input("Enter the title of the song to remove: ")
        if self.playlist.remove_song(song_title):
            print(f"'{song_title}' has been removed from the playlist.")
        else:
            print(f"'{song_title}' was not found in the playlist.")

    def add_to_play_next_queue(self):
        """Adds a song from the library to the play next queue."""
        self.view_song_library()
        try:
            song_index = int(input("Enter the number of the song to add to the play next queue: ")) - 1
            if 0 <= song_index < len(self.song_library):
                song = self.song_library[song_index]
                self.play_next_queue.enqueue(song)
                print(f"'{song.title}' has been added to the play next queue.")
            else:
                print("Invalid song number.")
        except ValueError:
            print("Please enter a valid number.")

    def add_to_party_queue(self):
        """Adds a song from the library to the party mode priority queue."""
        self.view_song_library()
        try:
            song_index = int(input("Enter the number of the song to add to the party mode queue: ")) - 1
            if 0 <= song_index < len(self.song_library):
                song = self.song_library[song_index]
                self.party_queue.enqueue(song)
                print(f"'{song.title}' has been added to the party mode queue with a default upvote.")
            else:
                print("Invalid song number.")
        except ValueError:
            print("Please enter a valid number.")
            
    def upvote_song(self):
        """Increases the upvote count of a song."""
        song_title = input("Enter the title of the song to upvote: ")
        
        if self.party_queue.upvote_song(song_title):
            print(f"'{song_title}' has been upvoted!")
            return

        for song in self.song_library:
            if song.title.lower() == song_title.lower():
                song.upvotes += 1
                print(f"'{song.title}' has been upvoted! Upvotes: {song.upvotes}")
                return
        
        print(f"'{song_title}' was not found in the party mode queue or song library.")

# This is the standard entry point for a Python script.
# It makes sure the application runs when you execute this file.
if __name__ == "__main__":
    manager = MusicManager()
    manager.run()