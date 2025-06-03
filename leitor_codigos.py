import tkinter as tk
from datetime import datetime
import os
import csv

# Pasta onde os arquivos CSV serão armazenados
PASTA = "conferencia_estoque"
os.makedirs(PASTA, exist_ok=True)

# Nome do arquivo CSV com base na data atual
data_hoje = datetime.now().strftime("%Y-%m-%d")
nome_arquivo = f"codigos_{data_hoje}.csv"
caminho_arquivo = os.path.join(PASTA, nome_arquivo)

# Cria o arquivo com cabeçalho se ainda não existir
if not os.path.exists(caminho_arquivo):
    with open(caminho_arquivo, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Codigo", "DataHora"])

# Lê códigos já salvos (para evitar duplicatas)
codigos_existentes = set()
with open(caminho_arquivo, mode="r", encoding="utf-8") as f:
    leitor = list(csv.reader(f, delimiter=";"))

    for linha in leitor[1:]:
        if linha:
            codigos_existentes.add(linha[0].strip())

# Interface gráfica
janela = tk.Tk()
janela.attributes("-fullscreen", True)
janela.title("Leitor de Código de Barras")
janela.geometry("400x500")

lista_codigos = tk.Listbox(janela, font=("Arial", 19), width=50, height=20)
lista_codigos.pack(pady=10)

entrada = tk.Entry(janela, font=("Arial", 21))
entrada.pack()
entrada.focus()


def registrar_codigo(event):
    codigo = entrada.get().strip()

    if codigo and codigo not in codigos_existentes:
        datahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        codigos_existentes.add(codigo)

        lista_codigos.insert(-1, f"{codigo} - {datahora}")
        lista_codigos.see(0)

        with open(caminho_arquivo, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow([codigo, datahora])

    entrada.delete(0, tk.END)


entrada.bind("<Return>", registrar_codigo)

# Botão de fechar
botao_fechar = tk.Button(janela, text="Fechar", font=("Arial", 16), command=janela.destroy)
botao_fechar.pack(pady=10)

janela.mainloop()
