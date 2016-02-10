import json

from enum import Enum
from os.path import join as jp
from random import shuffle


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


class Card():
    def __init__(self, name, card_type, colors, mana_cost, text, cmc):
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


class CardTypes(Enum):
    CREATURE = 1
    BASIC_LAND = 2
    LAND = 3
    INSTANT = 4
    SORCERY = 5
    ARTIFACT = 6
