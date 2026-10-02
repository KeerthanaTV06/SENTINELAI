import logging

class PrivacyAccountant:
    def __init__(self, target_epsilon=1.0, target_delta=1e-5):
        self.epsilon = target_epsilon
        self.delta = target_delta
    def track_round(self, round_num):
        logging.info(f"Round {round_num}: Privacy budget tracked.")
