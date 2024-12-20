import threading
import time
import random
from itertools import count
from queue import Queue
import matplotlib.pyplot as plt

id_counter = count(1)

class LinhaDeProducao:
    def __init__(self, capacidade_buffer):
        self.buffer = Queue(capacidade_buffer)
        self.capacidade = capacidade_buffer
        self.sem_espaco = threading.Semaphore(capacidade_buffer)
        self.sem_itens = threading.Semaphore(0)
        self.mutex = threading.Lock()
        self.total_produzido = 0
        self.total_consumido = 0
        self.operacoes_encerradas = threading.Event()
        self.producao_history = []  # Histórico de produção
        self.consumo_history = []  # Histórico de consumo

    def produzir(self, item):
        if not self.operacoes_encerradas.is_set():
            self.sem_espaco.acquire()
            with self.mutex:
                self.buffer.put(item)
                self.total_produzido += 1
                print(f"[PRODUÇÃO] Peça adicionada: {item} | Buffer: {self.buffer.qsize()}/{self.capacidade}")
            self.sem_itens.release()

    def consumir(self):
        if not self.operacoes_encerradas.is_set():
            self.sem_itens.acquire()
            with self.mutex:
                item = self.buffer.get()
                self.total_consumido += 1
                print(f"[CONSUMO] Peça retirada: {item} | Buffer: {self.buffer.qsize()}/{self.capacidade}")
            self.sem_espaco.release()

def produtor(linha, id):
    while not linha.operacoes_encerradas.is_set():
        time.sleep(random.uniform(0.5, 1.0))
        item_id = next(id_counter)  # Gera um ID crescente
        item = f"Peça-{item_id}"
        linha.produzir(item)
        print(f"[Produtor-{id}] Produziu: {item}")

def consumidor(linha, id):
    while not linha.operacoes_encerradas.is_set():
        time.sleep(random.uniform(0.5, 1.5))
        linha.consumir()

def executar_simulacao(capacidade_buffer, num_produtores, num_consumidores, timesteps):
    linha = LinhaDeProducao(capacidade_buffer)

    # Cria threads de produtores
    threads = []
    for i in range(num_produtores):
        thread = threading.Thread(target=produtor, args=(linha, i + 1), daemon=True)
        threads.append(thread)
        thread.start()

    # Cria threads de consumidores
    for i in range(num_consumidores):
        thread = threading.Thread(target=consumidor, args=(linha, i + 1), daemon=True)
        threads.append(thread)
        thread.start()

    # Simula os timesteps
    for t in range(timesteps):
        if linha.operacoes_encerradas.is_set():
            break
        with linha.mutex:
            linha.producao_history.append(linha.total_produzido)
            linha.consumo_history.append(linha.total_consumido)
        print(f"[CICLO] Timestep {t + 1}/{timesteps}")
        time.sleep(1)

    # Encerra a execução
    linha.operacoes_encerradas.set()

    # Aguarda o término das threads
    for thread in threads:
        thread.join(timeout=0.1)

    # Gera relatório e gráfico
    gerar_relatorio(linha)

def gerar_relatorio(linha):
    print("\n--- RELATÓRIO FINAL ---")
    print(f"Total de itens produzidos: {linha.total_produzido}")
    print(f"Total de itens consumidos: {linha.total_consumido}")
    print(f"Status final do buffer: {linha.buffer.qsize()} itens restantes")
    print("-----------------------")

    # Gerar gráfico
    gerar_grafico(linha)

def gerar_grafico(linha):
    timesteps = range(len(linha.producao_history))
    buffer_ocupacao = [prod - cons for prod, cons in zip(linha.producao_history, linha.consumo_history)]

    plt.plot(timesteps, linha.producao_history, label="Produção", color="blue")
    plt.plot(timesteps, linha.consumo_history, label="Consumo", color="red")
    plt.plot(timesteps, buffer_ocupacao, label="Ocupação do Buffer", color="green")

    plt.axhline(linha.capacidade, color="orange", linestyle="--", label="Capacidade Máxima do Buffer")
    plt.xlabel("Timestep")
    plt.ylabel("Quantidade de Itens")
    plt.title("Produção, Consumo e Ocupação do Buffer")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    # Parâmetros de entrada
    capacidade_buffer = 10
    num_produtores = 3
    num_consumidores = 4
    timesteps = 15  # Quantidade de timesteps

    executar_simulacao(capacidade_buffer, num_produtores, num_consumidores, timesteps)
