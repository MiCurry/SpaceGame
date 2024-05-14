import arcade

from SpaceGame.diagnostics.Diagnostics import DiagnosticsController

class SpaceGameDiagnostics(DiagnosticsController):
    def __init__(self, game):
        super().__init__(game)

    def setup(self):
        self.add_diagnostic(arcade.key.I,
                            lambda game: f"Left Stick: ({game.players[0].controller.x:.5f}, {game.players[0].controller.y:.5f})",
                            display_at_start=False)

        self.add_diagnostic(arcade.key.O,
                            lambda game: f"Right Stick: ({game.players[0].controller.z:.5f}, {game.players[0].controller.rz:.5f})",
                            display_at_start=False)

        self.add_diagnostic(arcade.key.U,
                            lambda game: f"Rotation: ({game.players[0].applied_rotational_vel:.5f}, {game.players[0].applied_rotational_vel:.5f})",
                            display_at_start=False)

        self.add_diagnostic(arcade.key.Y,
                            lambda game: f"Acceleration: ({game.players[0].dx:.5f}, {game.players[0].dy:.5f})",
                            display_at_start=False)

        self.add_diagnostic(arcade.key.H,
                            lambda game: f"Velocity: ({game.players[0].body.velocity[0]:.5f}, {game.players[0].body.velocity[1]:.5f})",
                            display_at_start=False)

        self.add_diagnostic(arcade.key.J,
                            lambda game: f"Angular Vel: ({game.players[0].body.angular_velocity:.5f})",
                            display_at_start=False)

        self.add_diagnostic(arcade.key.P,
                            lambda game: f"Position: P1: {game.players[0].position} P2: {game.players[1].position}))",
                            display_at_start=False)
