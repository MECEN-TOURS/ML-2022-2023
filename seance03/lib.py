"""Description.

Librairie de ML.
Utilisation unique donc pas de documentation/test/typage...
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt


class Realite:
    def __init__(self, gauche, droite, fonction):
        self.gauche = gauche
        self.droite = droite
        self.fonction = fonction
        
    def dessine(self, repere, nb_points=100):
        x = np.linspace(self.gauche, self.droite, nb_points)
        y = self.fonction(x)
        repere.plot(x, y, color="black", label="fonction cachée")
        
class Donnees:
    def __init__(self, points, mesures):
        self.points =  points
        self.mesures = mesures
        
    def __repr__(self):
        return f"Donnees(points={self.points}, mesures={self.mesures})"
        
    def dessine(self, repere, legende=None):
        if legende is None:
            repere.scatter(self.points, self.mesures, label="mesures bruitées")
        else:
            repere.scatter(self.points, self.mesures, label=legende)
            
    def __iter__(self):
        return iter(zip(self.points, self.mesures))
        
def echantillon_deterministe(nb_points: int, reel: Realite, taille_bruit: float) -> Donnees:
    points = np.linspace(reel.gauche, reel.droite, nb_points)
    valeurs = reel.fonction(points)
    mesures = valeurs + np.random.normal(loc=0.0, scale=taille_bruit, size=(nb_points,))
    return Donnees(points=points, mesures=mesures)

class Modele:
    def __init__(self, nb_bases:int, epsilon: float, realite: Realite):
        self.realite = realite
        self.bases = np.linspace(realite.gauche, realite.droite, nb_bases)
        self.nb_bases = nb_bases
        self.epsilon = epsilon
              
    def _evalue(self, points, coefficients):
        resultat = 0
        for coef, base in zip(coefficients, self.bases):
            resultat = resultat + coef * np.exp(-(points - base) ** 2 / (2 * self.epsilon) )
        return resultat
        
    def entrainement(self, donnees: Donnees):
        def erreur(cs):
            return (
                np.sum(
                    (
                        self._evalue(points=donnees.points, coefficients=cs) 
                        - donnees.mesures
                    ) ** 2
                )
                / (2 * len(donnees.points))
            )
        resultat = opt.minimize(fun=erreur, x0=np.zeros_like(self.bases))
        if resultat.success:
            self._meilleurs_coefficients = resultat.x
            self.erreur_minimale = resultat.fun
        else:
            raise ValueError("Impossible de faire converger le solveur")
                
    def dessine(self, rep, nb_points=100):
        x = np.linspace(self.realite.gauche, self.realite.droite, nb_points)
        y = self(x)
        rep.plot(x, y, label="prédicteur {}, {}".format(self.nb_bases, self.epsilon))
        
    def __call__(self, x):
        if "_meilleurs_coefficients" in self.__dict__: 
            resultat = 0
            for coef, base in zip(self._meilleurs_coefficients, self.bases):
                resultat = resultat + coef * np.exp(-(x - base) ** 2 / (2 * self.epsilon) )
            return resultat
        else:
            raise ValueError("Le modèle doit d'abord être entrainé.")
        