import threading
import time
import random
from collections import deque

# Fila que representa a rua (FIFO)
rua = deque()
rua_lock = threading.Lock()

# Lock para imprimir mensagens sem misturar saídas de diferentes threads
print_lock = threading.Lock()

# Evento global para sinalizar que ocorreu um acidente ou que a simulação deve terminar
acidente_event = threading.Event()

# Variáveis globais para detecção de liberações simultâneas
ultimo_liberado_lock = threading.Lock()
ultimo_liberado = 0.0
ultimo_semaforo = None
limite_insercao = 0.05  # 50 milissegundos

# Dicionário para contar quantos carros foram liberados por cada semáforo
carros_liberados = {1: 0, 2: 0, 3: 0, 4: 0}

# Conjunto para armazenar os semáforos que causaram o acidente
acidente_semaforos = set()

def semaforo(id_semaforo):
    global ultimo_liberado, ultimo_semaforo
    while not acidente_event.is_set():
        for cor in ['verde', 'vermelho']:
            if acidente_event.is_set():
                break

            with print_lock:
                print(f"Semáforo {id_semaforo}: {cor}")

            if cor == 'verde':
                # Com 20% de chance, o semáforo libera um carro
                if random.random() < 0.2:
                    current_time = time.time()
                    with ultimo_liberado_lock:
                        # Verifica se houve outra liberação muito próxima de um semáforo diferente
                        if (ultimo_semaforo is not None and 
                            (current_time - ultimo_liberado) < limite_insercao and 
                            ultimo_semaforo != id_semaforo):
                            acidente_semaforos.add(ultimo_semaforo)
                            acidente_semaforos.add(id_semaforo)
                            with print_lock:
                                print("ALERTA DE ACIDENTE! Liberação simultânea de carro pelos semáforos", acidente_semaforos)
                            acidente_event.set()
                        ultimo_liberado = current_time
                        ultimo_semaforo = id_semaforo

                    # Atualiza a contagem de carros liberados por esse semáforo
                    carros_liberados[id_semaforo] += 1

                    # Insere o carro na fila (identificado apenas pelo semáforo)
                    carro = f"carro_{id_semaforo}"
                    with rua_lock:
                        rua.append(carro)
                        with print_lock:
                            print(f"Semáforo {id_semaforo}: Carro inserido na rua. Estado da rua: {list(rua)}")

                    # Simula o tempo que o carro permanece na rua, verificando periodicamente se houve acidente.
                    tempo_permanencia = 3  # segundos
                    intervalo_check = 0.1   # intervalo de verificação (segundos)
                    elapsed = 0
                    while elapsed < tempo_permanencia:
                        if acidente_event.is_set():
                            # Se ocorreu acidente, interrompe sem remover o carro
                            return
                        time.sleep(intervalo_check)
                        elapsed += intervalo_check

                    # Se o acidente não ocorreu durante o tempo de espera, remove o carro da fila.
                    with rua_lock:
                        if rua:
                            removido = rua.popleft()
                            with print_lock:
                                print(f"Semáforo {id_semaforo}: Carro removido da rua: {removido}. Estado da rua: {list(rua)}")
            # Aguarda 1 segundo antes de mudar a cor
            time.sleep(1)

# Cria e inicia 4 threads (um para cada semáforo)
threads = []
for i in range(1, 5):
    t = threading.Thread(target=semaforo, args=(i,))
    t.start()
    threads.append(t)

# Define um tempo máximo para a simulação (por exemplo, 30 segundos)
TEMPO_SIMULACAO = 30
start_time = time.time()

while not acidente_event.is_set():
    if time.time() - start_time > TEMPO_SIMULACAO:
        with print_lock:
            print("Tempo máximo de simulação atingido sem acidentes.")
        acidente_event.set()
    time.sleep(0.5)

# Aguarda todas as threads terminarem
for t in threads:
    t.join()

with print_lock:
    print("\nSimulação encerrada!")
    print("Número de carros liberados por semáforo:")
    for sem, count in carros_liberados.items():
        print(f"Semáforo {sem}: {count} carros liberados")
    if acidente_semaforos:
        print("Semáforos que causaram o acidente:", list(acidente_semaforos))
    else:
        print("Nenhum acidente ocorreu.")