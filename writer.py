# writer.py
import time
import random

def writer(account, writer_id, running_flag):

    while running_flag["running"]:
        amount = random.randint(10, 100)
        account.withdraw(writer_id, amount)
        time.sleep(random.uniform(1, 2))