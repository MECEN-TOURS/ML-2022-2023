"""Description.

Librairie pour le scraping de la table de composition du CAC40 sur wikipedia.
"""

from requests import get
from typing import Tuple, List, Iterator
from dataclasses import dataclass
import re

def recupere_page(adresse: str) -> str:
    requete = get(adresse)
    if requete.status_code != 200:
        raise ValueError("Impossible de récupérer la page!")
    return requete.text
    
def recupere_premiere_table(page: str) -> str:
    debut = page.find("<table")
    fin = page.find("</table>", debut) + 7
    return page[debut: fin + 1]

def recupere_tables(page: str) -> Iterator[str]:
    debut = page.find("<table")
    while debut != -1:
        fin = page.find("</table>", debut) + 7
        yield page[debut: fin + 1]
        debut = page.find("<table", fin)

def decoupe_lignes(table: str) -> List[str]:
    lignes = list()
    fin = 0
    while True:
        debut = table.find("<tr>", fin) + 4
        if debut == 3:
            break
        fin = table.find("</tr>", debut)
        lignes.append(table[debut:fin])
    return lignes        
        
def recupere_lignes(table: str) -> Iterator[str]:
    """Itère sur les contenus de chaque ligne.
    
    Attention on suppose que les balises ouvrantes <tr> sont 
    sans attribus!
    """
    debut = table.find("<tr>")
    while debut != -1:
        fin = table.find("</tr>", debut)
        yield table[debut + 4: fin]
        debut = table.find("<tr>", fin)
    
@dataclass
class Entreprise:
    nom: str
    lien: str
    secteur: str
    poids_indiciel: float
    chiffre_affaire_euros: int
    capitalisation_euros: int
    date_entree: Tuple[int, int, int]    
    
def transforme_ligne(ligne: str) -> Entreprise:
    ...