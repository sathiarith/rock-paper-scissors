import arcade
import arcade.gui
from computer import Computer
from arcade.gui import UIAnchorLayout, UITextureButton, UIBoxLayout, UILabel, UIOnClickEvent, UIOnChangeEvent

# Preload files
blue_rect_button_default = arcade.load_texture("Graphics/Button/Rect-Medium/Default.png")
blue_rect_button_hover = arcade.load_texture("Graphics/Button/Rect-Medium/Hover.png")
title_img = arcade.load_texture("Graphics/Objects/Title.jpg")
rules_img = arcade.load_texture("Graphics/Objects/rps_rules_modified.png")
enemy_img = arcade.load_texture("Graphics/Objects/robot_profile.png")

button_sound = arcade.load_sound("Sounds/button-bling.wav")

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
        self.player_id = ""

        music = arcade.load_sound("Sounds/tam-xa-mai-start-background.mp3")
        play_music = arcade.play_sound(music, loop=True)

        # Create an anchor layout, which can be used to position widgets on screen
        title_anchor = self.ui.add(UIAnchorLayout(x=0,y=150))
        input_anchor = self.ui.add(UIAnchorLayout())
        start_game_anchor = self.ui.add(UIAnchorLayout(x=0,y=-(100)))
        enemy_anchor = self.ui.add(UIAnchorLayout(x=245,y=-(265)))

        # Title
        row_title = title_anchor.add(UIBoxLayout(align="center",vertical=False,size_hint=(0,0)))
        row_title.add(UILabel(text="Rock Paper Scissors", font_name="Arial", font_size=32, bold=True))
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
            print(self.player_id)

        @start_button.event("on_click")
        def _(event):
            arcade.play_sound(button_sound)
            self.window.show_view(Play())
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
        Short one-sentence summary of what the class represents.

        Longer explanation if necessary. Focus on **purpose**, not code details.

        Attributes:
            attribute_name (type): Description of what it stores.
            another_attribute (type): Another description.
    """
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()

        # select hand from click interface

class Results(arcade.View):
    """
        Short one-sentence summary of what the class represents.

        Longer explanation if necessary. Focus on **purpose**, not code details.

        Attributes:
            attribute_name (type): Description of what it stores.
            another_attribute (type): Another description.
    """
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()