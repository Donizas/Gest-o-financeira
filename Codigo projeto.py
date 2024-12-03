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

# Categorias predefinidas
CATEGORIAS = ["Produtos", "Atendimentos", "Contas", "Investimentos", "Vendas", "Outros"]

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

        # Menu suspenso para categorias
        self.categoria_selecionada = tk.StringVar(value=CATEGORIAS[0])
        self.menu_categoria = tk.OptionMenu(master, self.categoria_selecionada, *CATEGORIAS)
        self.menu_categoria.grid(row=1, column=1)

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

        # Botão para limpar todos os dados
        self.botao_limpar = tk.Button(master, text="Limpar Dados", command=self.limpar_dados_banco)
        self.botao_limpar.grid(row=5, column=1)

    def adicionar_transacao(self):
        valor = self.entry_valor.get()
        categoria = self.categoria_selecionada.get()
        tipo = self.entry_tipo.get().lower()

        if not valor or tipo not in ['receita', 'despesa']:
            messagebox.showerror("Erro", "Preencha todos os campos corretamente.")
            return

        try:
            valor = float(valor)
        except ValueError:
            messagebox.showerror("Erro", "Valor deve ser numérico.")
            return

        if tipo == 'despesa':
            valor = -valor

        # Adiciona ao banco de dados
        cursor.execute("INSERT INTO transacoes (valor, categoria, tipo) VALUES (?, ?, ?)", (valor, categoria, tipo))
        conexao.commit()

        self.transacoes.append({'valor': valor, 'categoria': categoria, 'tipo': tipo})
        messagebox.showinfo("Sucesso", "Transação adicionada com sucesso!")
        self.limpar_campos()

    def exibir_resumo(self):
        cursor.execute("SELECT valor, categoria, tipo FROM transacoes")
        transacoes_db = cursor.fetchall()
        saldo = sum(t[0] for t in transacoes_db)
        receitas = sum(t[0] for t in transacoes_db if t[2] == 'receita')
        despesas = abs(sum(t[0] for t in transacoes_db if t[2] == 'despesa'))

        resumo = f"Saldo Total: R$ {saldo:.2f}\nTotal de Receitas: R$ {receitas:.2f}\nTotal de Despesas: R$ {despesas:.2f}\n"
        resumo += "Categorias:\n"
        categorias_totais = {categoria: 0 for categoria in CATEGORIAS}
        for valor, categoria, _ in transacoes_db:
            categorias_totais[categoria] += valor

        for categoria, total in categorias_totais.items():
            resumo += f"  - {categoria}: R$ {total:.2f}\n"

        messagebox.showinfo("Resumo Financeiro", resumo)

    def limpar_campos(self):
        self.entry_valor.delete(0, tk.END)
        self.categoria_selecionada.set(CATEGORIAS[0])
        self.entry_tipo.delete(0, tk.END)

    def limpar_dados_banco(self):
        # Limpar todos os dados do banco de dados
        cursor.execute("DELETE FROM transacoes")
        conexao.commit()
        messagebox.showinfo("Sucesso", "Todos os dados foram limpos do banco de dados.")
        self.transacoes.clear()

# Inicialização da interface
root = tk.Tk()
app = AppGestaoFinanceira(root)
root.mainloop()

# Fechando conexão com o banco de dados ao encerrar o programa
conexao.close()
