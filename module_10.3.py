# "Блокировки и обработка ошибок"
# "Банковские операции"

# Импорты необходимых модулей и функций
import threading
from time import sleep
from random import randint


class Bank:

    def __init__(self):
        self.lock = threading.Lock()
        self.balance = 0           # баланс банка (int)

    def deposit(self):

        for _ in range(100):
            dep = randint(50, 500)
            self.balance += dep 
            print(f"Пополнение: {dep}. Баланс: {self.balance}")
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()     # разблокировать
            sleep(0.001)

    def take(self):
        for _ in range(100):        
            take_ = randint(50, 500)
            print(f"Запрос на: {take_}.")
            if take_ <= self.balance:
                self.balance -= take_
                print(f"Снятие: {take_}. Баланс: {self.balance}")      
            else:
                print(f"Запрос отклонён, недостаточно средств") 
                self.lock.acquire()      # заблокировать


bk = Bank()

# Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
