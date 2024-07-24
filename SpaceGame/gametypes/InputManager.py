from arcade.future.input import ControllerAxes, ControllerButtons, InputManager, Keys

class PlayerInputManager:
    def __init__(self, input_type):
        self.input_manager = arcade.InputManager()
        self.add_actions_and_axis()

        if input_type == 'CONTROLLER':
            self.add_controller_inputs()
        elif input_type == 'KEYBOARD':
            self.add_keyboard_inputs()


    def add_actions_and_axis(self):
        self.input_manager.new_action('shoot')
        self.input_manager.new_axis('up_down')
        self.input_manager.new_axis('left_right')
        self.input_manager.new_axis('rotate')

    def add_controller_inputs(self):
        self.input_manager.add_action_input('shoot', ControllersButton.)


    def add_keyboard_inputs(self):
        pass