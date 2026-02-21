# reader.py
import time
import random

def reader(account, reader_id, running_flag):

    while running_flag["running"]:
        account.consult_balance(reader_id)
        time.sleep(random.uniform(0.5, 1.5))