import tkinter as tk
from tkinter import messagebox
import sqlite3

# Conexão com o banco de dados
conexao = sqlite3.connect("gestao_financeira.db")
cursor = conexao.cursor()

# Criação da tabela de transações, se não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS transacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        valor REAL,
        categoria TEXT,
        tipo TEXT
    )
''')
# Classe para o aplicativo de gestão financeira
class AppGestaoFinanceira:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestão Financeira")
        self.transacoes = []

        # Layout de entrada de dados
        self.label_valor = tk.Label(master, text="Valor:")
        self.label_valor.grid(row=0, column=0)

        self.entry_valor = tk.Entry(master)
        self.entry_valor.grid(row=0, column=1)

        self.label_categoria = tk.Label(master, text="Categoria:")
        self.label_categoria.grid(row=1, column=0)

        self.entry_categoria = tk.Entry(master)
        self.entry_categoria.grid(row=1, column=1)

        self.label_tipo = tk.Label(master, text="Tipo (Receita/Despesa):")
        self.label_tipo.grid(row=2, column=0)

        self.entry_tipo = tk.Entry(master)
        self.entry_tipo.grid(row=2, column=1)

        # Botão para adicionar transação
        self.botao_adicionar = tk.Button(master, text="Adicionar", command=self.adicionar_transacao)
        self.botao_adicionar.grid(row=3, column=1)

        # Botão para exibir resumo
        self.botao_resumo = tk.Button(master, text="Resumo", command=self.exibir_resumo)
        self.botao_resumo.grid(row=4, column=1)

    def adicionar_transacao(self):
        valor = self.entry_valor.get()
        categoria = self.entry_categoria.get()
        tipo = self.entry_tipo.get().lower()

        if not valor or not categoria or tipo not in ['receita', 'despesa']:
            messagebox.showerror("Erro", "Preencha todos os campos corretamente.")
            return

        try:
            valor = float(valor)
        except ValueError:
            messagebox.showerror("Erro", "Valor deve ser numérico.")
            return

        if tipo == 'despesa':
            valor = -valor

        self.transacoes.append({'valor': valor, 'categoria': categoria, 'tipo': tipo})
        messagebox.showinfo("Sucesso", "Transação adicionada com sucesso!")
        self.limpar_campos()

    def exibir_resumo(self):
        saldo = sum(transacao['valor'] for transacao in self.transacoes)
        receitas = sum(transacao['valor'] for transacao in self.transacoes if transacao['tipo'] == 'receita')
        despesas = abs(sum(transacao['valor'] for transacao in self.transacoes if transacao['tipo'] == 'despesa'))
        categorias = list()
        resumo = 'Categorias: '
        for transacao in self.transacoes:
            resumo += f"{transacao.get('categoria')} "
        resumo += f"Saldo Total: R$ {saldo:.2f}\nTotal de Receitas: R$ {receitas:.2f}\nTotal de Despesas: R$ {despesas:.2f}"
        messagebox.showinfo("Resumo Financeiro", resumo)

    def limpar_campos(self):
        self.entry_valor.delete(0, tk.END)
        self.entry_categoria.delete(0, tk.END)
        self.entry_tipo.delete(0, tk.END)

# Inicialização da interface
root = tk.Tk()
app = AppGestaoFinanceira(root)
root.mainloop()