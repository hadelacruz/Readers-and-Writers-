# semaphore_custom.py
import time

# ============================================
# SPINLOCK - Implementación on Busy-Waiting
# ============================================
class Spinlock:

    def __init__(self):
        self.locked = False  # Variable compartida
    
    def acquire(self):
        while True:
            # Busy-waiting: revisa continuamente si está libre
            while self.locked:
                time.sleep(0.0001)  # Pequeña pausa para no saturar la CPU
            
            # Intenta adquirir (Test-and-Set simulado)
            if not self.locked:
                self.locked = True
                return
    
    def release(self):
        self.locked = False


# ============================================
# SEMAPHORE - Construido sobre Spinlock
# ============================================
class Semaphore:
    def __init__(self, initial):
        self.value = initial
        self.spinlock = Spinlock()  # Usa nuestro Spinlock personalizado
    
    def wait(self):
        while True:
            self.spinlock.acquire()
            
            if self.value > 0:
                self.value -= 1
                self.spinlock.release()
                return
            
            self.spinlock.release()
            time.sleep(0.001)  # Espera breve antes de reintentar
    
    def signal(self):
        self.spinlock.acquire()
        self.value += 1
        self.spinlock.release()