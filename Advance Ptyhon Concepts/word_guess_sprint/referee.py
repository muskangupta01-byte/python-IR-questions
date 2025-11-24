class Referee:
    def score(self, secret, guess):
        """
        Returns (match_pos, present_wrong_pos).
        - match_pos: letters correct and in the correct position.
        - present_wrong_pos: letters present in secret but in different positions,
          counted using leftover frequencies after removing exact matches.
        """
        match_pos = 0
        secret_left = {}
        guess_left = {}

        # First pass: count exact matches and collect leftovers
        for s, g in zip(secret, guess):
            if s == g:
                match_pos += 1
            else:
                secret_left[s] = secret_left.get(s, 0) + 1
                guess_left[g] = guess_left.get(g, 0) + 1

        # Second pass: present letters are min of leftover counts per letter
        present = 0
        for ch, cnt in guess_left.items():
            present += min(cnt, secret_left.get(ch, 0))

        return match_pos, present
