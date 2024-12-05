import os  # Manipulação de diretórios e arquivos
from datetime import datetime  # Para trabalhar com datas e horários
from pytz import timezone  # Para lidar com fusos horários
from tkinter import messagebox  # Exibição de caixas de diálogo
import customtkinter  # Biblioteca para interface gráfica moderna
import pyqrcode  # Biblioteca para criar QR Codes
from PIL import Image, ImageTk  # Para manipular e exibir imagens
import warnings  # Gerenciamento de avisos

# Ignora avisos desnecessários para melhorar a experiência do usuário
warnings.filterwarnings("ignore", category=UserWarning)


def centralizar_janela(janela):
    """
    Centraliza a janela no meio da tela.
    """
    janela.update_idletasks()  # Atualiza os cálculos de layout da janela
    largura_janela = janela.winfo_width()  # Largura da janela
    altura_janela = janela.winfo_height()  # Altura da janela
    # Calcula a posição para centralizar a janela na tela
    posicao_x = (janela.winfo_screenwidth() // 2) - (largura_janela // 2)
    posicao_y = (janela.winfo_screenheight() // 2) - (altura_janela // 2)
    # Define a geometria da janela
    janela.geometry(f"+{posicao_x}+{posicao_y}")


def redimensionar_imagem(image_path, max_width, max_height):
    """
    Redimensiona uma imagem para as dimensões especificadas.
    """
    try:
        with Image.open(image_path) as img:  # Abre a imagem
            img.thumbnail((max_width, max_height))  # Redimensiona proporcionalmente
            return ImageTk.PhotoImage(img)  # Retorna a imagem em formato compatível com Tkinter
    except Exception as e:
        # Exibe erro caso a imagem não possa ser carregada
        messagebox.showerror("Erro", f"Erro ao carregar a imagem: {e}")
        return None


def criar_qrcode(dados, caminho_arquivo):
    """
    Gera um QRCode a partir dos dados fornecidos e salva no caminho especificado.
    """
    try:
        qr_code = pyqrcode.create(dados)  # Cria o QRCode com os dados
        qr_code.png(caminho_arquivo, scale=6)  # Salva o QRCode como imagem
    except Exception as e:
        # Exibe erro caso ocorra um problema ao criar o QRCode
        messagebox.showerror("Erro", f"Erro ao criar QRCode: {e}")


def get_qrcode():
    """
    Captura os dados de entrada do usuário, gera o QRCode e exibe na interface.
    """
    global qr_code_label  # Referência à variável global para atualizar o QRCode exibido

    # Captura e limpa o texto da entrada
    input_text = entry.get().strip()

    # Validação: garante que o campo não esteja vazio
    if not input_text:
        messagebox.showerror("Erro", "Por favor, insira algum dado para gerar o QRCode.")
        return

    # Adiciona a data e hora aos dados do QRCode
    dados = f"{data_atual_lisboa.strftime(FORMATO_DATA_PT)}\n{input_text}"

    # Garante que o diretório para salvar os QRCodes exista
    os.makedirs("qrcodes", exist_ok=True)

    # Gera o nome do arquivo com base no horário atual
    data_hora_atual = datetime.now().strftime("%Y%m%d_%H%M%S")
    qr_code_path = os.path.join("qrcodes", f"qrcode_{data_hora_atual}.png")

    # Cria e salva o QRCode
    criar_qrcode(dados, qr_code_path)

    # Redimensiona a imagem do QRCode para exibição
    qr_code_image = redimensionar_imagem(qr_code_path, 150, 150)
    if qr_code_image:
        # Remove o QRCode anterior, se existir
        if qr_code_label is not None:
            qr_code_label.destroy()

        # Exibe o QRCode na interface
        qr_code_label = customtkinter.CTkLabel(master=qr_code_frame, image=qr_code_image, text="")
        qr_code_label.image = qr_code_image  # Armazena referência para evitar garbage collection
        qr_code_label.pack()

    # Limpa o campo de entrada após a submissão
    entry.delete(0, 'end')


# Configurações globais
FORMATO_DATA_PT = "%d-%m-%Y %H:%M:%S"  # Formato de data e hora usado no QRCode
FUSO_HORARIO_LISBOA = timezone("Europe/Lisbon")  # Fuso horário para Lisboa
data_atual_lisboa = datetime.now(FUSO_HORARIO_LISBOA)  # Data e hora atual em Lisboa

# Configuração da interface principal
root = customtkinter.CTk()  # Criação da janela principal com customtkinter
customtkinter.set_appearance_mode("dark")  # Define o modo escuro
customtkinter.set_default_color_theme("green")  # Define a cor tema como verde
root.title("JSANDEV - QRCode Generator")  # Título da janela
root.geometry("250x250")  # Tamanho da janela
root.resizable(False, False)  # Impede redimensionamento
root.minsize(250, 370)
centralizar_janela(root)  # Centraliza a janela na tela


qr_code_label = None  # Variável para armazenar o QRCode exibido

# Estrutura da interface
frame = customtkinter.CTkFrame(master=root)  # Cria o frame principal
frame.pack(pady=10, padx=10, fill="both", expand=True)  # Configura o layout do frame

label = customtkinter.CTkLabel(master=frame, text="JSANDEV - QRCode Generator")  # Título no frame
label.pack(pady=12, padx=10)

entry = customtkinter.CTkEntry(master=frame, placeholder_text="Insert Data")  # Campo de entrada
entry.pack(pady=12, padx=10)

btn_generator = customtkinter.CTkButton(
    master=frame, text="Get QRCode", command=get_qrcode
)  # Botão para gerar QRCode
btn_generator.pack(pady=12, padx=10)

qr_code_frame = customtkinter.CTkFrame(master=frame, width=150, height=150)  # Área para exibir o QRCode
qr_code_frame.pack(pady=12, padx=12)
qr_code_frame.pack_propagate(False)  # Impede que o frame redimensione dinamicamente

# Inicia o loop principal da aplicação
try:
    root.mainloop()  # Mantém a aplicação em execução até ser fechada
except KeyboardInterrupt:
    print("Aplicativo encerrado.")  # Tratamento de encerramento seguro pelo teclado
