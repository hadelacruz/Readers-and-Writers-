import threading
import time
import random

# =========================
# CONFIGURACIÓN
# =========================
NUM_READERS = 3
NUM_WRITERS = 2
SIMULATION_TIME = 60  # segundos

# =========================
# VARIABLES COMPARTIDAS
# =========================
read_count = 0
shared_data = 0

# =========================
# SINCRONIZACIÓN (Solución Justa)
# =========================
mutex = threading.Lock()                 # Protege read_count
roomEmpty = threading.Semaphore(1)       # Exclusión escritores
turnstile = threading.Semaphore(1)       # Justicia (cola global)

# Bandera para detener simulación
running = True


# =========================
# FUNCIÓN LECTOR
# =========================
def reader(reader_id):
    global read_count, shared_data, running

    while running:
        # ---- Entry Section ----
        turnstile.acquire()
        turnstile.release()

        mutex.acquire()
        read_count += 1
        if read_count == 1:
            roomEmpty.acquire()
        mutex.release()

        # ---- Critical Section ----
        print(f"[Reader {reader_id}] ENTRA - leyendo valor {shared_data}")
        time.sleep(random.uniform(0.5, 1.5))
        print(f"[Reader {reader_id}] SALE")

        # ---- Exit Section ----
        mutex.acquire()
        read_count -= 1
        if read_count == 0:
            roomEmpty.release()
        mutex.release()

        time.sleep(random.uniform(0.5, 1.5))


# =========================
# FUNCIÓN ESCRITOR
# =========================
def writer(writer_id):
    global shared_data, running

    while running:
        # ---- Entry Section ----
        turnstile.acquire()
        roomEmpty.acquire()

        # ---- Critical Section ----
        shared_data += 1
        print(f"        [Writer {writer_id}] ENTRA - escribiendo valor {shared_data}")
        time.sleep(random.uniform(0.5, 1.5))
        print(f"        [Writer {writer_id}] SALE")

        # ---- Exit Section ----
        roomEmpty.release()
        turnstile.release()

        time.sleep(random.uniform(1, 2))


# =========================
# MAIN
# =========================
def main():
    global running

    threads = []

    # Crear lectores
    for i in range(NUM_READERS):
        t = threading.Thread(target=reader, args=(i+1,))
        threads.append(t)

    # Crear escritores
    for i in range(NUM_WRITERS):
        t = threading.Thread(target=writer, args=(i+1,))
        threads.append(t)

    # Iniciar hilos
    for t in threads:
        t.start()

    # Simulación por 60 segundos
    time.sleep(SIMULATION_TIME)
    running = False

    # Esperar que todos terminen
    for t in threads:
        t.join()

    print("\nSimulación finalizada.")


if __name__ == "__main__":
    main()