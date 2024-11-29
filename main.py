from PyQt5 import uic, QtWidgets, QtCore
import sys
import os
from datetime import datetime
from conexao import Conexao
from PyQt5.QtWidgets import QSizePolicy, QAction, QKeySequenceEdit
from conexao import Conexao
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# Permite que a janela seja redimensionável



class MainWindow(QtWidgets.QMainWindow):
    class RelatorioPDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "Relatório de Transações", 0, 1, "C")
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

        @staticmethod
        def calcular_totais_transacoes():
            conexao = Conexao()
            transacoes = conexao.read_all()
            
            total_entrada = 0.0
            total_saida = 0.0

            for transacao in transacoes:
                try:
                    valor = float(transacao[1])
                except ValueError:
                    continue

                tipo_transacao = transacao[3].strip().lower()
                if tipo_transacao == "entrada":
                    total_entrada += valor
                elif tipo_transacao == "saida":
                    total_saida += valor

            return total_entrada, total_saida

        @staticmethod
        def calcular_totais_mensais():
            conexao = Conexao()
            transacoes = conexao.read_all()
            
            totais_mensais = {}

            for transacao in transacoes:
                try:
                    valor = float(transacao[1])
                    data_transacao = datetime.strptime(transacao[4], "%Y-%m-%d")
                except (ValueError, IndexError):
                    continue

                mes_ano = data_transacao.strftime("%Y-%m")
                tipo_transacao = transacao[3].strip().lower()

                if mes_ano not in totais_mensais:
                    totais_mensais[mes_ano] = {"entrada": 0.0, "saida": 0.0}

                if tipo_transacao == "entrada":
                    totais_mensais[mes_ano]["entrada"] += valor
                elif tipo_transacao == "saida":
                    totais_mensais[mes_ano]["saida"] += valor

            return totais_mensais  # Agora está fora do loop

        @staticmethod
        def gerar_relatorio_pdf(caminho_pdf):
            total_entrada, total_saida = MainWindow.RelatorioPDF.calcular_totais_transacoes()
            totais_mensais = MainWindow.RelatorioPDF.calcular_totais_mensais()
            
            pdf = MainWindow.RelatorioPDF()
            pdf.add_page()
            pdf.set_font("Arial", "", 12)
            
            pdf.cell(0, 10, f"Total de Entradas: R$ {total_entrada:.2f}", 0, 1)
            pdf.cell(0, 10, f"Total de Saídas: R$ {total_saida:.2f}", 0, 1)
            
            pdf.cell(0, 10, "", 0, 1)
            pdf.cell(0, 10, "Totais Mensais de Entradas e Saídas", 0, 1)
            
            pdf.set_font("Arial", "B", 10)
            pdf.cell(40, 10, "Mês", 1)
            pdf.cell(40, 10, "Total Entrada", 1)
            pdf.cell(40, 10, "Total Saída", 1)
            pdf.ln()

            pdf.set_font("Arial", "", 10)
            for mes, totais in totais_mensais.items():
                pdf.cell(40, 10, mes, 1)
                pdf.cell(40, 10, f"R$ {totais['entrada']:.2f}", 1)
                pdf.cell(40, 10, f"R$ {totais['saida']:.2f}", 1)
                pdf.ln()

            pdf.cell(0, 10, "", 0, 1)
            pdf.cell(0, 10, "Detalhes das Transações", 0, 1)
            
            pdf.set_font("Arial", "B", 10)
            pdf.cell(30, 10, "ID", 1)
            pdf.cell(50, 10, "Nome", 1)
            pdf.cell(30, 10, "Tipo", 1)
            pdf.cell(30, 10, "Valor", 1)
            pdf.cell(30, 10, "Data", 1)
            pdf.ln()

            pdf.set_font("Arial", "", 10)
            conexao = Conexao()
            transacoes = conexao.read_all()
            for transacao in transacoes:
                pdf.cell(30, 10, str(transacao[0]), 1)
                pdf.cell(50, 10, transacao[2], 1)
                pdf.cell(30, 10, transacao[3], 1)
                
                try:
                    valor_formatado = f"R$ {float(transacao[1]):.2f}"
                except ValueError:
                    valor_formatado = "Erro"

                pdf.cell(30, 10, valor_formatado, 1)
                pdf.cell(30, 10, transacao[4], 1)
                pdf.ln()

            pdf.output(caminho_pdf)
            print(f"Relatório salvo em {caminho_pdf}")
    def chamar_gerar_relatorio_pdf(MainWindow):
        caminho_pdf = "relatorio_transacoes.pdf"  # Salva no diretório atual
        MainWindow.RelatorioPDF.gerar_relatorio_pdf(caminho_pdf)


