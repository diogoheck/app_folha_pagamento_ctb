import os
import glob


def remover_arquivo(arquivo):
    if os.path.exists(arquivo):
        os.remove(arquivo)


def remover_todos(caminho):
    py_files = glob.glob(caminho)

    for py_file in py_files:
        try:
            os.remove(py_file)
        except OSError as e:
            print(f"Error:{ e.strerror}")
