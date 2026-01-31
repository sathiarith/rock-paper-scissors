import sys

import arcade
import arcade.gui
from computer import Computer
from arcade.gui import UIAnchorLayout, UITextureButton, UIBoxLayout, UILabel

# Preload files
# Graphics
blue_rect_button_default = arcade.load_texture("Graphics/Button/Rect-Medium/Default.png")
blue_rect_button_hover = arcade.load_texture("Graphics/Button/Rect-Medium/Hover.png")
blue_sq_button_default = arcade.load_texture("Graphics/Button/Square-Medium/Default.png")
blue_sq_button_hover = arcade.load_texture("Graphics/Button/Square-Medium/Hover.png")

title_img = arcade.load_texture("Graphics/Objects/Title.jpg")
rules_img = arcade.load_texture("Graphics/Objects/rps_rules_modified.png")
enemy_img = arcade.load_texture("Graphics/Objects/robot_profile.png")

comp_speech = arcade.load_texture("Graphics/Objects/orange_speech_right.png")
player_speech = arcade.load_texture("Graphics/Objects/orange_speech_left.png")

# Sound
button_sound = arcade.load_sound("Sounds/button-bling.wav")
music = arcade.load_sound("Sounds/tam-xa-mai-start-background.mp3")

class Start(arcade.View):
    """
        Title and start menu to store player name and begin gameplay.

        Attributes:
            attribute_name (type): Description of what it stores.
            another_attribute (type): Another description.
    """

    def __init__(self):
        super().__init__()

        # Setup ui manager
        self.ui = arcade.gui.UIManager()
        self.player_id = "Player"

        play_music = arcade.play_sound(music, loop=True)

        # Create an anchor layout, which can be used to position widgets on screen
        # Note: arcade widgets use the center of screen, therefore uses x and y offsets and not cords
        # Arcade window sets cord x=0, y=0 at the bottom left of window
        input_anchor = self.ui.add(UIAnchorLayout(x=0,y=0))
        start_game_anchor = self.ui.add(UIAnchorLayout(x=0,y=-100))
        enemy_anchor = self.ui.add(UIAnchorLayout(x=245,y=-265))

        # Title
        self.title_sprite = arcade.Sprite(title_img, center_x=400.0, center_y=470.0, scale=0.1)
        self.title_sprite.width = 800

        # Rules Overlay
        self.rules_sprite = arcade.Sprite(rules_img, center_x=150.0, center_y=130.0, scale=0.4)

        # Opponent Introduction
        self.enemy_sprite = arcade.Sprite(enemy_img, center_x=650.0, center_y=150.0, scale=0.75)
        enemy_anchor.add(UILabel(text="Opponent", font_name=("Arial",), font_size=24, bold=True))

        # Get player's name
        row_username = input_anchor.add(UIBoxLayout(align = "left", vertical=True, size_hint=(0, 0)))
        row_username.add(UILabel(text="Player Name: ", font_name=("Arial",), font_size= 24, bold=True))
        p_input = arcade.gui.UIInputText(
                width=400,
                height=40,
                font_name=('Arial',),
                font_size=24,
                border_color=arcade.uicolor.WHITE,
                border_width=2,
            )
        row_username.add(p_input)

        start_game_anchor.add(UIBoxLayout(align="center",vertical=False,size_hint=(0, 0)))
        start_button = UITextureButton(
                text="Start Game",
                texture=blue_rect_button_default,
                texture_pressed=blue_rect_button_default,
                texture_hovered=blue_rect_button_hover,
                size_hint=(.2, .1),
            )
        start_game_anchor.add(start_button)

        @p_input.event("on_change")
        def _(event):
            self.player_id = p_input.text

        @start_button.event("on_click")
        def _(event):
            arcade.play_sound(button_sound)
            self.window.show_view(Play(self.player_id))
            play_music.pause()


    def on_show_view(self) -> None:
        self.ui.enable()

    def on_hide_view(self) -> None:
        self.ui.disable()

    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.DARK_PASTEL_BLUE)
        self.ui.draw()
        arcade.draw_sprite(self.title_sprite)
        arcade.draw_sprite(self.rules_sprite)
        arcade.draw_sprite(self.enemy_sprite)