def abrir_janela_inserir():
        
    tela_inserir_matriculas.show()








def setup_button_for_search_dialog(tela_cadastro, dialog):
    # Conecta o botão de pesquisa ao diálogo
    tela_cadastro.pushButton_7.clicked.connect(lambda: show_search_dialog(dialog))

def show_search_dialog(dialog):
    # Exibe o diálogo de pesquisa
    dialog.exec_()

def limpa_tabela(valor):
    # Valor é o valor de linhas que terá a tabela
    conexao = Conexao()
    if valor == 1:
        tela_cadastro.tableWidget.setRowCount(1)
        tela_cadastro.tableWidget.setColumnCount(len(conexao.read_all()[0]))
        tela_cadastro.tableWidget.setHorizontalHeaderLabels(["id cliente","Cliente","Banho", "Tosa", "data", "Creche"])
        tela_cadastro.tableWidget.setRowCount(valor)
        tela_cadastro.tableWidget.setColumnCount(len(conexao.read_all()[0]))
        tela_cadastro.tableWidget.setHorizontalHeaderLabels(["id cliente","Cliente","Banho", "Tosa", "data", "Creche"])

def voltar():
    tela_inserir_matriculas.close()
    tela_cadastro.close()

def atualiza_tabela_principal():
    conexao = Conexao()
    # Recupera todas as transações do banco de dados
    rows = conexao.read_all()

    # Limpa a tabela se não houver dados disponíveis
    if not rows:
        tela_cadastro.tableWidget.setRowCount(0)
        tela_cadastro.tableWidget.setColumnCount(0)
        tela_cadastro.tableWidget.setHorizontalHeaderLabels([])  # Limpa os rótulos do cabeçalho
        return

    # Define o número de linhas e colunas
    tela_cadastro.tableWidget.setRowCount(len(rows))
    tela_cadastro.tableWidget.setColumnCount(len(rows[0]))  # O número de colunas da primeira linha

    # Define os nomes das colunas
    tela_cadastro.tableWidget.setHorizontalHeaderLabels(["Id cliente","Cliente","Banho", "Tosa","Transporte", "Data", "Creche", "Hotel"])

    # Preenche a tabela com os dados das transações
    for i, row in enumerate(rows):  # Para cada linha
        for j, value in enumerate(row):  # Para cada coluna
            item = QtWidgets.QTableWidgetItem(str(value))       
            tela_cadastro.tableWidget.setItem(i, j, item)

def fechar_janela_inserir():
    atualiza_tabela_principal()
    tela_inserir_matriculas.lineEdit_4.setText('')
    tela_inserir_matriculas.lineEdit_5.setText('')
    tela_inserir_matriculas.lineEdit_3.setText('')
    tela_inserir_matriculas.lineEdit2.setText('')
    tela_inserir_matriculas.close()

