import arcade
import pygame


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
SCREEN_TITLE = "Mario Demo"

#Constantes para escalar los sprites
CHARACTER_SCALING = 0.17
GROUND_SCALING = 0.20 #escalamiento de tierra
CYLINDER_SCALING = 0.20 #escala del cilindro
ff = 20

#SPEED PLAYER
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20 #saltoN

# Cuántos píxeles mantener como margen mínimo entre el carácter
# y el borde de la pantalla.
LEFT_VIEWPORT_MARGIN = 20      # margen izquierdo margen
RIGHT_VIEWPORT_MARGIN = 20
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

class MyGame(arcade.Window):

    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE) #CORNFLOWER_BLUE

        self.coin_list = None # lista de monedas propias
        self.wall_list = None # #pared
        self.player_list = None #jugador
        self.background = None
        #Variable del sprite jugador
        self.player_sprite = None
        
        # Utilizado para realizar un seguimiento de nuestro desplazamiento
        self.view_bottom = 0 #vista inferior
        
        self.view_left = 0 #Vista propia a la izquierda

    def setup(self): #setup=config
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.background = arcade.load_texture("fondo.jpg")
        #Player
        image_source = "mario.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 93
        self.player_list.append(self.player_sprite)

        # Create the ground
        # Esto muestra el uso de un bucle para colocar varios sprites horizontalmente
        for x in range(0, 1250, 64):
            wall = arcade.Sprite("ground.png", GROUND_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        #cylinder
        # Esto muestra el uso de una lista de coordenadas para colocar sprites.
        coordinate_list = [[512, 110],
                            [256, 110],
                            [768, 110]]

        for coordinate in coordinate_list:
            # Agrega una caja en el suelo
            wall = arcade.Sprite("cylinder.png", CYLINDER_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)

        #Creathe the "physics engine"=Crea el "motor de física"
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)
    
    def on_draw(self): #en el dibujo
        arcade.start_render() #empieza a renderizar
        arcade.draw_texture_rectangle(0, 0,3000,3000, self.background,0, 100)
        
        self.player_list.draw()
        self.wall_list.draw()

    def on_key_press(self, key, modifiers): #presionar tecla
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():                  #motor de fisica salto
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Mueve al jugador con el motor de física.
        self.physics_engine.update()

        # --- Administrar el desplazamiento ---

        # Seguimiento si necesitamos cambiar la ventana gráfica

        changed = False

        # Scroll left ---- Desplazar izquierda
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            # Desplácese solo a números enteros. De lo contrario, terminamos con píxeles que
            # no se alinee en la pantalla 
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling -- Hacer el desplazamiento
            arcade.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left, self.view_bottom,SCREEN_HEIGHT + self.view_bottom)

def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
