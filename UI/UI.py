from ursina import *

from cube_model import Cube


def create_sensor(name, pos, scale):
    return Entity(
        name=name,
        position=pos,
        model='cube',
        color=color.dark_gray,
        scale=scale,
        collider='box',
        visible=False
    )


class Algorithms:
    def pif_paf_right(self, cube_model, cube_ui):  # правый пифпаф
        cube_ui.rotate_side('RIGHT', False)
        cube_model.rotate_R()
        cube_ui.rotate_side('UP', False)
        cube_model.rotate_U()
        cube_ui.rotate_side('RIGHT', True)
        cube_model.rotate_R_streak()
        cube_ui.rotate_side('UP', True)
        cube_model.rotate_U_streak()

    def pif_paf_left(self, cube_model, cube_ui):  # левый пифпаф
        cube_model.rotate_L_streak()
        cube_ui.rotate_side('LEFT', True)
        cube_model.rotate_U_streak()
        cube_ui.rotate_side('UP', True)
        cube_model.rotate_L()
        cube_ui.rotate_side('LEFT', False)
        cube_model.rotate_U()
        cube_ui.rotate_side('UP', False)

    def F1L(self, cube_model, cube_ui, cube_solved):  # сборка первого слоя
        z0 = -1
        x0, y0 = 1, 1
        for _ in range(4):
            colors = cube_model.get_colors(x0, y0, z0)
            solved_colors = cube_solved.get_colors(x0, y0, z0)

            if set(colors.values()) == set(
                    solved_colors.values()):  # кубик стоит на месте, но цвета необходимо перевернуть
                while cube_model.get_colors(x0, y0, z0) != solved_colors:
                    self.pif_paf_right(cube_model, cube_ui)
            elif set(colors.values()) != set(solved_colors.values()):

                # найти нужный кубик:
                x1, y1, z1, = 0, 0, 0
                for x in (-1, 1):
                    for y in (-1, 1):
                        for z in (-1, 1):
                            if set(cube_model.get_colors(x, y, z).values()) == set(solved_colors.values()):
                                x1, y1, z1, = x, y, z

                # перевести нужный кубик на верхнюю грань над нужным положением:
                if z1 == -1:
                    if (x1, y1) == (1, -1):
                        self.pif_paf_left(cube_model, cube_ui)
                        cube_model.rotate_U_streak()
                        cube_ui.rotate_side('UP', True)
                    elif (x1, y1) == (-1, -1):
                        cube_model.rotate_cube_U_streak()
                        cube_ui.rotate_cube('UP', True)
                        self.pif_paf_left(cube_model, cube_ui)
                        cube_model.rotate_cube_U()
                        cube_ui.rotate_cube('UP', False)
                        # функция поворота куба в ui
                        for _ in range(2):
                            cube_model.rotate_U()
                            cube_ui.rotate_side('UP', False)
                    else:
                        cube_model.rotate_cube_U()
                        cube_ui.rotate_cube('UP', False)
                        self.pif_paf_right(cube_model, cube_ui)
                        cube_model.rotate_cube_U_streak()
                        cube_ui.rotate_cube('UP', True)
                        cube_model.rotate_U()
                        cube_ui.rotate_side('UP', False)
                # поставить кубик на место:
                if cube_model.get_colors(x0, y0, 1)['R'] == cube_model.get_colors(0, 0, -1)['D']:
                    self.pif_paf_right(cube_model, cube_ui)
                elif cube_model.get_colors(x0, y0, 1)['U'] == cube_model.get_colors(0, 0, -1)['D']:
                    for _ in range(3):
                        self.pif_paf_right(cube_model, cube_ui)
                else:
                    cube_model.rotate_cube_U()
                    cube_ui.rotate_cube('UP', False)
                    self.pif_paf_left(cube_model, cube_ui)
                    cube_model.rotate_cube_U_streak()  # важно повернуть собранный куб тоже
                    cube_ui.rotate_cube('UP', True)
            cube_model.rotate_cube_U()
            cube_ui.rotate_cube('UP', False)
            cube_solved.rotate_cube_U()


