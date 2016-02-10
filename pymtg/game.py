from card import Deck


class Player():
    def __init__(self, deck, name):
        self.deck = deck
        self.name = name
        self.life = 20
        self.active = False
        self.hand = []

    def draw_card(self):
        self.hand.append(self.deck.draw())

if __name__ == '__main__':
    phases = {
        1: 'upkeep',
        2: 'draw',
        3: 'main1',
        4: 'attack',
        5: 'block',
        6: 'damage',
        7: 'end_combat',
        8: 'main2',
        0: 'end'
    }

    deck1 = Deck('white_weenie')
    deck2 = Deck('white_weenie')

    player_1 = Player(deck1, 'Chris')
    player_2 = Player(deck2, 'Joe')
    player_1.deck.shuffle()
    player_2.deck.shuffle()

    player_indicator_fmt = "Player[{}]      Phase[{}]       Life[{}]"

    active_player = player_1
    current_phase = 0

    # Main game loop
    while True:
        current_phase += 1
        current_phase %= 9

        print(player_indicator_fmt.format(
            active_player.name, phases[current_phase], active_player.life)
        )

        if phases[current_phase] == 'upkeep':
            pass

        elif phases[current_phase] == 'draw':
            # Draw phase
            active_player.draw_card()
            print("{} drew \n{}".format(
                active_player.name, active_player.hand[len(active_player.hand) - 1])
            )

        pass_priority = input()

        if current_phase == 0:
            if active_player == player_1:
                active_player = player_2
            else:
                active_player = player_1
