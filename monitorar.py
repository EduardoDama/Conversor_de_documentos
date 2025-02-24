import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pdf2docx import Converter
import comtypes.client
from plyer import notification
from datetime import datetime
from pathlib import Path

class MeuManipulador(FileSystemEventHandler):
    def __init__(self, converter, convertido, copia):
        super().__init__()
        self.caminho_converter = converter
        self.caminho_convertido = convertido
        self.caminho_copia = copia

    def on_created(self, event):
        if not event.is_directory:
            print(f"Arquivo criado: {event.src_path}")
            tipo, nome = tipoArq(event.src_path)

            if tipo == ".pdf":
                pdf_to_docx(event.src_path, self.caminho_convertido, nome, self.caminho_copia)
            elif tipo in [".docx", ".doc"]:
                docx_to_pdf(event.src_path, self.caminho_convertido, nome, self.caminho_copia)

def tipoArq(caminho_arq):
    nome, extensao = os.path.splitext(os.path.basename(caminho_arq))

    print(nome, extensao)
    return extensao.lower(), nome

def pdf_to_docx(caminho_arq, caminho_convertido, nome, caminho_copia):
    try:
        cv = Converter(caminho_arq)
        caminhofinal = os.path.join(caminho_convertido, nome + ".docx")
        print(f"Convertendo {caminho_arq} para {caminhofinal}")
        
        cv.convert(caminhofinal, start=0, end=None)
        cv.close()

        mover_arquivo(caminho_arq, caminho_copia, nome + ".pdf")
    except Exception:
        notificar('ERRO', 'Erro ao converter PDF para DOCX. TENTE NOVAMENTE')

def docx_to_pdf(caminho_arq, caminho_convertido, nome, caminho_copia):
    word = None
    try:
        word = comtypes.client.CreateObject("Word.Application")
        doc = word.Documents.Open(caminho_arq)
        caminhofinal = os.path.join(caminho_convertido, nome + ".pdf")
        print(f"Convertendo {caminho_arq} para {caminhofinal}")

        doc.SaveAs(caminhofinal, FileFormat=17)
        doc.Close()
        word.Quit()
        
        time.sleep(1)
        mover_arquivo(caminho_arq, caminho_copia, nome + ".docx")
    except Exception:
        notificar('ERRO', 'Erro ao converter DOCX para PDF. TENTE NOVAMENTE')

def mover_arquivo(caminho_arq, caminho_copia, novo_nome):
    """Move o arquivo para a pasta de cópias, evitando erros."""
    destino_final = os.path.join(caminho_copia, novo_nome)
    try:
        os.rename(caminho_arq, destino_final)
        print(f"Arquivo movido para: {destino_final}")
    except FileExistsError:
        os.remove(caminho_arq)
    except Exception:
        notificar('ERRO', 'Erro em mover arquivo original para a pasta de cópias')

def notificar(titulo, msg):
    notification.notify(
        title=titulo,
        message=msg,
        app_name="Monitorar",
        timeout=5  # Tempo em segundos
    )

def verifdia(caminho):
    dia_de_hoje = datetime.today().timetuple().tm_yday
    arquiv = list(Path(caminho).rglob('*'))
    for i in arquiv:
        datademod = time.ctime(os.stat(i).st_ctime)
        data_obj = datetime.strptime(datademod, "%a %b %d %H:%M:%S %Y")
        dia_de_cria = data_obj.timetuple().tm_yday

        if dia_de_hoje - dia_de_cria >= 7 or dia_de_hoje - dia_de_cria < 0:
            os.remove(i)

def verifpasta():
    caminho_area_trabalho = Path.home() / "OneDrive" / "Área de Trabalho"
    pastas = ('Converter', 'Convertido', 'Copias')

    caminho_das_pastas = []
    for i in pastas:
        caminho_pasta = caminho_area_trabalho / i

        if not os.path.exists(caminho_pasta):
            os.makedirs(caminho_pasta)

        caminho_das_pastas.append(caminho_pasta)

    return caminho_das_pastas

def iniciar_monitoramento(pastas):
    while True:  # Loop infinito para manter o programa rodando sempre
        try:
            monitor = MeuManipulador(converter=pastas[0], convertido=pastas[1], copia=pastas[2])
            observer = Observer()
            observer.schedule(monitor, path=monitor.caminho_converter, recursive=False)
            observer.start()
            observer.join()  # Aguarda eventos indefinidamente
        except Exception as e:
            notificar('ERRO MONITORAR PASTA', 'ocorreu um erro na monitoração da pasta converter. Verifique se ela existe')
            time.sleep(5)  # Aguarda 5 segundos antes de tentar reiniciar

if __name__ == '__main__':
    pastas = verifpasta()
    verifdia(caminho=pastas[1])
    verifdia(caminho=pastas[2])
    iniciar_monitoramento(pastas)
