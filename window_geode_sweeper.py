# -*- coding: utf-8 -*-

"""
Exemple d'application pyglet (python + OpenGL).

Affiche un objet en 3D, qu'on peut faire tourner avec les touches de direction.
(Pour être précis, c'est la caméra qui tourne autour de l'objet,
et non pas l'objet qui tourne)

La nature de l'objet est à définir par du code extérieur.
On doit fournir un "mesh" à l'application. (Voir module mesh_builder.py).

L'application s'exécute dans une fenêtre retaillable. L'affichage
s'adapte à peu près à la taille de la fenêtre.

Trucs à faire pour plus tard : lorsqu'on clique sur l'objet,
l'application détecte quelle face a été cliquée. Inspirations possibles :
 - intersection ligne et plan :
   * http://geomalgorithms.com/a05-_intersect-1.html
   * http://mathworld.wolfram.com/CrossProduct.html

 - transformation d'un point cliqué à l'écran en rayon.
   * http://myweb.lmu.edu/dondi/share/cg/unproject-explained.pdf
"""

from __future__ import (unicode_literals, absolute_import,
                        print_function, division)
import pyglet
pgl = pyglet.gl

from vector3D import Vector3D
from camera import CameraAroundSphere

# Disable error checking for increased performance
#pyglet.options['debug_gl'] = False

# Plus cette valeur est petite, plus l'application sera rapide.
# (Sauf si l'ordinateur est trop lent,
# dans ce cas, ça ne sert à rien de mettre une valeur faible).
PERIOD_GAME_CYCLE_SECONDS = 0.01

