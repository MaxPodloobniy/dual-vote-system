import pandas as pd
import numpy as np

from encryption_decryption import *
from signing_checking import *

class Commission:
    def __init__(self, voters_ids, candidates_names):
        self.comm_keys = generate_keys()
        self.public_comm_key = self.comm_keys['public_key']
        self.private_comm_key = self.comm_keys['private_key']
        self.voters = voters_ids
        self.candidates_data = pd.DataFrame({
            'Name': candidates_names,
            'Votes_Count': np.zeros(len(candidates_names))
        })
        self.voted_ballots = {}

    def count_vote(self, encrypted_ballot, signature, public_sign_voter_key):
        decrypted_ballot = decrypt_string(
            encrypted_ballot,
            self.private_comm_key,
            self.public_comm_key[0]
        )

        is_valid = verify_signature(decrypted_ballot, signature, public_sign_voter_key)

        if is_valid:
            # ballot_id, reg_id, choice
            ballot_parts = decrypted_ballot.split('|')
            # Перевірка чи не голосував вже виборець
            if ballot_parts[1] not in self.voters and ballot_parts[1] in self.voted_ballots.keys():
                raise ValueError("Виборець за таким id вже проголосував")

            # Перевірка чи такий виборець зареєстрований
            if ballot_parts[1] not in self.voters:
                raise ValueError("Виборця нема в системі")

            # Зараховуємо голос, видаляємо ID зі списку виборців і реєструємо бюлетень
            self.candidates_data.iloc[int(ballot_parts[2])-1, self.candidates_data.columns.get_loc('Votes_Count')] += 1
            self.voted_ballots.update({f'{ballot_parts[1]}': ballot_parts[0]})
            self.voters.remove(ballot_parts[1])
        else:
            raise ValueError("Під час перевірки підпису виникла помилка")


    def get_results(self):
        """Передає результати голосування"""
        num_of_voted = len(self.voted_ballots.keys())
        return self.candidates_data, num_of_voted, self.voted_ballots
