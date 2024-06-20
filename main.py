from ursina import *

from cube_model import Cube
from Algoritms import Algorithms



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
                    angel = -90
            elif side_name == 'RIGHT':
                if streak:
                    angel = -90
            elif side_name == 'UP':
                if streak:
                    angel = -90
            elif side_name == 'DOWN':
                if not streak:
                    angel = -90
            elif side_name == 'FACE':
                if streak:
                    angel = -90
            elif side_name == 'BACK':
                if not streak:
                    angel = -90

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
                if streak:
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


class Game:
    def __init__(self):
        self.app = Ursina()

        window.fullscreen = True
        EditorCamera(rotation=(30, -20, 0), zoom_speed=0, move_speed=0)

        Entity(model='sphere', scale=1000, texture='background_grey', double_sided=True)
        self.model, self.texture = 'custom_cube', 'rubik_texture'

        self.cube = RubiksCube()

        self.solve_button = Button(text='Собрать кубик', color=color.azure, position=(0, 0.4), scale=(0.5, 0.1))
        self.solve_button.on_click = self.solve_cube

        '''self.mode_button = Button(text='Сменить режим', color=color.azure, position=(0, -0.4), scale=(0.5, 0.1))
        self.mode_button.on_click = self.cube.change_game_mode'''

        # управление
        self.R_button = Button(text='R', color=color.azure, position=(0.4, 0.4), scale=(0.1, 0.1))
        self.R_button.on_click = lambda: [self.cube.rotate_side('RIGHT', False),
                                          self.cube.cube_instance.rotate_R()] # if self.cube.action_mode and self.cube.action_flag else None

        self.R_streak_button = Button(text="R'", color=color.azure, position=(0.6, 0.4), scale=(0.1, 0.1))
        self.R_streak_button.on_click = lambda: [self.cube.rotate_side('RIGHT', True), self.cube.cube_instance.rotate_R_streak()]

        self.L_button = Button(text='L', color=color.azure, position=(0.4, 0.25), scale=(0.1, 0.1))
        self.L_button.on_click = lambda: [self.cube.rotate_side('LEFT', False), self.cube.cube_instance.rotate_L()]

        self.L_streak_button = Button(text="L'", color=color.azure, position=(0.6, 0.25), scale=(0.1, 0.1))
        self.L_streak_button.on_click = lambda: [self.cube.rotate_side('LEFT', True), self.cube.cube_instance.rotate_L_streak()]

        self.F_button = Button(text='F', color=color.azure, position=(0.4, 0.1), scale=(0.1, 0.1))
        self.F_button.on_click = lambda: [self.cube.rotate_side('FACE', False), self.cube.cube_instance.rotate_F()]

        self.F_streak_button = Button(text="F'", color=color.azure, position=(0.6, 0.1), scale=(0.1, 0.1))
        self.F_streak_button.on_click = lambda: [self.cube.rotate_side('FACE', True), self.cube.cube_instance.rotate_F_streak()]

        self.U_button = Button(text='U', color=color.azure, position=(0.4, -0.05), scale=(0.1, 0.1))
        self.U_button.on_click = lambda: [self.cube.rotate_side('UP', False), self.cube.cube_instance.rotate_U()]

        self.U_streak_button = Button(text="U'", color=color.azure, position=(0.6, -0.05), scale=(0.1, 0.1))
        self.U_streak_button.on_click = lambda: [self.cube.rotate_side('UP', True), self.cube.cube_instance.rotate_U_streak()]

        self.B_button = Button(text='B', color=color.azure, position=(0.4, -0.2), scale=(0.1, 0.1))
        self.B_button.on_click = lambda: [self.cube.rotate_side('BACK', False), self.cube.cube_instance.rotate_B()]

        self.B_streak_button = Button(text="B'", color=color.azure, position=(0.6, -0.2), scale=(0.1, 0.1))
        self.B_streak_button.on_click = lambda: [self.cube.rotate_side('BACK', True), self.cube.cube_instance.rotate_B_streak()]

        self.D_button = Button(text='D', color=color.azure, position=(0.4, -0.35), scale=(0.1, 0.1))
        self.D_button.on_click = lambda: [self.cube.rotate_side('DOWN', False), self.cube.cube_instance.rotate_D()]

        self.D_streak_button = Button(text="D'", color=color.azure, position=(0.6, -0.35), scale=(0.1, 0.1))
        self.D_streak_button.on_click = lambda: [self.cube.rotate_side('DOWN', True), self.cube.cube_instance.rotate_D_streak()]


    def solve_cube(self):
        a = Algorithms()
        a.low_cross(cube_model=self.cube.cube_instance, cube_ui=self.cube, cube_solved=self.cube.cube_solved)
        a.F1L(cube_model=self.cube.cube_instance, cube_ui=self.cube, cube_solved=self.cube.cube_solved)
        a.F2L(cube_model=self.cube.cube_instance, cube_ui=self.cube, cube_solved=self.cube.cube_solved)
        a.up_cross_colors(cube_model=self.cube.cube_instance, cube_ui=self.cube, cube_solved=self.cube.cube_solved)
        a.final(cube_model=self.cube.cube_instance, cube_ui=self.cube, cube_solved=self.cube.cube_solved)


    def run(self):
        self.app.run()


if __name__ == '__main__':
    game = Game()
    game.run()
