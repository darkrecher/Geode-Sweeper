# Geode Sweeper #

Exemple de 3D simple, avec python et OpenGL (librairie pyglet).
Affiche un icosaèdre vert et blanc.
On peut le faire tourner avec les flèches. (Pour être plus précis, c'est la caméra qui tourne autour de l'objet, et non pas l'objet qui tourne)


# État actuel #

C'est du code "prototype". Le but, ce serait d'essayer de faire un genre de démineur en 3D sur un icosaèdre. D'où le nom : Geode Sweeper.

Je n'ai pas prévu d'avancer ce projet pour l'instant. Mais qui sait ce que l'avenir nous réserve...


# Doc de conception #

Il n'y en a pas. (Pour l'instant)


# Installation #

Récupérer le dernier python 2.x
https://www.python.org/downloads/

(j'ai pris le 2.7.9)
"Windows x86 MSI installer"
python-2.7.9.msi

le 64 bits marche pas. Apparemment, il y a le même problème avec le 64 bits de Mac OSX.
http://stackoverflow.com/questions/16308100/enthought-canopy-64bit-on-osx-import-pyglet-gl-failure


(shell windows)

`cd c:\python27\`
`python`

ça marche.

`exit()`


pip est pré-installé avec le python 2.7.9, ça c'est sympa.

`Scripts\pip`

avast râle, mais finit par bien vouloir l'exécuter. Ça renvoit un usage.

`Scripts\pip install pyglet`

Ça met du temps et ça crache un peu de log.


`python`
`import pyglet`
`import pyglet.gl`

ça marche.

