import pandas as pd
import numpy as np
from datetime import datetime
import hashlib


def generate_ids(length):
    id_list = []

    for i in range(length):
        # Унікальний ID виборця
        timestamp = datetime.now().isoformat().encode('utf-8')
        voter_id = hashlib.sha1(timestamp).hexdigest()
        id_list.append(voter_id)
    return id_list


class RegistrationBureau:
    def __init__(self, voters_names):
        self.voters_df = pd.DataFrame({
            'name': voters_names,
            'voters_id': generate_ids(len(voters_names))
        })

    def get_voter_id(self, name):
        result = self.voters_df[self.voters_df['name'] == name]['voters_id']
        if not result.empty:
            return result.iloc[0]  # Повертає перший збіг
        else:
            return None  # Якщо ім'я не знайдено

    def get_all_voters(self):
        return self.voters_df['voters_id'].tolist()

