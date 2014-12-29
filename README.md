# Geode Sweeper #

Exemple de 3D simple, avec python et OpenGL (librairie pyglet).

Affiche un cube multicolore, ou un icosaèdre vert et blanc.

On peut faire tourner l'objet avec les touches de direction. (Pour être plus précis, c'est la caméra qui tourne autour de l'objet, et non pas l'objet qui tourne)

![screenshot icosaèdre](https://raw.githubusercontent.com/darkrecher/Geode-Sweeper/master/screenshot_icosahedron.png)

![screenshot cube](https://raw.githubusercontent.com/darkrecher/Geode-Sweeper/master/screenshot_cube.png)

# État actuel #

C'est du code "prototype". Le but serait d'essayer de faire un genre de démineur en 3D sur un icosaèdre. D'où le nom : Geode Sweeper.

Je n'ai pas prévu d'avancer ce projet pour l'instant. Mais qui sait ce que l'avenir nous réserve...


# Doc de conception #

Il n'y en a pas. (Pour l'instant)


# Installation (windows) #

Récupérez le dernier python 2.x, par ici : https://www.python.org/downloads/

J'ai pris le 2.7.9. Le lien sur la page s'appelle "Windows x86 MSI installer"

Le fichier récupéré a pour nom : python-2.7.9.msi

Prenez obligatoirement la version 32 bits, car la librairie pyglet ne marche pas avec le python 64 bits. (Un problème similaire a été rapporté sur Mac OSX 64 bits : http://stackoverflow.com/questions/16308100/enthought-canopy-64bit-on-osx-import-pyglet-gl-failure )

pip est pré-installé avec le python 2.7.9, ce qui est bien sympa.

Après avoir installé python, ouvrez un shell windows :

    cd c:\python27
    Scripts\pip.exe

Si vous avez installé Avast, il va râler, mais acceptera d'exécuter pip au bout d'un petit moment. Des informations sur l'usage de l'outil devrait s'afficher dans la console.

Installez la libraire pyglet, via la commande suivante :

    Scripts\pip.exe install pyglet

Téléchargez et décompressez le contenu de ce repository, puis revenez au shell windows.

    cd <emplacement du repository décompressé>

Pour afficher le cube :

    c:\python27\python.exe main_cube.py

Pour afficher l'icosaèdre :

    c:\python27\python.exe main_icosahedron.py


# Crédits #

Créé par Réchèr.

Le code et cette doc sont sous la double licence : Art Libre ou Creative Commons CC-BY (au choix).

Repository : https://github.com/darkrecher/Geode-Sweeper

Mon blog : http://recher.wordpress.com
