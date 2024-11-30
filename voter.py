from encryption_decryption import *
from signing_checking import *
from datetime import datetime

class Voter:
    def __init__(self, voter_id):
        self.comm_keys = generate_keys()
        self.public_comm_key = self.comm_keys['public_key']
        self.private_comm_key = self.comm_keys['private_key']
        self.sign_keys = generate_dsa_keys()
        self.public_sign_key = self.sign_keys['public_key']
        self.private_sign_key = self.sign_keys['private_key']
        self.registration_id = voter_id

    def generate_ballot(self, public_commission_key, choice):
        timestamp = datetime.now().isoformat().encode('utf-8')
        ballot_id = hashlib.sha1(timestamp).hexdigest()

        ballot = f'{ballot_id}|{self.registration_id}|{choice}'
        encrypted_ballot = encrypt_string(ballot, public_commission_key)

        ballot_signature = sign_message(ballot, self.private_sign_key, self.public_sign_key)
        # !!!!! Чи треба енкріптить підпис чи нє?

        return encrypted_ballot, ballot_signature, self.public_sign_key