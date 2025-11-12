from emoji_recommender import EmojiRecommender

if __name__ == "__main__":
    recommender = EmojiRecommender()

    messages = [
        "I am so happy today!",
        "Feeling sad about the result",
        "I love my dog",
        "Work makes me angry sometimes",
        "Time to sleep"
    ]

    for msg in messages:
        emoji = recommender.recommend(msg)
        print(f"Message: {msg} → {emoji}")