class RubiksCube:
    def __init__(self, cube_model='custom_cube', rubik_texture='rubik_texture'):
        self.cube_instance = Cube(3)
        self.cube_solved = Cube(3)
        self.model = cube_model
        self.texture = rubik_texture

        self.LEFT = {Vec3(-1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.RIGHT = {Vec3(1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.UP = {Vec3(x, 1, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.DOWN = {Vec3(x, -1, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.FACE = {Vec3(x, y, -1) for x in range(-1, 2) for y in range(-1, 2)}
        self.BACK = {Vec3(x, y, 1) for x in range(-1, 2) for y in range(-1, 2)}

        self.SIDE_POSITIONS = self.LEFT | self.DOWN | self.FACE | self.BACK | self.RIGHT | self.UP

        self.PARENT = Entity(model=self.model, texture=self.texture)
        self.CUBES = [Entity(
            model=self.model,
            texture=self.texture,
            position=pos,
            parent=self.PARENT
        ) for pos in self.SIDE_POSITIONS]

        self.rotation_axes = {
            'LEFT': 'x',
            'RIGHT': 'x',
            'UP': 'y',
            'DOWN': 'y',
            'FACE': 'z',
            'BACK': 'z'
        }

        self.cubes_side_positions = {
            'LEFT': self.LEFT,
            'RIGHT': self.RIGHT,
            'UP': self.UP,
            'DOWN': self.DOWN,
            'FACE': self.FACE,
            'BACK': self.BACK
        }

        self.action_flag = True
        self.action_mode = False
        self.animation_time = 0.4
        self.action_queue = []

    def rotate_side(self, side_name, streak):
        if not self.action_flag:
            self.action_queue.append((side_name, streak, 'side'))
            return
        angel = 90
        if self.cube_instance:
            if side_name == 'LEFT':
                if not streak:
                    self.cube_instance.rotate_L()
                    angel = -90
                else:
                    self.cube_instance.rotate_L_streak()
            elif side_name == 'RIGHT':
                if not streak:
                    self.cube_instance.rotate_R()
                else:
                    self.cube_instance.rotate_R_streak()
                    angel = -90
            elif side_name == 'UP':
                if not streak:
                    self.cube_instance.rotate_U()
                else:
                    self.cube_instance.rotate_U_streak()
                    angel = -90
            elif side_name == 'DOWN':
                if not streak:
                    self.cube_instance.rotate_D()
                    angel = -90
                else:
                    self.cube_instance.rotate_D_streak()
            elif side_name == 'FACE':
                if not streak:
                    self.cube_instance.rotate_F()
                else:
                    self.cube_instance.rotate_F_streak()
                    angel = -90
            elif side_name == 'BACK':
                if not streak:
                    self.cube_instance.rotate_B()
                    angel = -90
                else:
                    self.cube_instance.rotate_B_streak()

        self.action_flag = False

        positions = self.cubes_side_positions[side_name]
        rotation_axis = self.rotation_axes[side_name]
        self.change_parent_to_scene()

        for cube in self.CUBES:
            if cube.position in positions:
                cube.parent = self.PARENT
                rotate_method = getattr(self.PARENT, f'animate_rotation_{rotation_axis}')
                rotate_method(angel, duration=self.animation_time)

        invoke(self.change_animation_flag, delay=self.animation_time + 0.05)

    def rotate_cube(self, side_name, streak):
        if not self.action_flag:
            self.action_queue.append((side_name, streak, 'cube'))
            return
        angel = 90
        rotation_axis = ''
        if self.cube_instance:
            if side_name == 'RIGHT':
                rotation_axis = 'x'
                if not streak:
                    pass
                else:
                    pass
            elif side_name == 'UP':
                rotation_axis = 'y'
                if not streak:
                    self.cube_instance.rotate_cube_U()
                    self.cube_solved.rotate_cube_U()
                else:
                    self.cube_instance.rotate_cube_U_streak()
                    self.cube_solved.rotate_cube_U_streak()
                    angel = -90
            elif side_name == 'FACE':
                rotation_axis = 'z'
                pass

        self.action_flag = False

        positions = self.SIDE_POSITIONS
        self.change_parent_to_scene()

        for cube in self.CUBES:
            if cube.position in positions:
                cube.parent = self.PARENT
                rotate_method = getattr(self.PARENT, f'animate_rotation_{rotation_axis}')
                rotate_method(angel, duration=self.animation_time)

        invoke(self.change_animation_flag, delay=self.animation_time + 0.05)

    def change_parent_to_scene(self):
        for cube in self.CUBES:
            if cube.parent == self.PARENT:
                world_pos, world_rot = round(cube.world_position, 1), cube.world_rotation
                cube.parent = scene
                cube.position, cube.rotation = world_pos, world_rot

        self.PARENT.rotation = 0

    def change_game_mode(self):
        self.action_mode = not self.action_mode

    def change_animation_flag(self):
        self.action_flag = not self.action_flag

        if self.action_flag and self.action_queue:
            next_action = self.action_queue.pop(0)
            if next_action[2] == 'side':
                self.rotate_side(next_action[0], next_action[1])
            elif next_action[2] == 'cube':
                self.rotate_cube(next_action[0], next_action[1])


class InputHandler(Entity):
    KEYS = ['r', 'l', 'd', 'u', 'f', 'b', 't', 'i', ';', 'g', 's', 'n', 'y']

    def __init__(self, cube: RubiksCube):
        super().__init__()
        self.cube = cube

    def input(self, key):
        if key in self.KEYS and self.cube.action_mode and self.cube.action_flag:
            for info in mouse.collisions:
                side_name = info.entity.name
                if key == 'mouse1' and side_name in 'LEFT RIGHT FACE BACK':
                    self.cube.rotate_side(side_name, False)
                    break
                elif key == 'mouse3' and side_name in 'UP DOWN':
                    self.cube.rotate_side(side_name, False)
                    break
                elif key == 'r':
                    self.cube.rotate_side('RIGHT', False)
                elif key == 't':
                    self.cube.rotate_side('RIGHT', True)
                elif key == 'l':
                    self.cube.rotate_side('LEFT', False)
                elif key == ';':
                    self.cube.rotate_side('LEFT', True)
                elif key == 'u':
                    self.cube.rotate_side('UP', False)
                elif key == 'i':
                    self.cube.rotate_side('UP', True)
                elif key == 'd':
                    self.cube.rotate_side('DOWN', False)
                elif key == 's':
                    self.cube.rotate_side('DOWN', True)
                elif key == 'b':
                    self.cube.rotate_side('BACK', False)
                elif key == 'n':
                    self.cube.rotate_side('BACK', True)
                elif key == 'f':
                    self.cube.rotate_side('FACE', False)
                elif key == 'g':
                    self.cube.rotate_side('FACE', True)
                elif key == 'y':
                    self.cube.rotate_cube('UP', False)


class Game:
    def __init__(self):
        self.app = Ursina()

        window.fullscreen = True
        EditorCamera(rotation=(30, -20, 0))

        Entity(model='sphere', scale=1000, texture='background_grey', double_sided=True)
        self.model, self.texture = 'custom_cube', 'rubik_texture'

        self.LEFT_sensor = create_sensor(name='LEFT', pos=(-0.99, 0, 0), scale=(1, 3, 3))
        self.FACE_sensor = create_sensor(name='FACE', pos=(0, 0, -0.99), scale=(3, 3, 1))
        self.BACK_sensor = create_sensor(name='BACK', pos=(0, 0, 0.99), scale=(3, 3, 1))
        self.RIGHT_sensor = create_sensor(name='RIGHT', pos=(0.99, 0, 0), scale=(1, 3, 3))
        self.UP_sensor = create_sensor(name='UP', pos=(0, 0.99, 0), scale=(3, 1, 3))
        self.DOWN_sensor = create_sensor(name='DOWN', pos=(0, -0.99, 0), scale=(3, 1, 3))

        self.cube = RubiksCube()
        self.input_handler = InputHandler(self.cube)

        self.solve_button = Button(text='Собрать кубик', color=color.azure, position=(0, 0.4), scale=(0.5, 0.1))
        self.solve_button.on_click = self.solve_cube

        self.mode_button = Button(text='Сменить режим', color=color.azure, position=(0, -0.4), scale=(0.5, 0.1))
        self.mode_button.on_click = self.cube.change_game_mode

        # управление
        self.R_button = Button(text='R', color=color.azure, position=(0.4, 0.4), scale=(0.1, 0.1))
        self.R_button.on_click = lambda: self.cube.rotate_side('RIGHT', False)

    def solve_cube(self):
        a = Algorithms()
        a.pif_paf_right(cube_model=self.cube.cube_instance, cube_ui=self.cube)  # , cube_solved=self.cube.cube_solved)

    def run(self):
        self.app.run()


if __name__ == '__main__':
    game = Game()
    game.run()
