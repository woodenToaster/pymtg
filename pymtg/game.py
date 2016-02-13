import pygame

from card import Deck

from os.path import join as jp


class Player():
    def __init__(self, deck, name):
        self.deck = deck
        self.name = name
        self.life = 20
        self.active = False
        self.hand = []

    def draw_card(self):
        self.hand.append(self.deck.draw())


class Game():
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

    player_indicator_fmt = "Player[{}]      Phase[{}]       Life[{}]"

    def __init__(self, player1, player2):
        self.player_1 = player1
        self.player_2 = player2
        self.current_phase = 1
        self.active_player = 1
        self.starting_hand_size = 7

    def next_phase(self):
        self.current_phase += 1
        self.current_phase %= 9

        if self.current_phase == 0:
            if self.active_player == self.player_1:
                self.active_player = self.player_2
            else:
                self.active_player = self.player_1

    def start_game(self):
        for i in range(self.starting_hand_size):
            self.player_1.draw_card()
            self.player_2.draw_card()

        # while True:
        #     print(Game.player_indicator_fmt.format(
        #         self.active_player.name, Game.phases[self.current_phase], self.active_player.life)
        #     )

        #     if Game.phases[self.current_phase] == 'upkeep':
        #         pass

        #     elif Game.phases[self.current_phase] == 'draw':
        #         self.active_player.draw_card()
        #         print("{} drew \n{}".format(
        #             self.active_player.name, self.active_player.hand[len(self.active_player.hand) - 1])
        #         )

BLACK = (0, 0, 0)
MAGENTA = (255, 0, 255)

if __name__ == '__main__':
    deck1 = Deck('white_weenie')
    deck2 = Deck('white_weenie')

    player_1 = Player(deck1, 'Chris')
    player_2 = Player(deck2, 'Joe')
    player_1.deck.shuffle()
    player_2.deck.shuffle()

    game = Game(player_1, player_2)

    img_path = 'data/img/origins/cards/Cards'
    anointer = 'anointer_of_champions'
    img_ext = '.jpg'

    pygame.init()
    display_size = display_width, display_height = (1600, 900)
    screen = pygame.display.set_mode(display_size)
    screen.fill(BLACK)
    running = True

    hand_surface_width = 0.7 * display_width
    card_width_in_hand = int(hand_surface_width / 7)

    hand_surface_height = 0.2 * display_height
    card_height_in_hand = int(hand_surface_height)

    hand_surface = pygame.Surface((hand_surface_width, hand_surface_height))
    hand_surface.fill(MAGENTA)

    hand_surface_location = (
        (display_width - hand_surface_width) / 2.0,
        display_height - hand_surface_height
    )
    screen.blit(hand_surface, hand_surface_location)

    anointer_img = pygame.image.load(jp(img_path, anointer + img_ext)).convert()
    anointer_img = pygame.transform.scale(
        anointer_img, (card_width_in_hand, card_height_in_hand)
    )

    for i in range(7):
        screen.blit(
            anointer_img,
            (hand_surface_location[0] + i * card_width_in_hand, hand_surface_location[1])
        )

    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
