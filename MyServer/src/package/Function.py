
def write_file(nom_fichier, contenu, mode="a"):
    from datetime import datetime
    """
    Écrit du contenu dans un fichier.
    
    :param nom_fichier: Nom du fichier (avec ou sans chemin).
    :param contenu: Texte à écrire dans le fichier.
    :param mode: Mode d'ouverture du fichier ('w' pour écraser, 'a' pour ajouter).
    """

    contenu = f"{datetime.now()}: {contenu}"
    try:
        with open(nom_fichier, mode, encoding="utf-8") as fichier:
            fichier.write(contenu)
            fichier.write("\n") 
    except Exception as e:
        print(f"Une erreur est survenue : {e}")


