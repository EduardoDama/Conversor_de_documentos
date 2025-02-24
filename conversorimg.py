import tkinter as tk
from tkinter import messagebox

# Função que será chamada quando o botão for pressionado
def on_button_click():
    nome = entry_nome.get()
    mensagem = f"Olá, {nome}! Bem-vindo ao Tkinter."
    text_area.insert(tk.END, mensagem + "\n")
    messagebox.showinfo("Mensagem", mensagem)

# Cria a janela principal
root = tk.Tk()
root.title("Exemplo Básico de Layout")

# Define o tamanho da janela
root.geometry("400x300")

# Cria um Label (rótulo)
label_nome = tk.Label(root, text="Digite seu nome:")
label_nome.pack(pady=10)

# Cria um Entry (campo de entrada)
entry_nome = tk.Entry(root, width=30)
entry_nome.pack(pady=10)

# Cria um Button (botão)
button_ok = tk.Button(root, text="OK", command=on_button_click)
button_ok.pack(pady=10)

# Cria um Text (área de texto)
text_area = tk.Text(root, height=10, width=40)
text_area.pack(pady=10)

# Inicia o loop principal da aplicação
root.mainloop()