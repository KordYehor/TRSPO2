import random
import threading
import time
import math
#Change for pull request

lock = threading.Lock()


def MonteCarlo_pi(num_samples):
    global inside_circle
    local_inside_circle = 0

    for _ in range(num_samples):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)

        if x ** 2 + y ** 2 <= 1:
            local_inside_circle += 1

    with lock:
        inside_circle += local_inside_circle


#Кількість випадкових точок, кількість потоків та відоме значення числа π
num_samples = 1000000


for num_threads in range(1, 7):
    # Заміряємо час виконання
    start_time = time.time()
    inside_circle = 0
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=MonteCarlo_pi, args=(num_samples // num_threads,))
        threads.append(thread)
        thread.start()

    # Перевіряємо статус потоків та чекаємо, поки вони завершаться
    while any(thread.is_alive() for thread in threads):
        time.sleep(1)

    # Кінець вимірювання
    end_time = time.time()

    approximate_pi = 4 * inside_circle / num_samples

    # Порахуємо абсолютну і відносну похибки
    absolute_error = abs(math.pi - approximate_pi)
    relative_error = absolute_error / math.pi

    print(f"Задіяні ядра: {num_threads}")
    print(f"Приблизне значення π: {approximate_pi}")
    print(f"Абсолютна похибка: {absolute_error}")
    print(f"Відносна похибка: {relative_error * 100}%")
    print(f"Час виконання: {end_time - start_time} секунд")
