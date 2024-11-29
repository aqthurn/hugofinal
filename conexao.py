import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from pandas.plotting import table

class Conexao:
    def __init__(self):
        self.connection = self.conectar()
        self.cursor = self.connection.cursor()
        self.criar_tabela()

    def conectar(self):
        try:
            connection = sqlite3.connect("deleonhotel.db")
            return connection
        except sqlite3.Error as e:
            print(f'Erro ao conectar ao banco de dados: {e}')
            return None

    def criar_tabela(self):
        try:
            # Criando ou alterando a tabela para incluir a coluna 'creche'
            sql = '''
                CREATE TABLE IF NOT EXISTS pethotel (
                    id_cliente INTEGER PRIMARY KEY,
                    Cliente VARCHAR(255),
                    Banho INT,
                    Tosa INT,
                    Transporte INT,
                    Data VARCHAR(12),
                    creche TEXT,
                    Hotel TEXT  -- Nova coluna 'creche' adicionada
                )
            '''
            self.cursor.execute(sql)
            self.connection.commit()
            print('Tabela criada com sucesso')
        except sqlite3.Error as e:
            print(f'Erro ao criar a tabela: {e}')

    def insert_transacao(self, cliente, banho, tosa, transporte, data, creche, hotel):
        try:
            sql = '''
                INSERT INTO pethotel (Cliente, Banho, Tosa, Transporte, Data, creche, Hotel)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            self.cursor.execute(sql, (cliente, banho, tosa, transporte, data, creche, hotel))
            self.connection.commit()
            print('Transação inserida com sucesso')
        except sqlite3.Error as e:
            print(f'Erro ao inserir transação: {e}')

    def update_transacao(self, cliente, banho, tosa, transporte, data, creche, id_cliente, hotel):
        try:
            sql = '''
                UPDATE pethotel
                SET Cliente = ?, Banho = ?, Tosa = ?, Transporte = ?, Data = ?, creche = ?, Hotel = ?
                WHERE id_cliente = ?
            '''
            self.cursor.execute(sql, (cliente, banho, tosa, transporte, data, creche, id_cliente, hotel))
            self.connection.commit()
            print('Transação atualizada com sucesso')
        except sqlite3.Error as e:
            print(f'Erro ao atualizar transação: {e}')
  
    def delete_transacao(self, id_cliente):
        try:
            sql = '''
                DELETE FROM pethotel
                WHERE id_cliente = ?
            '''
            self.cursor.execute(sql, (id_cliente,))
            self.connection.commit()
            print('Transação deletada com sucesso')
        except sqlite3.Error as e:
            print(f'Erro ao deletar transação: {e}')

    def delete_all(self):
        try:
            self.cursor.execute("DELETE FROM pethotel")  # Ajuste o nome da tabela, se necessário
            self.connection.commit()
            print('Todas as transações deletadas com sucesso')
        except sqlite3.Error as e:
            print(f'Erro ao deletar todas as transações: {e}')

    def read_all(self):
        try:
            sql = '''SELECT * FROM pethotel'''
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f'Erro ao ler todas as transações: {e}')
            return []

    def read_one(self, id_cliente):
        try:
            sql = '''SELECT * FROM pethotel WHERE id_cliente = ?'''
            self.cursor.execute(sql, (id_cliente,))
            row = self.cursor.fetchone()
            return row
        except sqlite3.Error as e:
            print(f'Erro ao ler transação: {e}')
            return None

    def read_data_por_ano(self, ano):
        try:
            query = "SELECT * FROM pethotel WHERE strftime('%Y', data) = ?"
            self.cursor.execute(query, (str(ano),))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f'Erro ao ler transações por ano: {e}')
            return []

    def read_data_por_mes(self, ano, mes):
        try:
            query = "SELECT * FROM pethotel WHERE strftime('%Y', data) = ? AND strftime('%m', data) = ?"
            self.cursor.execute(query, (str(ano), str(mes).zfill(2)))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f'Erro ao ler transações por mês: {e}')
            return []

    def read_data_por_dia(self, data_pesquisa):
        try:
            query = "SELECT * FROM pethotel WHERE data = ?"
            self.cursor.execute(query, (data_pesquisa,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f'Erro ao ler transações por dia: {e}')
            return []

    def close(self):
        if self.connection:
            self.connection.close()
            print('Conexão fechada com sucesso')
        else:
            print('Nenhuma conexão ativa para fechar')
    def salvar_datas_creche(self, id_cliente, datas_creche):
        """
        Salva as datas de creche no banco de dados para um cliente específico.
        :param id_cliente: ID do cliente.
        :param datas_creche: Lista de datas selecionadas para a creche.
        """
        try:
            # Converte a lista de datas em uma string separada por vírgulas
            datas_str = ",".join(datas_creche)
            
            # Atualiza a tabela 'pethotel' com as novas datas de creche
            sql = '''
                UPDATE pethotel
                SET creche = ?
                WHERE id_cliente = ?
            '''
            self.cursor.execute(sql, (datas_str, id_cliente))
            self.connection.commit()
            print(f'Datas de creche para o cliente {id_cliente} salvas com sucesso: {datas_str}')
        except sqlite3.Error as e:
            print(f'Erro ao salvar datas de creche: {e}')
if __name__ == '__main__':
    conexao = Conexao()

    # Inserir uma transação com o valor de 'creche'
    conexao.insert_transacao("Cliente Exemplo", 1, 1, 0, "2024-11-13", 1, 1)

    # Atualizar a transação, incluindo o valor de 'creche'
    conexao.update_transacao("Cliente Atualizado", 0, 1, 1, "2024-11-14", 0, 1, 1)  # id_cliente = 1

    # Ler todas as transações
    transacoes = conexao.read_all()
    print(transacoes)

    # Fechar a conexão
    conexao.close()
