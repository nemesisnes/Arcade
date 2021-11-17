import arcade

class GameOverView(arcade.View):
    def __init__(self):
        # View to show when game is over
        super().__init__()
    def on_draw(self):
        # Draw this view
        arcade.start_render()
        line_height = 70
        line_location = self.window.height - line_height * 2
        arcade.draw_text("Game Over",
                         self.window.width / 2,
                         line_location,
                         arcade.color.WHITE,
                         font_size=50,
                         anchor_x="center",
                         font_name="SF Atarian System")
        line_location -= line_height
        line_location -= line_height
        line_height = 40
        arcade.draw_text("Start a new game of Space Defense Force?",
                         self.window.width / 2,
                         line_location,
                         arcade.color.WHITE,
                         font_size=30,
                         anchor_x="center",
                         font_name="SF Atarian System")
        line_location -= line_height
        line_location -= line_height
        arcade.draw_text("1 - Start One Player Game",
                         self.window.width / 2,
                         line_location,
                         arcade.color.WHITE,
                         font_size=20,
                         anchor_x="center",
                         font_name="SF Atarian System")
        color = arcade.color.GRAY
        line_location -= line_height
        arcade.draw_text("2 - Start Two Player Game",
                         self.window.width / 2,
                         line_location,
                         color,
                         font_size=20,
                         anchor_x="center",
                         font_name="SF Atarian System")
        line_location -= line_height
        line_location -= line_height
        color = arcade.color.WHITE
        arcade.draw_text("Use joysticks to play, or arrow keys to move and number keys to fire.",
                         self.window.width / 2,
                         line_location,
                         color,
                         font_size=20,
                         anchor_x="center",
                         font_name="SF Atarian System")

    def on_key_press(self, symbol: int, modifiers: int):
        from game_view import GameView
        if symbol == arcade.key.KEY_1:
            game_view = GameView()
            game_view.start_new_game(1)
            self.window.show_view(game_view)
        elif symbol == arcade.key.KEY_2:
            game_view = GameView()
            game_view.start_new_game(2)
            self.window.show_view(game_view)
        
    def update(self, delta_time):
        self.game_over = True
