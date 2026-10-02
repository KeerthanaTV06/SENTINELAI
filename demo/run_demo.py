import time
import logging

def run_demo():
    logging.info("1. Normal traffic baseline...")
    time.sleep(1)
    logging.info("2. Injecting DoS attack wave...")
    time.sleep(1)
    logging.info("3. Detecting anomalies...")
    time.sleep(1)
    logging.info("4. Triggering SHAP explanations & Auto-blocking IP...")
    logging.info("Demo complete.")

if __name__ == '__main__':
    run_demo()
