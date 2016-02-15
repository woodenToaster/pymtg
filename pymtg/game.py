import pygame

from card import Deck, HandSurface
from colors import COLORS


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


def init_game(p1, p1_deck, p2, p2_deck):
    deck1 = Deck(p1_deck)
    deck2 = Deck(p2_deck)

    player_1 = Player(deck1, p1)
    player_2 = Player(deck2, p2)
    player_1.deck.shuffle()
    player_2.deck.shuffle()

    return Game(player_1, player_2)


def init_display(width, height):
    display_size = display_width, display_height = (width, height)
    screen = pygame.display.set_mode(display_size)
    screen.fill(COLORS['black'])

    return screen

if __name__ == '__main__':

    game = init_game('Chris', 'white_weenie', 'Joe', 'white_weenie')

    pygame.init()
    screen = init_display(1600, 900)
    hand_surface = HandSurface(screen.get_width(), screen.get_height())
    large_card_surface = pygame.Surface(
        (hand_surface.card_width * 3, hand_surface.card_height * 3)
    )
    large_card_dest = pygame.Rect(
        ((screen.get_width() // 2) - ((hand_surface.card_width * 3) // 2), 0),
        (large_card_surface.get_width(), large_card_surface.get_height())
    )

    game.start_game()

    hand_surface.init_images(game.player_1.hand)
    for img, dest in hand_surface.card_img_data:
        screen.blit(img, dest)
    pygame.display.flip()

    running = True
    while running:
        dirty = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        for i in range(len(hand_surface.card_img_data)):
            img, dest = hand_surface.card_img_data[i]
            if hand_surface.mouse_is_over(i):
                print("Over card {}".format(i))
                pressed = pygame.mouse.get_pressed()
                if pressed[0] and pressed[2]:
                    pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3), large_card_surface)
                    screen.blit(large_card_surface, large_card_dest)
                    dirty.append(large_card_surface.get_rect(topleft=(large_card_dest.left, large_card_dest.top)))
                if not pressed[0] and not pressed[2]:
                    large_card_surface.fill((COLORS['black']))
                    screen.blit(large_card_surface, large_card_dest)
                    dirty.append(large_card_surface.get_rect(topleft=(large_card_dest.left, large_card_dest.top)))
        if dirty:
            pygame.display.update(dirty)
        pygame.time.wait(50)
    pygame.quit()
