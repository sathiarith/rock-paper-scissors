import random as rnd


class Computer:
    """
        The Computer is responsible for tracking the player's history
        to help determine what hand to play.

        Attributes:
            play_style(int) : 0 (random) or 1 (procedural) for selecting hands
            total_games(int) : Total number of games
            opponent_rock_picks(int) : Number of rock picks
            opponent_paper_picks(int) : Number of paper picks
            opponent_scissors_picks(int) : Number of scissors picks
    """
    def __init__(self):
        self.play_style = 0
        self.total_games = 0
        self.opponent_rock_picks = 0
        self.opponent_paper_picks = 0
        self.opponent_scissors_picks = 0

    def play(self) -> str:
        # play style defaults to random if first game
        if self.play_style == 0 or self.total_games == 0:
            return rnd.choice(['rock', 'paper', 'scissors'])
        else:
            # probability of opponent picking choice
            rock = self.opponent_rock_picks / self.total_games
            paper = self.opponent_paper_picks / self.total_games
            scissors = self.opponent_scissors_picks / self.total_games

            # shift weights to beat opponent
            # bias for rock -> computer assign bias to paper
            # paper -> scissors
            # scissors -> rock
            return rnd.choices(['rock', 'paper', 'scissors'],
                               [scissors, rock, paper], k=1)[0]
