from otree.api import *
import csv
import random
import math


class C(BaseConstants):
    NAME_IN_URL = 'Instructions'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class Instructions(Page):
    def vars_for_template(player):
        num_columns = player.session.config['slider_columns']
        column_width = math.floor(100 / num_columns)
        return {
            'column_width': column_width
        }

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


page_sequence = [
    Instructions
]
