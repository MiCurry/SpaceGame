import arcade


class Scoreboard:
    def __init__(self,
                 game_type,
                 players,
                 starting_lives=10,
                 time=3600):
        self.score_text = None
        self.timer_text = None
        self.game_type = game_type
        self.players = players
        self.starting_lives = starting_lives

        self.time = time
        self.total_time = time

        self.kills = []
        self.deaths = []
        self.lives = []

    def setup(self):
        self.setup_timer()
        self.init_score()
        self.init_player_lives()
        self.init_kills()
        self.init_deaths()

    def init_kills(self):
        for player in self.players:
            self.kills.append(0)

    def init_deaths(self):
        for player in self.players:
            self.deaths.append(0)

    def init_player_lives(self):
        for player in self.players:
            self.lives.append(0)

    def add_kill(self, killer, killed):
        self.kills[killer.player_number] += 1
        self.add_death(killed.player_number)

    def add_death(self, player):
        self.deaths[player] += 1

        if self.game_type == 'stock':
            self.sub_life(player)

    def sub_life(self, player):
        self.lives[player] -= 1

    def draw_timer(self):
        camera = arcade.get_window().current_camera
        vp = camera.projection.viewport
        self.timer_text.x = camera.view.position[0]
        self.timer_text.y = camera.view.position[1] - (vp[3] / 2) + vp[3] - 100
        self.timer_text.draw()

    def draw_score(self):
        camera = arcade.get_window().current_camera
        vp = camera.projection.viewport
        self.score_text.x = camera.view.position[0]
        self.score_text.y = camera.view.position[1] - (vp[3] / 2) + vp[3] - 150
        self.score_text.draw()

    def on_draw(self):
        self.draw_timer()
        self.draw_score()

    def timer_elapsed(self):
        if self.total_time <= 0:
            return True

    def setup_timer(self):
        window = arcade.get_window()
        self.timer_text = arcade.Text(
            text="00:00:00",
            x=window.width // 2,
            y=window.height // 2 - 50,
            color=arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
        )
        minutes = int(self.total_time) // 60
        seconds = int(self.total_time) % 60
        seconds_100s = int((self.total_time - seconds) * 100)
        self.timer_text.text = f"{minutes:02d}:{seconds:02d}:{seconds_100s:02d}"

    def init_score(self):
        window = arcade.get_window()
        self.score_text = arcade.Text(
            text="0 vs 0",
            x=window.width // 2,
            y=window.height // 2 - 50,
            color=arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
        )

    def update_timer(self, delta_time):
        self.total_time -= delta_time

        if self.total_time <= 0:
            self.timer_elapsed()

        minutes = int(self.total_time) // 60
        seconds = int(self.total_time) % 60
        self.timer_text.text = f"{minutes:02d}:{seconds:02d}"

    def update_score(self):
        self.score_text.text = f"{self.kills[self.players[0].player_number]} to {self.kills[self.players[1].player_number]}"

    def on_update(self, delta_time):
        self.update_timer(delta_time)
        self.update_score()
