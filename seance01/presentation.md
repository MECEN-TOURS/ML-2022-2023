# Exemple de projet

## Objectif

On imagine qu'on veut coder une application de recommandation d'annonces
immobilières "intéressantes".
Plus précisément, un acheteur potentiel renseignerait certains critères:

- tranche de prix,
- nombre de pièces min,
- quartiers
- ...

  L'application renverrait alors les 10 premières annonces correspondant
  à ces critères à examiner en priorité.

## Modélisation

La difficulté principale est d'arriver à définir ce qui constitue une annonce "intéressante".
On va raisonner de la façon suivante.
Chaque bien immobilier possède des caractéristiques physiques précises:

1. Surface
2. Quartier
3. Nombre de pièces
4. Appartement ou maison
5. Neuf ou ancien
6. Classe énergétique
7. Etc

On imagine alors qu'il existe une fonction déterminée mais inconnue qui
permettrait d'obtenir le prix rationnel du bien à partir de ces caractéristiques.
Le prix affiché de l'annonce est alors une version bruitée de ce prix dûe
à la subjectivité du vendeur.
Une annonce sera alors d'autant plus intéressante que l'écart entre le
prix rationnel et le prix affiché est grand.

## Procédure

1. La première étape consistera alors à récupérer les données brutes
   depuis internet via du "webscraping" par exemple sur le site [leboncoin](https://www.leboncoin.fr/).
   Á la fin de cette étape, on aura donc une base de données brutes
   sous forme non structurée (typiquement un fichier `json` ).
2. La deuxième partie consistera à nettoyer cette base de donnée (éliminer
   les doublons ou les annonces trop incomplètes par exemple) puis à numériser
   le résultat. Les caractéristiques de chaque annonce sera alors représenté
   par un vecteur de \mathbb{R}^D.
   Noter que si dans certains la numérisation est évidente (e.g. surface,
   nombre de pièce), dans d'autres cela peut être un peu plus délicat.
   Par exemple, dans le cas du quartier le fait de simplement numéroter les
   quartiers induit une notion d'ordre et de distance entre quartier totalement
   articielle qui pourrait biaiser la suite de la procédure.
   On verra dans ce cas qu'on peut utiliser un `OneHotEncoder`.
3. Á ce stade, on a donc $N$ vecteurs $(c_1,\ldots c_N) \in (\mathbb{R}^D)^N$
   et les prix affichés $(p_1,...,p_N) \in \mathbb{R}^N$ correspondant.
   On se donne alors un modèle c'est à dire une classe $\mathcal{P}$ de
   fonctions de $\mathbb{R}^D$ dans $\mathbb{R}$.
   On va alors chercher le modèle minimisant l'erreur quadratique moyenne
   par rapport aux annonces récupérées, mathématiquement

   $$
      P^*
      :=
      \underset{P \in \mathcal{P}}{\arg \min}
      \frac{1}{2N} \sum_{i=1}^N{(P(c_i) - p_i)^2}.
   $$

   L'idée étant d'adaptée du Théorème Centrale Limite qui prouve que
   la moyenne empirique de variables aléatoires indépendantes et identiquement
   distribuées converge vers la moyenne de la distribution (et les deux
   quantités sont obtenues comme minimiseurs des variances empiriques et de la variance).

4. La dernière étape consiste alors d'utiliser le minimiseur obtenu, en créant
   une application avec une interface utilisateur (GUI ou TUI) permettant de filtrer
   les annonces de la base de donnée, puis on triera les annonces restantes suivant
   la valeur numérique
   $$p_i - P^*(c_i).$$