class WindowGeodeSweeper(pyglet.window.Window):
    """
    Classe principale, définissant une application pyglet.
    Voir doc de pyglet pour plus de détails. Cet exemple est quand même
    assez simple.    
    """

    # --- Diverses constantes, (valeurs déterminées au feeling) ---

    # paramètres fovy, zNear, zFar.
    # Voir documentation de la fonction gluPerspective
    # https://www.opengl.org/sdk/docs/man2/xhtml/gluPerspective.xml
    FIELD_OF_VIEW_ANGLE_Y = 40.0
    Z_NEAR = 1.0
    Z_FAR = 40.0

    # Distance entre la caméra et le centre de l'espace O.
    # (La caméra se déplace sur une sphère centrée en O, de rayon DIST_CAM).
    DIST_CAM = 15

    # Facteur d'agrandissement des coordonnées de l'espace.
    SCALE_COORD = 3.0

    # Distance de déplacement orthogonal de la caméra, à chaque cycle.
    CAM_DELTA = 0.05

    def init_geode_sweeper(self, mesh):
        """
        À exécuter au début, juste après avoir instancié l'application.

        :param mesh: classe Mesh (ou dérivée). Définit l'objet 3D à afficher
            (coordonnées des sommets, couleurs, faces, ...)                    
        """
        self.mesh = mesh
        self.cam = CameraAroundSphere()        
        pgl.glEnable(pgl.GL_DEPTH_TEST)        

    def on_resize(self, width, height):
        """
        Fonction qui s'exécute lorsque la fenêtre de l'application est
        retaillée. (Et donc, elle s'exécute forcément une fois au début,
        à la création de la fenêtre. 
        Initialise/met à jour le contexte d'affichage OpenGL.
        """
        pgl.glViewport(0, 0, width, height)
        pgl.glMatrixMode(pgl.GL_PROJECTION)
        pgl.glLoadIdentity()
        if height != 0:
            pgl.gluPerspective(
                WindowGeodeSweeper.FIELD_OF_VIEW_ANGLE_Y,
                # TODO : ne marche pas comme j'aurais voulu lorsque la fenêtre
                # est plus haute que large. L'image devrait se réduire.
                width / height,
                WindowGeodeSweeper.Z_NEAR,
                WindowGeodeSweeper.Z_FAR)
        return pyglet.event.EVENT_HANDLED

    def on_draw(self):
        """
        Fonction qui s'exécute à chaque redessin de la fenêtre.
        Récupère la position actuelle de la caméra, et dessine le mesh.
        """

        # Effaçage de l'écran et du contexte OpenGL.
        pgl.glClearColor(0.0, 0.0, 0.0, 1)
        pgl.glClear(pgl.GL_COLOR_BUFFER_BIT | pgl.GL_DEPTH_BUFFER_BIT)

        # Positionnement de la caméra, de l'échelle, etc.
        pgl.glMatrixMode(pgl.GL_MODELVIEW)
        pgl.glLoadIdentity()
        cam_pos_final = self.cam.pos * WindowGeodeSweeper.DIST_CAM
        pgl.gluLookAt(
            cam_pos_final.x, cam_pos_final.y, cam_pos_final.z, 
            self.cam.lookat.x, self.cam.lookat.y, self.cam.lookat.z,
            self.cam.v_up.x, self.cam.v_up.y, self.cam.v_up.z)
        scale_coord = WindowGeodeSweeper.SCALE_COORD
        pgl.glScalef(scale_coord, scale_coord, scale_coord)

        # Dessin du mesh. On prend le tableau contenant les coordonnées,
        # et on le balance en une seule fois chacun à la carte graphique,
        # à l'aide de la fonction OpenGL idoine.
        # Pareil pour le tableau contenant les couleurs.
        # Ça permet d'optimiser l'affichage.
        pgl.glEnableClientState(pgl.GL_VERTEX_ARRAY)
        pgl.glEnableClientState(pgl.GL_COLOR_ARRAY)
        pgl.glColorPointer(3, pgl.GL_FLOAT, 0, self.mesh.glfloat_colors)
        pgl.glVertexPointer(3, pgl.GL_FLOAT, 0, self.mesh.glfloat_vertices)
        # Attention au dernier param de glDrawArrays !
        # On n'indique pas le nombre d'élément du tableau,
        # mais le nombre d'objets qu'on veut dessiner.
        # C'est pas comme la fonction glDrawElements.
        pgl.glDrawArrays(
            pgl.GL_TRIANGLES,
            0,
            len(self.mesh.glfloat_vertices) // 3)
        pgl.glDisableClientState(pgl.GL_COLOR_ARRAY)
        pgl.glDisableClientState(pgl.GL_VERTEX_ARRAY)

    # -- Fonctions pour initialiser les déplacement de caméra. --

    def move_lat_right(self):
        self.cam.delta_lateral = WindowGeodeSweeper.CAM_DELTA
    def move_lat_left(self):
        self.cam.delta_lateral = -WindowGeodeSweeper.CAM_DELTA
    def move_longi_up(self):
        self.cam.delta_longitudinal = -WindowGeodeSweeper.CAM_DELTA
    def move_longi_down(self):
        self.cam.delta_longitudinal = WindowGeodeSweeper.CAM_DELTA

    def on_key_press(self, symbol, modifiers):
        """
        Fonction qui s'exécute lorsqu'on appuie sur une touche.
        Effectue la correspondance entre la touche appuyée et l'action.
        Actions prises en compte :
         - Démarrage des mouvements de la caméra avec les flèches de direction.
         - Fermeture de l'appli avec Echap.
        """
        function_from_key_pressed = {
            pyglet.window.key.RIGHT : self.move_lat_right,
            pyglet.window.key.LEFT : self.move_lat_left,
            pyglet.window.key.UP : self.move_longi_up,
            pyglet.window.key.DOWN : self.move_longi_down,
            pyglet.window.key.ESCAPE : self.close,
        }
        function_to_exec = function_from_key_pressed.get(symbol)
        if function_to_exec is not None:
            function_to_exec()

    # -- Fonctions pour arrêter les déplacement de la caméra. --

    def stop_move_lat(self):
        self.cam.delta_lateral = 0.0
    def stop_move_longi(self):
        self.cam.delta_longitudinal = 0.0

    def on_key_release(self, symbol, modifiers):
        """
        Fonction qui s'exécute lorsqu'on relâche sur une touche.
        Action prise en compte :
         - Arrêt des mouvements de la caméra lorsque des flèches de direction
           sont relâchées.
        """
        function_from_key_released = {
            pyglet.window.key.RIGHT : self.stop_move_lat,
            pyglet.window.key.LEFT : self.stop_move_lat,
            pyglet.window.key.UP : self.stop_move_longi,
            pyglet.window.key.DOWN : self.stop_move_longi,
        }
        function_to_exec = function_from_key_released.get(symbol)
        if function_to_exec is not None:
            function_to_exec()

    def update(self, dt):
        """
        Fonction exécutée à chaque cycle de l'application.
        Met à jour la position de la caméra en fonction des mouvements
        en cours.
        """
        self.cam.slide_with_deltas()


# Instanciation de l'application.
# (Le code extérieur devra exécuter la fonction init_geode_sweeper).
window_geode_sweeper = WindowGeodeSweeper(
    fullscreen=False, vsync=False, resizable=True,
    height=600, width=600)