def inserir_dados():
    # Definindo tipos válidos de transação
    numeros = '123456789'
    caracteres_especiais = "!@#$%¨&*()-=+[]"

    try:
        # Resgatando o valor dos campos da janela inserir
        cliente = tela_inserir_matriculas.lineEdit2.text()  # Campo para o nome da transação
        banho = tela_inserir_matriculas.lineEdit_5.text()
        tosa = tela_inserir_matriculas.lineEdit_4.setText('')
        transporte =  tela_inserir_matriculas.lineEdit_3.setText('')
            
        # QComboBox para o tipo
        data_transacao = tela_inserir_matriculas.dateTimeEdit.dateTime().toString("yyyy-MM-dd")  # QDateTimeEdit para data

        # Verificando se os campos obrigatórios estão preenchidos
        if not cliente or not banho:
            QtWidgets.QMessageBox.about(tela_inserir_matriculas, 'Erro', 'Por favor, preencha todos os campos antes de inserir')
            return

        # Convertendo valor para float
        try:
            banho = float(banho)
        except ValueError:
            QtWidgets.QMessageBox.about(tela_inserir_matriculas, 'Erro', 'Insira apenas números no campo Valor')
            return

        # Validando o nome para impedir números e caracteres especiais
        for char in cliente:
            if char in numeros or char in caracteres_especiais:
                QtWidgets.QMessageBox.about(tela_inserir_matriculas, 'Erro', 'Por favor, não insira números ou caracteres especiais no campo "nome da transação"')
                return

        # Inserir no banco de dados com o campo data (simulação)
        conexao = Conexao()
        Connection = conexao.insert_transacao(banho, tosa, transporte, cliente, data_transacao)
        atualiza_tabela_principal()
        QtWidgets.QMessageBox.about(tela_inserir_matriculas, 'Sucesso', 'Transação inserida com sucesso')

    except Exception as e:
        QtWidgets.QMessageBox.about(tela_inserir_matriculas, 'Erro', f'Ocorreu um erro: {e}')
    
    return


def abrir_janela_atualizar():
    tela_atualizar.show()

def fechar_janela_atualizar():
    atualiza_tabela_principal()
    tela_atualizar.lineEdit.setText('')
    tela_atualizar.lineEdit_2.setText('')
    #tela_atualizar.lineEdit_4.setText('')
    tela_atualizar.close()

def atualizar_dados():
    # Caracteres inválidos para nome da transação
    numeros = '1234567890'
    caracteres_especiais = "!@#$%¨&*()-=+[]"
    
    try:
        # Resgatando valores dos campos
        id_transacao = tela_atualizar.lineEdit_id.text().strip()  # Obtém o ID da transação
        nome_transacao = tela_atualizar.lineEdit2.text().strip()
        banho = tela_atualizar.lineEdit_5.text().strip()
        tosa = tela_atualizar.lineEdit_4.text().strip()
        transporte = tela_atualizar.lineEdit_3.text().strip()
          # Captura o tipo de transação selecionado no comboBox
        
        # Verifica se o campo ID da transação não está vazio
        if not id_transacao.isdigit():
            QtWidgets.QMessageBox.about(tela_atualizar, 'Erro', 'ID da transação inválido.')
            return
        id_transacao = int(id_transacao)

        # Validação do campo "Valor"
        try:
            valor = float(valor)
            if valor < 0:
                raise ValueError("O valor deve ser positivo.")
        except ValueError:
            QtWidgets.QMessageBox.about(tela_atualizar, 'Erro', 'Por favor, insira um valor numérico positivo.')
            return

        # Validação do campo "Nome da Transação"
        if any(char in numeros + caracteres_especiais for char in nome_transacao):
            QtWidgets.QMessageBox.about(tela_atualizar, 'Erro', 'O nome da transação não deve conter números ou caracteres especiais.')
            return

        # Atualização no banco de dados
        conexao = Conexao()
        conexao.update_transacao(id_transacao, nome_transacao, valor, banho, tosa, transporte)

        atualiza_tabela_principal()
        QtWidgets.QMessageBox.about(tela_atualizar, 'Conexão banco de dados', 'Atualização feita com sucesso')

    except Exception as e:
        QtWidgets.QMessageBox.about(tela_atualizar, 'Erro', f'Ocorreu um erro: {e}')

    return
def abrir_janela_excluir():
    tela_excluir.show()

def fechar_janela_excluir():
    atualiza_tabela_principal()
    tela_excluir.lineEdit.setText('')
    tela_excluir.close()

