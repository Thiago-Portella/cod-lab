import os
import wx

class Livro:
    def __init__(self, tipo, caminho, autor, serie, titulo):
        self.tipo = tipo
        self.caminho = caminho
        self.autor = autor
        self.serie = serie
        self.titulo = titulo

def obter_caminho():
    app = wx.App(False)
    dialog = wx.FileDialog(None, "Selecione o arquivo ou pasta", wildcard="All Files (*.*)|*.*", style=wx.FD_OPEN)
    if dialog.ShowModal() == wx.ID_OK:
        caminho = dialog.GetPath()
    else:
        caminho = ""
    dialog.Destroy()
    return caminho

class RenomeadorApp(wx.Frame):
    def __init__(self):
        super().__init__(None, title='Renomeador de Arquivos')

        self.lista_de_informacoes = []

        self.initUI()
        self.Show()

    def initUI(self):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Campos de entrada
        self.label_caminho = wx.StaticText(panel, label="Caminho:")
        self.entry_caminho = wx.TextCtrl(panel, style=wx.TE_READONLY)
        self.entry_caminho.SetHint("Insira o caminho ou clique em 'Procurar'")

        self.label_autor = wx.StaticText(panel, label="Autor:")
        self.entry_autor = wx.TextCtrl(panel)

        self.label_serie = wx.StaticText(panel, label="Série:")
        self.entry_serie = wx.TextCtrl(panel)

        self.label_titulo = wx.StaticText(panel, label="Título:")
        self.entry_titulo = wx.TextCtrl(panel)

        self.label_tipo = wx.StaticText(panel, label="Tipo:")
        self.dropdown_tipo = wx.Choice(panel, choices=["Arquivo", "Pasta"])

        # Botões
        self.btn_adicionar = wx.Button(panel, label="Adicionar Livro")
        self.btn_adicionar.Bind(wx.EVT_BUTTON, self.adicionar_livro)

        self.btn_procurar = wx.Button(panel, label="Procurar")
        self.btn_procurar.Bind(wx.EVT_BUTTON, self.procurar_caminho)

        self.btn_renomear = wx.Button(panel, label="Renomear Arquivos")
        self.btn_renomear.Bind(wx.EVT_BUTTON, self.renomear_arquivos)

        # Adiciona widgets ao sizer
        sizer.Add(self.label_caminho, 0, wx.ALL, 5)
        sizer.Add(self.entry_caminho, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.btn_procurar, 0, wx.ALL, 5)
        sizer.Add(self.label_autor, 0, wx.ALL, 5)
        sizer.Add(self.entry_autor, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.label_serie, 0, wx.ALL, 5)
        sizer.Add(self.entry_serie, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.label_titulo, 0, wx.ALL, 5)
        sizer.Add(self.entry_titulo, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.label_tipo, 0, wx.ALL, 5)
        sizer.Add(self.dropdown_tipo, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.btn_adicionar, 0, wx.ALL, 5)
        sizer.Add(self.btn_renomear, 0, wx.ALL, 5)

        panel.SetSizer(sizer)

    def adicionar_livro(self, event):
        tipo = self.dropdown_tipo.GetStringSelection()
        caminho = self.entry_caminho.GetValue()
        autor = self.entry_autor.GetValue()
        serie = self.entry_serie.GetValue()
        titulo = self.entry_titulo.GetValue()

        if caminho and autor and serie and titulo:
            livro = Livro(tipo, caminho, autor, serie, titulo)
            self.lista_de_informacoes.append(livro)
            self.limpar_campos()
        else:
            print("Por favor, preencha todos os campos.")

    def procurar_caminho(self, event):
        caminho = obter_caminho()
        if caminho:
            self.entry_caminho.SetValue(caminho)

    def limpar_campos(self):
        self.entry_caminho.Clear()
        self.entry_autor.Clear()
        self.entry_serie.Clear()
        self.entry_titulo.Clear()

    def renomear_arquivos(self, event):
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
    app = wx.App(False)
    frame = RenomeadorApp()
    app.MainLoop()
