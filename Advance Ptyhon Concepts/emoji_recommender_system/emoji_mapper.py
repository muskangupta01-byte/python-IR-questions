class EmojiMapper:
    def __init__(self):
        # Mapping of mood keywords to emojis
        self.emoji_dict = {
            "happy": "😊",
            "sad": "😢",
            "love": "❤️",
            "angry": "😡",
            "excited": "🤩"
        }

    def get_emoji(self, word):
        """
        Returns the emoji for the given word if it exists.
        Case-insensitive lookup. Returns empty string if not found.
        """
        return self.emoji_dict.get(word.lower(), "")