def excluir_dados():
    try:
        id_transacao = tela_excluir.lineEdit.text()
        id_transacao = int(id_transacao)
        if id_transacao < 1 or id_transacao > 300:
            QtWidgets.QMessageBox.about(tela_excluir, 'Erro', 'Por favor insira um id de transacão válido')
            return
        conexao = Conexao()
        response = conexao.read_one(id_transacao)
        if response == None:
            QtWidgets.QMessageBox.about(tela_excluir, 'Erro', 'Falha ao excluir, id inexistente na tabela')
            return
           
    except Exception:
        QtWidgets.QMessageBox.about(tela_excluir, 'Erro', 'Insira apenas números')
        return

    # Parte da inserção no banco de dados
    conexao = Conexao()
    resposta = conexao.delete_transacao(id_transacao)
    atualiza_tabela_principal()
    QtWidgets.QMessageBox.about(tela_excluir, 'Conexão banco de dados', 'Registro excluido com sucesso')
    tela_excluir.lineEdit.clear()
    return  

def setup_button_for_date_search(tela_cadastro):
    # Configura o botão para abrir o calendário
    tela_cadastro.buttonSelectDate.clicked.connect(lambda: open_calendar(tela_cadastro))

def open_calendar(tela_cadastro):
    # Cria e configura o calendário
    calendar = QtWidgets.QCalendarWidget()
    calendar.setWindowTitle("Selecionar Data")
    calendar.setGridVisible(True)
    
    # Conecta a seleção da data à função de pesquisa e fecha o calendário
    calendar.clicked.connect(lambda date: select_date_and_search(calendar, date, tela_cadastro))
    
    # Exibe o calendário
    calendar.show()

def select_date_and_search(calendar, date, tela_cadastro):
    # Fecha o calendário após a seleção da data
    calendar.close()
    
    # Formata a data selecionada
    data_pesquisa = date.toString("yyyy-MM-dd")
    print(f"Data de pesquisa: {data_pesquisa}")

    # Chama a função de pesquisa com a data selecionada
    pesquisar_por_data(data_pesquisa, tela_cadastro)

def pesquisar_por_data(data_pesquisa, tela_cadastro):
    try:
        # Tenta converter a data para verificar o formato
        data = datetime.strptime(data_pesquisa, '%Y-%m-%d')
    except ValueError:
        QtWidgets.QMessageBox.about(tela_cadastro, 'Alerta', 'Por favor, selecione uma data válida no formato YYYY-MM-DD')
        return

    conexao = Conexao()
    # Verifica o nível de granularidade da pesquisa
    if data.day == 1 and data.month == 1:  # Apenas ano
        rows = conexao.read_data_por_ano(data.year)
    elif data.day == 1:  # Apenas mês
        rows = conexao.read_data_por_mes(data.year, data.month)
    else:  # Dia específico
        rows = conexao.read_data_por_dia(data_pesquisa)

    # Verifica se há resultados
    if not rows:
        QtWidgets.QMessageBox.about(tela_cadastro, 'Alerta', 'Valor não encontrado na tabela')
        return

    # Limpa a tabela e exibe os resultados
    limpa_tabela(len(rows))
    for i in range(len(rows)):
        for j in range(len(rows[0])):
            item = QtWidgets.QTableWidgetItem(f"{rows[i][j]}")
            tela_cadastro.tableWidget.setItem(i, j, item)

def alternar_tela_cheia():
    if tela_cadastro.isFullScreen():
        tela_cadastro.showNormal()  # Sai do modo tela cheia
    else:
        tela_cadastro.showFullScreen()  # Entra no modo tela cheia

def obter_nome_transacao(lineEdit):
    return lineEdit.text().strip()  # Retorna o texto do QLineEdit, removendo espaços extras

