# Simulação de Semáforos com Threads

Este projeto simula o funcionamento de semáforos em uma rua, utilizando múltiplas threads para controlar a liberação de carros e detectar possíveis colisões por liberações simultâneas.

## 📌 Funcionalidades
- Cada semáforo opera em ciclos de verde e vermelho.
- Com 20% de chance, um semáforo libera um carro quando está verde.
- Se dois semáforos liberarem um carro ao mesmo tempo (dentro de 50ms), ocorre um acidente.
- A rua é gerenciada por uma fila `queue.Queue()` para garantir a segurança entre as threads.
- A simulação tem um tempo máximo de 30 segundos.

## 🛠 Tecnologias Utilizadas
- **Python** (versão 3.x)
- **threading** (para controle das threads)
- **queue.Queue()** (para gerenciar os carros de forma segura)
- **time e random** (para controle de tempo e eventos aleatórios)


## 📊 Saída Esperada
O programa exibirá mensagens indicando o estado dos semáforos, os carros sendo inseridos e removidos da rua e, caso ocorra um acidente, a simulação será encerrada com uma notificação.

Exemplo de saída:
```
Semáforo 1: verde
Semáforo 3: verde
Semáforo 2: verde
Semáforo 4: verde
Semáforo 1: Carro inserido na rua. Estado da rua: ['carro_1']
Semáforo 2: Carro inserido na rua. Estado da rua: ['carro_1', 'carro_2']
ALERTA DE ACIDENTE! Liberação simultânea de carro pelos semáforos {1, 2}
Simulação encerrada!
```



