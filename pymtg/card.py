import json

import pygame

from enum import Enum
from os.path import join as jp
from random import shuffle

from colors import COLORS


class Drawable():
    def __init__(self, surf=None, dest=None):
        self.x = dest.x if dest else 0
        self.y = dest.y if dest else 0
        self.topleft = (self.x, self.y)
        self.surf = surf if surf else pygame.Surface((0, 0))
        self.width = self.surf.get_width()
        self.height = self.surf.get_height()
        self.dest = pygame.Rect(self.x, self.y, self.width, self.height)

    def set_surf(self, surf):
        self.surf = surf
        self.width = surf.get_width()
        self.height = surf.get_height()

    def set_dest(self, dest):
        self.x = dest.x
        self.y = dest.y
        self.topleft = (dest.x, dest.y)
        self.dest = dest

    def render(self, dest):
        dest.blit(self.surf, self.dest)


class Deck():
    def __init__(self, deck_file):
        with open('data/origins.json', 'r') as f:
            card_data = json.load(f)
        with open(jp('data', 'decks', deck_file + '.json'), 'r') as f:
            deck_data = json.load(f)

        cards = []

        for card_name, num in deck_data['cards'].items():
            for card in card_data['cards']:
                if card['name'] == card_name:
                    if 'Creature' in card['types']:
                        for i in range(num):
                            cards.append(
                                CreatureCard(
                                    card.get('name'), card.get('types'),
                                    card.get('colors'), card.get('manaCost'),
                                    card.get('power'), card.get('toughness'),
                                    card.get('text'), card.get('cmc')
                                )
                            )
                    else:
                        for i in range(num):
                            cards.append(
                                Card(
                                    card.get('name'), card.get('types'),
                                    card.get('colors'), card.get('manaCost'),
                                    card.get('text'), card.get('cmc')
                                )
                            )

        self.cards = cards
        self.size = len(cards)

    def shuffle(self):
        shuffle(self.cards)

    def draw(self):
        return self.cards.pop(0)


class Card(Drawable):
    def __init__(self, name, card_type, colors, mana_cost, text, cmc):
        super().__init__()
        self.name = name
        self.card_type = card_type
        self.colors = colors
        self.mana_cost = mana_cost
        self.text = text
        self.cmc = cmc

        self.is_tapped = False

        def tap(self):
            self.is_tapped = True

        def untap(self):
            self.is_tapped = False

    def __str__(self):
        fmt = "{!s:15}{!s}\n"
        ret_string = ""
        ret_string += fmt.format('Name:', self.name)
        ret_string += fmt.format('Card Type:', self.card_type)
        ret_string += fmt.format('Colors:', self.colors)
        ret_string += fmt.format('Mana Cost:', self.mana_cost)
        ret_string += fmt.format('Rules Text:', self.text)
        ret_string += fmt.format('CMC:', self.cmc)

        return ret_string


class CreatureCard(Card):
    def __init__(
        self, name, card_type, colors, mana_cost, power, toughness, text, cmc
    ):
        super().__init__(name, card_type, colors, mana_cost, text, cmc)
        self.power = power
        self.toughness = toughness

    def __str__(self):
        fmt = "{!s:15}{!s}\n"
        ret_string = super().__str__()
        ret_string += fmt.format('Power:', self.power)
        ret_string += fmt.format('Toughness:', self.toughness)

        return ret_string


class HandSurface():
    img_path = 'data/img/origins/cards/Cards'
    img_ext = '.jpg'

    def __init__(self, screen_width, screen_height):
        self.width = 0.7 * screen_width
        self.height = 0.25 * screen_height
        self.card_width = int(self.width / 7)
        self.card_height = int(self.card_width * 1.4)

        self.hand_surface = pygame.Surface((self.width, self.height))
        self.hand_surface.fill(COLORS['magenta'])

        self.hand_surface_location = (
            (screen_width - self.width) / 2.0,
            screen_height - self.height
        )

        self.card_img_data = []

    def init_images(self, hand):
        i = 0
        for card in hand:
            img_name = card.name.lower().replace(' ', '_').replace("'", '')
            img_path = jp(HandSurface.img_path, img_name + HandSurface.img_ext)
            img = pygame.image.load(img_path).convert()
            img = pygame.transform.scale(
                img, (self.card_width, self.card_height)
            )
            self.card_img_data.append(
                (img,
                 (self.hand_surface_location[0] + i * self.card_width,
                  self.hand_surface_location[1]))
            )
            i += 1

    def mouse_is_over(self, card_num):
        x = self.hand_surface_location[0] + card_num * self.card_width
        y = self.hand_surface_location[1]
        rect = self.card_img_data[card_num][0].get_rect(topleft=(x, y))
        if rect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False


class CardTypes(Enum):
    CREATURE = 1
    BASIC_LAND = 2
    LAND = 3
    INSTANT = 4
    SORCERY = 5
    ARTIFACT = 6
