import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QVBoxLayout, QComboBox

class Livro:
    def __init__(self, tipo, caminho, autor, serie, titulo):
        self.tipo = tipo
        self.caminho = caminho
        self.autor = autor
        self.serie = serie
        self.titulo = titulo

def obter_caminho():
    caminho, _ = QFileDialog.getOpenFileName(None, "Selecione o arquivo ou pasta")
    return caminho

class RenomeadorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.lista_de_informacoes = []

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Campos de entrada
        self.label_caminho = QLabel("Caminho:")
        self.entry_caminho = QLineEdit()
        self.entry_caminho.setPlaceholderText("Insira o caminho ou clique em 'Procurar'")
        self.entry_caminho.setDisabled(True)  # Desabilita a edição manual

        self.label_autor = QLabel("Autor:")
        self.entry_autor = QLineEdit()

        self.label_serie = QLabel("Série:")
        self.entry_serie = QLineEdit()

        self.label_titulo = QLabel("Título:")
        self.entry_titulo = QLineEdit()

        self.label_tipo = QLabel("Tipo:")
        self.dropdown_tipo = QComboBox()
        self.dropdown_tipo.addItems(["Arquivo", "Pasta"])

        # Botões
        self.btn_adicionar = QPushButton("Adicionar Livro")
        self.btn_adicionar.clicked.connect(self.adicionar_livro)

        self.btn_procurar = QPushButton("Procurar")
        self.btn_procurar.clicked.connect(self.procurar_caminho)

        self.btn_renomear = QPushButton("Renomear Arquivos")
        self.btn_renomear.clicked.connect(self.renomear_arquivos)

        # Adiciona widgets ao layout
        layout.addWidget(self.label_caminho)
        layout.addWidget(self.entry_caminho)
        layout.addWidget(self.btn_procurar)
        layout.addWidget(self.label_autor)
        layout.addWidget(self.entry_autor)
        layout.addWidget(self.label_serie)
        layout.addWidget(self.entry_serie)
        layout.addWidget(self.label_titulo)
        layout.addWidget(self.entry_titulo)
        layout.addWidget(self.label_tipo)
        layout.addWidget(self.dropdown_tipo)
        layout.addWidget(self.btn_adicionar)
        layout.addWidget(self.btn_renomear)

        self.setLayout(layout)
        self.setWindowTitle('Renomeador de Arquivos')

    def adicionar_livro(self):
        tipo = self.dropdown_tipo.currentText()
        caminho = self.entry_caminho.text()
        autor = self.entry_autor.text()
        serie = self.entry_serie.text()
        titulo = self.entry_titulo.text()

        if caminho and autor and serie and titulo:
            livro = Livro(tipo, caminho, autor, serie, titulo)
            self.lista_de_informacoes.append(livro)
            self.limpar_campos()
        else:
            print("Por favor, preencha todos os campos.")

    def procurar_caminho(self):
        caminho = obter_caminho()
        if caminho:
            self.entry_caminho.setText(caminho)

    def limpar_campos(self):
        self.entry_caminho.clear()
        self.entry_autor.clear()
        self.entry_serie.clear()
        self.entry_titulo.clear()

    def renomear_arquivos(self):
        for livro in self.lista_de_informacoes:
            tipo = livro.tipo
            caminho = livro.caminho
            autor = livro.autor.title()
            serie = livro.serie.title()
            titulo = livro.titulo.title()

            novo_nome = f"{autor} - ({serie}) - {titulo}"

            if tipo.lower() == "pasta":
                os.rename(caminho, os.path.join(os.path.dirname(caminho), novo_nome))
            elif tipo.lower() == "arquivo":
                extensao = os.path.splitext(caminho)[1]
                os.rename(caminho, os.path.join(os.path.dirname(caminho), novo_nome + extensao))
            else:
                print("Tipo inválido. Por favor, escolha 'pasta' ou 'arquivo'.")

if __name__ == '__main__':
    app = QApplication([])
    renomeador_app = RenomeadorApp()
    renomeador_app.show()
    app.exec_()
