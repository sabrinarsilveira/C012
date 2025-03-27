import threading
import time
import random
import queue

# Fila que representa a rua (FIFO) - thread-safe
rua = queue.Queue()

# Evento global para sinalizar que ocorreu um acidente ou que a simulação deve terminar
acidente_event = threading.Event()

# Variáveis globais para detecção de liberações simultâneas
ultimo_liberado = 0.0
ultimo_semaforo = None
limite_insercao = 0.05  # 50 milissegundos

# Dicionário para contar quantos carros foram liberados por cada semáforo
carros_liberados = {1: 0, 2: 0, 3: 0, 4: 0}

# Conjunto para armazenar os semáforos que causaram o acidente
acidente_semaforos = set()

# Condição para sincronizar as verificações de liberação (evitar situações de corrida)
condicao_liberacao = threading.Condition()

def semaforo(id_semaforo):
    global ultimo_liberado, ultimo_semaforo
    while not acidente_event.is_set():
        for cor in ['verde', 'vermelho']:
            if acidente_event.is_set():
                return

            print(f"Semáforo {id_semaforo}: {cor}")

            if cor == 'verde':
                if random.random() < 0.2:
                    current_time = time.time()
                    with condicao_liberacao:
                        if (
                            ultimo_semaforo is not None and 
                            (current_time - ultimo_liberado) < limite_insercao and 
                            ultimo_semaforo != id_semaforo
                        ):
                            acidente_semaforos.update([ultimo_semaforo, id_semaforo])
                            print("ALERTA DE ACIDENTE! Liberação simultânea de carro pelos semáforos", acidente_semaforos)
                            acidente_event.set()
                            return
                        
                        ultimo_liberado = current_time
                        ultimo_semaforo = id_semaforo

                    carros_liberados[id_semaforo] += 1
                    carro = f"carro_{id_semaforo}"
                    rua.put(carro)
                    print(f"Semáforo {id_semaforo}: Carro inserido na rua. Estado da rua: {list(rua.queue)}")

                    tempo_permanencia = 3
                    intervalo_check = 0.1
                    elapsed = 0
                    while elapsed < tempo_permanencia:
                        if acidente_event.is_set():
                            return
                        time.sleep(intervalo_check)
                        elapsed += intervalo_check

                    if not rua.empty():
                        removido = rua.get()
                        print(f"Semáforo {id_semaforo}: Carro removido da rua: {removido}. Estado da rua: {list(rua.queue)}")
            
            time.sleep(1)

# Criação e inicialização das threads
threads = []
for i in range(1, 5):
    t = threading.Thread(target=semaforo, args=(i,))
    t.start()
    threads.append(t)

TEMPO_SIMULACAO = 30
start_time = time.time()

while not acidente_event.is_set():
    if time.time() - start_time > TEMPO_SIMULACAO:
        print("Tempo máximo de simulação atingido sem acidentes.")
        acidente_event.set()
    time.sleep(0.5)

# Aguarda todas as threads finalizarem
for t in threads:
    t.join()

print("\nSimulação encerrada!")
print("Número de carros liberados por semáforo:")
for sem, count in carros_liberados.items():
    print(f"Semáforo {sem}: {count} carros liberados")
if acidente_semaforos:
    print("Semáforos que causaram o acidente:", list(acidente_semaforos))
else:
    print("Nenhum acidente ocorreu.")
