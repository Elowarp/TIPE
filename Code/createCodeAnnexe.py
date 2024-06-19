# Recupère toutes les fichiers .py dans le dossier courant et les copies dans un fichier texte séparé par des underscore

def createCodeAnnexe():
    """
    Create a file containing all the code snippets from the .py files in the current directory
    """
    import os
    import re

    # Get all the .py files in the current directory
    files = [f for f in os.listdir() if f.endswith('.py') and f != 'createCodeAnnexe.py' and f != 'rastrigrinPlot.py']

    # Create the file containing all the code snippets
    with open('codeAnnexe.txt', 'w') as f:
        for file in files:
            with open(file, 'r') as f2:
                code = f2.read()
                f.write(code + '\n       ________________________________________________________\n')

createCodeAnnexe()