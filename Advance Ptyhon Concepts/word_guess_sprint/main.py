from dictionary import Dictionary
from referee import Referee

def main():
    words = ["APPLE", "GRAPE", "MANGO", "BERRY"]
    d = Dictionary(words)
    r = Referee()

    secret = d.get_random()
    attempts = 5

    print("Word Guess Sprint")
    print("=================")
    print(f"Guess the {len(secret)}-letter word in {attempts} tries!\n")

    tries = 0
    while tries < attempts:
        guess = input(f"Guess {tries + 1}: ").strip().upper()

        if len(guess) != len(secret) or not guess.isalpha():
            print(f"Please enter a {len(secret)}-letter word.\n")
            continue

        m, p = r.score(secret, guess)
        print(f"Match: {m}, Present: {p}\n")

        if guess == secret:
            print("WIN!")
            return

        tries += 1

    print(f"LOSE! Secret was: {secret}")

if __name__ == "__main__":
    main()