def pesquisar_por_nome_e_exibir(tela_cadastro, valor_pesquisa):
    transacao = valor_pesquisa.lower()  # Converte o texto para minúsculas
    print(f"Buscando por: {transacao}")  # Para depuração
    encontrou_correspondencia = False  # Para verificar se alguma linha foi exibida

    for row in range(tela_cadastro.tableWidget.rowCount()):
        item = tela_cadastro.tableWidget.item(row, 2)  # Supondo que o nome está na coluna 2
        
        if item:  # Verifica se o item não é None
            print(f"Linha {row}: {item.text()}")  # Imprime o texto do item
            if transacao in item.text().lower():  # Verifica se a transação está no texto
                tela_cadastro.tableWidget.showRow(row)  # Exibe a linha que corresponde
                encontrou_correspondencia = True  # Marque que encontramos uma correspondência
            else:
                tela_cadastro.tableWidget.hideRow(row)  # Oculta a linha que não corresponde
        else:
            tela_cadastro.tableWidget.hideRow(row)  # Oculta linhas onde não há item

    if not encontrou_correspondencia:
        print("Nenhuma correspondência encontrada.")  # Mensagem se nada foi encontrado

def mostrar_dialog_creche(inserir_dados):
  

    
    
    dialogcreche = QtWidgets.QDialog()
    uic.loadUi(r"C:\Users\Arthur\OneDrive\Área de Trabalho\cadastro alunos\dialogcreche.ui", dialogcreche)

    # Obtém os widgets do calendário e botões
    calendar = dialogcreche.findChild(QtWidgets.QCalendarWidget, "calendarWidget")
    button_ok = dialogcreche.findChild(QtWidgets.QPushButton, "pushButtondialogok")
    button_cancel = dialogcreche.findChild(QtWidgets.QPushButton, "pushButtondialogcancelar")

    # Lista para armazenar as datas selecionadas
    datas_selecionadas = set()

    # Função para adicionar/remover datas ao clicar no calendário
    def registrar_data():
        data = calendar.selectedDate().toString("yyyy-MM-dd")
        if data in datas_selecionadas:
            datas_selecionadas.remove(data)  # Remove se já estiver na lista
        else:
            datas_selecionadas.add(data)  # Adiciona se não estiver

        print(f"Datas selecionadas até agora: {datas_selecionadas}")

    # Conecta o clique do calendário à função registrar_data
    calendar.selectionChanged.connect(registrar_data)

    # Função para salvar as datas no banco e fechar o diálogo
    def salvar_e_fechar():
        if datas_selecionadas:
            conexao = Conexao()
              # Obtém o ID do cliente
            conexao.salvar_datas_creche(list(datas_selecionadas))  # Salva no banco
        dialogcreche.accept()  # Fecha o diálogo

    if button_ok:
        button_ok.clicked.connect(salvar_e_fechar)

    if button_cancel:
        button_cancel.clicked.connect(dialogcreche.reject)  # Fecha o diálogo sem salvar

    dialogcreche.exec_()



def mostrar_dialog_pesquisa(tela_cadastro):
    dialog_pesquisa = QtWidgets.QDialog()
    dialog_pesquisa.setWindowTitle("Pesquisar Transação")  # Define o título do diálogo
    setup_search_button_with_dialog(tela_cadastro, dialog_pesquisa)
    dialog_pesquisa.exec_()  # Exibe o diálogo como um modal

def setup_search_button_with_dialog(tela_cadastro, dialog_pesquisa):
    layout = QtWidgets.QVBoxLayout()

    lineEdit_pesquisa = QtWidgets.QLineEdit()
    lineEdit_pesquisa.setPlaceholderText("Digite o nome da pesquisa")
    layout.addWidget(lineEdit_pesquisa)

    botao_confirmar_pesquisa = QtWidgets.QPushButton("Pesquisar")
    layout.addWidget(botao_confirmar_pesquisa)

    dialog_pesquisa.setLayout(layout)

    # Conectar o botão de pesquisa para realizar a ação
    botao_confirmar_pesquisa.clicked.connect(lambda: realizar_pesquisa_dialog(lineEdit_pesquisa, dialog_pesquisa, tela_cadastro))

