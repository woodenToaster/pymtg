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

    def next_phase(self):
        self.current_phase += 1
        self.current_phase %= 9

        if self.current_phase == 0:
            if self.active_player == self.player_1:
                self.active_player = self.player_2
            else:
                self.active_player = self.player_1

    def start_game(self):
        # Main game loop
        while True:
            print(Game.player_indicator_fmt.format(
                self.active_player.name, Game.phases[self.current_phase], self.active_player.life)
            )

            if Game.phases[self.current_phase] == 'upkeep':
                pass

            elif Game.phases[self.current_phase] == 'draw':
                self.active_player.draw_card()
                print("{} drew \n{}".format(
                    self.active_player.name, self.active_player.hand[len(self.active_player.hand) - 1])
                )


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
    size = width, height = (1600, 900)
    black = (0, 0, 0)
    screen = pygame.display.set_mode(size)
    screen.fill(black)
    running = True

    anointer_img = pygame.image.load(jp(img_path, anointer + img_ext)).convert()
    anointer_img = pygame.transform.scale(anointer_img, (120, 200))
    anointer_rect = anointer_img.get_rect()

    screen.blit(anointer_img, anointer_rect)
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
