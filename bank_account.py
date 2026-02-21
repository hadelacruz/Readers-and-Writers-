# bank_account.py
from semaphore_custom import Semaphore

class BankAccount:
    def __init__(self, initial_balance):
        self.balance = initial_balance
        self.read_count = 0

        # Semáforos solución justa
        self.mutex = Semaphore(1)
        self.roomEmpty = Semaphore(1)
        self.turnstile = Semaphore(1)

    # ---------------------------
    # MÉTODO LECTOR (consultar saldo)
    # ---------------------------
    def consult_balance(self, reader_id):

        # Justicia
        self.turnstile.wait()
        self.turnstile.signal()

        # Control lectores
        self.mutex.wait()
        self.read_count += 1
        if self.read_count == 1:
            self.roomEmpty.wait()
        self.mutex.signal()

        # Sección crítica (lectura)
        print(f"[Cliente {reader_id}] CONSULTA saldo: Q{self.balance}")

        # Salida lectores
        self.mutex.wait()
        self.read_count -= 1
        if self.read_count == 0:
            self.roomEmpty.signal()
        self.mutex.signal()

    # ---------------------------
    # MÉTODO ESCRITOR (transacción)
    # ---------------------------
    def withdraw(self, writer_id, amount):

        self.turnstile.wait()
        self.roomEmpty.wait()

        # Sección crítica (escritura)
        if self.balance >= amount:
            self.balance -= amount
            print(f"        [Transacción {writer_id}] RETIRO Q{amount} → Nuevo saldo: Q{self.balance}")
        else:
            print(f"        [Transacción {writer_id}] RETIRO FALLIDO (fondos insuficientes)")

        self.roomEmpty.signal()
        self.turnstile.signal()