class Play(arcade.View):
    """
        Interface for play to select hand sign and play against computer.
        A scoreboard tracks play history.

        Attributes:
            attribute_name (type): Description of what it stores.
            another_attribute (type): Another description.
    """
    def __init__(self, player_id: str) -> None:
        super().__init__()
        self.p_id = player_id
        self.ui = arcade.gui.UIManager()
        self.computer = Computer()
        self.player_wins = 0
        self.comp_wins = 0
        self.hand_choices = {"player": "none", "computer": "none"}
        self.player_speech_anchor = None
        self.player_speech = None
        self.enemy_speech_anchor = None
        self.enemy_speech = None

        # Anchors layout
        score_anchor = self.ui.add(UIAnchorLayout(x=-250, y=250))
        enemy_anchor = self.ui.add(UIAnchorLayout(x=280, y=70))
        select_buttons_anchor = self.ui.add(UIAnchorLayout(x=40, y=-180))

        # Enemy sprite placement
        self.enemy_sprite = arcade.Sprite(enemy_img, center_x=680.0, center_y=490.0, scale=0.75)
        enemy_anchor.add(UILabel(text="Opponent", font_name=("Arial",), font_size=24, bold=True))

        # Create score board
        score_box = score_anchor.add(UIBoxLayout(align="left", vertical=True, size_hint=(0, 0)))

        self.p_wins = UILabel(
            text=f"{self.p_id} Wins: {self.player_wins}",
            font_name=("Arial",),
            font_size=24,
            bold=True,
        )

        self.c_wins = UILabel(
            text=f"Computer Wins: {self.comp_wins}",
            font_name=("Arial",),
            font_size=24,
            bold=True,
        )

        score_box.add(self.p_wins)
        score_box.add(self.c_wins)

        # Create buttons for rock, paper, and scissors
        # Buttons have an image each

        rock_img = arcade.gui.UIImage(
            texture = arcade.load_texture("Graphics/Objects/rock.png"),
            size_hint=(.4, .7),
        )
        self.rock_button = UITextureButton(
            texture = blue_sq_button_default,
            texture_pressed = blue_sq_button_default,
            texture_hovered = blue_sq_button_hover,
            size_hint=(.3, .2),
        )
        self.rock_button.add(rock_img)

        paper_img = arcade.gui.UIImage(
            texture = arcade.load_texture("Graphics/Objects/paper.png"),
            size_hint=(.4, .7),
        )
        self.paper_button = UITextureButton(
            texture = blue_sq_button_default,
            texture_pressed = blue_sq_button_default,
            texture_hovered = blue_sq_button_hover,
            size_hint = (.3, .2),
        )
        self.paper_button.add(paper_img)

        scissors_img = arcade.gui.UIImage(
            texture = arcade.load_texture("Graphics/Objects/scissors.png"),
            size_hint=(.4, .7),
        )
        self.scissors_button = UITextureButton(
            texture = blue_sq_button_default,
            texture_pressed = blue_sq_button_default,
            texture_hovered = blue_sq_button_hover,
            size_hint = (.3, .2),
        )
        self.scissors_button.add(scissors_img)

        # UI Box layout
        buttons_layout = UIBoxLayout(
            align = "center",
            vertical = False,
            size_hint = (1, 1),
            space_between = 10,
        )

        # Anchor organizes all buttons
        buttons_layout.add(self.rock_button)
        buttons_layout.add(self.paper_button)
        buttons_layout.add(self.scissors_button)

        select_buttons_anchor.add(buttons_layout)

        quit_anchor = self.ui.add(UIAnchorLayout(x=280, y=-270))
        quit_button = UITextureButton(
            texture=blue_sq_button_default,
            texture_pressed=blue_sq_button_default,
            texture_hovered=blue_sq_button_hover,
            size_hint=(.2, .067),
        )

        text = UILabel(
            text="QUIT",
            font_name=("Arial",),
            text_color=arcade.color.BLACK,
        )

        quit_button.add(text)
        quit_anchor.add(quit_button)

        @self.rock_button.event("on_click")
        def _(event):
            arcade.play_sound(button_sound)
            self.hand_choices["player"] = "rock"
            self.play_round("rock")
            print("comp: " + str(self.hand_choices["computer"]) + " player: " + str(self.hand_choices["player"]))
            if self.hand_choices["computer"] in ["rock", "paper", "scissors"]:
                self.player_response("rock", reveal_choice=True)
            else:
                self.player_response("rock", reveal_choice=False)

            # reset responses
            for key in self.hand_choices:
                self.hand_choices[key] = "none"

        @self.paper_button.event("on_click")
        def _(event):
            arcade.play_sound(button_sound)
            self.hand_choices["player"] = "paper"
            self.play_round("paper")
            if self.hand_choices["computer"] in ["rock", "paper", "scissors"]:
                self.player_response("paper", reveal_choice=True)
            else:
                self.player_response("paper", reveal_choice=False)

            # reset responses
            for key in self.hand_choices:
                self.hand_choices[key] = "none"

        @self.scissors_button.event("on_click")
        def _(event):
            arcade.play_sound(button_sound)
            self.hand_choices["player"] = "scissors"
            self.play_round("scissors")
            if self.hand_choices["computer"] in ["rock", "paper", "scissors"]:
                self.player_response("scissors", reveal_choice=True)
            else:
                self.player_response("scissors", reveal_choice=False)

            # reset responses
            for key in self.hand_choices:
                self.hand_choices[key] = "none"

        @quit_button.event("on_click")
        def _(event):
            self.window.close()



    def on_show_view(self) -> None:
        self.ui.enable()

    def on_hide_view(self) -> None:
        self.ui.disable()

    def on_draw(self):
        self.clear()

        # Set up GUI
        self.ui.draw()
        arcade.draw_sprite(self.enemy_sprite)
        self.p_wins.text = f"{self.p_id} Wins: {self.player_wins}"
        self.c_wins.text = f"Computer Wins: {self.comp_wins}"


    def player_response(self,  choice: str, reveal_choice: bool) -> None:
        message = "..."
        if reveal_choice:
            message = choice

        if self.player_speech_anchor:
            self.ui.remove(self.player_speech_anchor)
            self.player_speech_anchor = None

        self.player_speech_anchor = self.ui.add(UIAnchorLayout(x=-245, y=-10))

        # Create speech/choice bubbles
        self.player_speech = UITextureButton(
            texture=player_speech,
            size_hint=(.3, .3),
        )
        player_speech_text = UILabel(
            text=message,
            font_name=("Arial",),
            font_size=24,
            bold=True,
        )

        self.player_speech.add(player_speech_text)
        self.player_speech_anchor.add(self.player_speech)

    def computer_response(self, choice: str, reveal_choice: bool) -> None:
        message = "..."
        if reveal_choice:
            message = choice

        if self.enemy_speech_anchor:
            self.ui.remove(self.enemy_speech_anchor)
            self.enemy_speech_anchor = None

        self.enemy_speech_anchor = self.ui.add(UIAnchorLayout(x=60, y=190))

        # Create speech/choice bubbles
        self.enemy_speech = UITextureButton(
            texture = comp_speech,
            size_hint=(.3, .3),
        )
        enemy_speech_text = UILabel(
            text=message,
            font_name=("Arial",),
            font_size=24,
            bold=True,
        )

        self.enemy_speech.add(enemy_speech_text)
        self.enemy_speech_anchor.add(self.enemy_speech)

    @staticmethod
    def decide_winner(p_choice: str, c_choice: str)-> str:
        # Each key, key beats index 0 and loses to index 1
        win_loss_dict = {
            "rock": ["scissors", "paper"],
            "paper": ["rock", "scissors"],
            "scissors": ["paper", "rock"]
        }
        # Case of clear winner
        if c_choice in win_loss_dict[p_choice]:
            # computer loses
            if c_choice == win_loss_dict[p_choice][0]:
                return "player"
            else:
                return "computer"
        return "tie"

    def play_round(self, p_choice) -> None:
        # Player and Computer win tally
        # Computer decides based on algorithm
        self.hand_choices["computer"] = self.computer.play()
        self.hand_choices["player"] = p_choice # error: comp doesnt decide player
        player_ready = self.hand_choices["player"] != "none"
        self.computer_response(self.hand_choices["computer"], player_ready)
        winner = "none"
        if self.hand_choices["player"] != "none" and self.hand_choices["computer"] != "none":
            winner = self.decide_winner(self.hand_choices["player"], self.hand_choices["computer"])
        print(self.hand_choices)
        if winner != "none":
            print(winner)

            # Update scoreboard
            if winner == "player":
                self.player_wins += 1
            elif winner == "computer":
                self.comp_wins += 1

            # Troubleshoot, scoreboard does not update function pw and cw tracker
            print(f"pw: {self.player_wins}")
            print(f"cw: {self.comp_wins}")


            # Tally up score board and computer records
            print("computer records")
            self.computer.total_games += 1
            if self.hand_choices["player"] == "rock":
                self.computer.opponent_rock_picks += 1
            elif self.hand_choices["player"] == "paper":
                self.computer.opponent_paper_picks += 1
            else: # "scissors" choice
                self.computer.opponent_scissors_picks += 1