def realizar_pesquisa_dialog(lineEdit, dialog, tela_cadastro):
    valor_pesquisa = obter_nome_transacao(lineEdit)  # Obtém o nome da transação
    print(f"Nome da transação a ser pesquisado: {valor_pesquisa}")  # Para depuração
    lineEdit.clear()
    # Chame a função de pesquisa passando o valor da pesquisa
    pesquisar_por_nome_e_exibir(tela_cadastro, valor_pesquisa)

    dialog.close()  # Fecha o diálogo após a pesquisa


def deletar_todas_transacoes(self):
    # Exibe uma caixa de diálogo de confirmação
    

    # Verifica se o usuário confirmou a exclusão
    
        # Executa a deleção de todas as transações
        conexao = Conexao()
        conexao.delete_all() 
        
      



def att_tabela_cadastro():
    tela_cadastro.tableWidget.clearContents()  # Limpa a tabela

    # Create a connection to the database
    conexao = Conexao()

    # Fetch all data from the database
    data = conexao.read_all()

    # Update the table with the fetched data
    tela_cadastro.tableWidget.setRowCount(len(data))
    tela_cadastro.tableWidget.setColumnCount(len(data[0]) if data else 0)

    for row_index, row_data in enumerate(data):
        for col_index, col_data in enumerate(row_data):
            tela_cadastro.tableWidget.setItem(row_index, col_index, QtWidgets.QTableWidgetItem(str(col_data)))

    # Close the database connection
    conexao.close()

# Connect the push button to the function
    tela_cadastro.pushButton_8.clicked.connect(att_tabela_cadastro)








# The rest of your code


app = QtWidgets.QApplication(sys.argv)
tela_cadastro = uic.loadUi('tela_cadastro.ui')
tela_inserir_matriculas = uic.loadUi('inserir_dados.ui')
tela_atualizar = uic.loadUi('atualizar_dados.ui')
tela_excluir = uic.loadUi('tela_excluir.ui')
setup_button_for_date_search(tela_cadastro)
dialog_pesquisa = QtWidgets.QDialog()
setup_search_button_with_dialog(tela_cadastro, dialog_pesquisa)
import os
import sys

import os
import sys

# Define o caminho base dependendo se o executável está "frozen" (empacotado) ou não
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Exemplo de uso
image_path = resource_path('imagens/inserir.png')
print(image_path)  # Verifique se o caminho está correto





 


# Conectando os botoes da janela principal as funções da janela principal
tela_cadastro.pushButton_2.clicked.connect(abrir_janela_inserir)
tela_cadastro.pushButton_7.clicked.connect(lambda: dialog_pesquisa.exec_())
tela_cadastro.pushButton_3.clicked.connect(abrir_janela_atualizar)
tela_cadastro.pushButton_5.clicked.connect(voltar)
tela_cadastro.pushButton_4.clicked.connect(abrir_janela_excluir)
tela_cadastro.pushButton_8.clicked.connect(att_tabela_cadastro)
tela_cadastro.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
main_window = MainWindow()
tela_cadastro.pushButton_6.clicked.connect(main_window.chamar_gerar_relatorio_pdf)
tela_cadastro.pushButton_9.clicked.connect(deletar_todas_transacoes)

# Conectando os botões da janela de inserir as funções da janela de inserir
tela_inserir_matriculas.pushButton_2.clicked.connect(fechar_janela_inserir)
tela_inserir_matriculas.pushButton.clicked.connect(inserir_dados)
tela_inserir_matriculas.pushButton_10.clicked.connect(mostrar_dialog_creche)
# Conectando os botões da jenala atualizar as funções da janela atualizar
tela_atualizar.pushButton_2.clicked.connect(fechar_janela_atualizar)
tela_atualizar.pushButton.clicked.connect(atualizar_dados)

# Conectando os botões da janela excluir as funções da janela excluir
tela_excluir.pushButton_2.clicked.connect(fechar_janela_excluir)
tela_excluir.pushButton.clicked.connect(excluir_dados)

atualiza_tabela_principal()

tela_cadastro.show()
sys.exit(app.exec_())