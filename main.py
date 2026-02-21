# main.py
import threading
import time
from bank_account import BankAccount
from reader import reader
from writer import writer

NUM_READERS = 4
NUM_WRITERS = 2
SIMULATION_TIME = 180

def main():

    print("=== SIMULACIÓN SISTEMA BANCARIO ===")
    print(f"Clientes consultando: {NUM_READERS}")
    print(f"Transacciones activas: {NUM_WRITERS}")
    print("=" * 50)

    account = BankAccount(initial_balance=10000)

    running_flag = {"running": True}

    threads = []

    # Crear lectores (clientes consultando)
    for i in range(NUM_READERS):
        t = threading.Thread(target=reader, args=(account, i+1, running_flag))
        threads.append(t)

    # Crear escritores (transacciones)
    for i in range(NUM_WRITERS):
        t = threading.Thread(target=writer, args=(account, i+1, running_flag))
        threads.append(t)

    for t in threads:
        t.start()

    time.sleep(SIMULATION_TIME)

    print("\n--- FINALIZANDO SIMULACIÓN ---\n")
    running_flag["running"] = False

    for t in threads:
        t.join()

    print("Simulación finalizada.")
    print(f"Saldo final: Q{account.balance}")

if __name__ == "__main__":
    main()