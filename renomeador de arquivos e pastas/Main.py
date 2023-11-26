import os
import wx

class Livro:
    def __init__(self, tipo, caminho, autor, serie, titulo):
        self.tipo = tipo
        self.caminho = caminho
        self.autor = autor
        self.serie = serie
        self.titulo = titulo

class EscolhaTipo(wx.Frame):
    def __init__(self):
        super().__init__(None, title='Escolha o Tipo', size=(300, 150))

        self.initUI()

    def initUI(self):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        label_tipo = wx.StaticText(panel, label="Escolha o Tipo:")
        choices = ["Arquivo", "Pasta"]
        self.dropdown_tipo = wx.Choice(panel, choices=choices)
        btn_prosseguir = wx.Button(panel, label="Prosseguir")
        btn_prosseguir.Bind(wx.EVT_BUTTON, self.prosseguir)

        sizer.Add(label_tipo, 0, wx.ALL, 10)
        sizer.Add(self.dropdown_tipo, 0, wx.ALL | wx.EXPAND, 10)
        sizer.Add(btn_prosseguir, 0, wx.ALL, 10)

        panel.SetSizer(sizer)

    def prosseguir(self, event):
        tipo_selecionado = self.dropdown_tipo.GetStringSelection()
        self.Hide()
        TelaPrincipal(tipo_selecionado).Show()

class TelaPrincipal(wx.Frame):
    def __init__(self, tipo):
        super().__init__(None, title='Renomeador de Arquivos', size=(400, 300))

        self.tipo = tipo
        self.caminho = ""
        self.lista_de_informacoes = []

        self.initUI()

    def initUI(self):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.label_caminho = wx.StaticText(panel, label="Caminho:")
        self.entry_caminho = wx.TextCtrl(panel, style=wx.TE_READONLY)
        self.btn_procurar = wx.Button(panel, label="Procurar")
        self.btn_procurar.Bind(wx.EVT_BUTTON, self.procurar_caminho)

        self.label_autor = wx.StaticText(panel, label="Autor:")
        self.entry_autor = wx.TextCtrl(panel)

        self.label_serie = wx.StaticText(panel, label="Série:")
        self.entry_serie = wx.TextCtrl(panel)

        self.label_titulo = wx.StaticText(panel, label="Título:")
        self.entry_titulo = wx.TextCtrl(panel)

        btn_renomear = wx.Button(panel, label="Renomear")
        btn_renomear.Bind(wx.EVT_BUTTON, self.renomear)
        btn_adicionar_outro = wx.Button(panel, label="Renomear e Adicionar Outro")
        btn_adicionar_outro.Bind(wx.EVT_BUTTON, self.renomear_e_adicionar)
        btn_cancelar = wx.Button(panel, label="Cancelar")
        btn_cancelar.Bind(wx.EVT_BUTTON, self.cancelar)
        btn_voltar = wx.Button(panel, label="Voltar")
        btn_voltar.Bind(wx.EVT_BUTTON, self.voltar)

        sizer.Add(self.label_caminho, 0, wx.ALL, 5)
        sizer.Add(self.entry_caminho, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.btn_procurar, 0, wx.ALL, 5)
        sizer.Add(self.label_autor, 0, wx.ALL, 5)
        sizer.Add(self.entry_autor, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.label_serie, 0, wx.ALL, 5)
        sizer.Add(self.entry_serie, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.label_titulo, 0, wx.ALL, 5)
        sizer.Add(self.entry_titulo, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(btn_renomear, 0, wx.ALL, 5)
        sizer.Add(btn_adicionar_outro, 0, wx.ALL, 5)
        sizer.Add(btn_cancelar, 0, wx.ALL, 5)
        sizer.Add(btn_voltar, 0, wx.ALL, 5)

        panel.SetSizer(sizer)

    def procurar_caminho(self, event):
        style = wx.FD_OPEN if self.tipo == "Arquivo" else wx.DD_DIR_MUST_EXIST
        dialog = wx.FileDialog(None, "Selecione o arquivo ou pasta", style=style)
        if dialog.ShowModal() == wx.ID_OK:
            self.caminho = dialog.GetPath()
            self.entry_caminho.SetValue(self.caminho)
        dialog.Destroy()

    def renomear(self, event):
        autor = self.entry_autor.GetValue()
        serie = self.entry_serie.GetValue()
        titulo = self.entry_titulo.GetValue()

        if self.caminho and autor and serie and titulo:
            novo_nome = f"{autor} - ({serie}) - {titulo}"

            if self.tipo.lower() == "pasta":
                os.rename(self.caminho, os.path.join(os.path.dirname(self.caminho), novo_nome))
            elif self.tipo.lower() == "arquivo":
                extensao = os.path.splitext(self.caminho)[1]
                os.rename(self.caminho, os.path.join(os.path.dirname(self.caminho), novo_nome + extensao))
            else:
                print("Tipo inválido. Por favor, escolha 'pasta' ou 'arquivo'.")

            self.Destroy()  # Fecha a janela após renomear
        else:
            print("Por favor, preencha todos os campos.")

    def renomear_e_adicionar(self, event):
        self.renomear(event)
        EscolhaTipo().Show()  # Inicia o fluxo novamente

    def cancelar(self, event):
        self.Destroy()

    def voltar(self, event):
        EscolhaTipo().Show()
        self.Destroy()

if __name__ == '__main__':
    app = wx.App(False)
    EscolhaTipo().Show()
    app.MainLoop()
