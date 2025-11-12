from emoji_mapper import EmojiMapper

class EmojiRecommender:
    def __init__(self):
        # Use composition to include the mapper
        self.mapper = EmojiMapper()

    def recommend(self, message):
        """
        Analyzes the message and returns the first matching emoji.
        Returns "No emoji found 😶" if no matching keyword is found.
        """
        words = message.split()
        for word in words:
            emoji = self.mapper.get_emoji(word)
            if emoji:
                return emoji
        return "No emoji found 😶"