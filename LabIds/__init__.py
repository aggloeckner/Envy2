from otree.api import *
from string import digits


class Constants(BaseConstants):
    name_in_url = 'LabIds'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    DecisionLabId = models.CharField( max_length = 7 )


# PAGES
class IdPage(Page):
    form_model = 'player'
    form_fields = ['DecisionLabId']

    @staticmethod
    def vars_for_template(player):
        pdone = round(player.participant._index_in_pages / player.participant._max_page_index * 100)

        return {"pdone": pdone}

    @staticmethod
    def error_message(player, values):
        # Only digits
        if any([c not in digits for c in values['DecisionLabId']]):
            return "Bitte nur Ziffern eingeben!"

        # Exactly 7 digits
        if len(values['DecisionLabId']) < 7:
            return "Eingabe zu kurz! Die Decision Lab Id sollte genau sieben Stellen haben!"

        # Last two digits are the sum of all other digits
        sm = sum([int(c) * (i + 1) for i, c in enumerate(values['DecisionLabId'][0:5])]) % 100
        if not sm == int(values['DecisionLabId'][5:]):
            return "Fehlerhafte Decision Lab ID!"

        if values['DecisionLabId'] == "0000000":
            return "Fehlerhafe Decision Lab ID!"

        # Already participated
        with open('LabIds/Participated.txt', 'r') as file:
            txt = file.read()
        if(values['DecisionLabId'] in txt and values['DecisionLabId'] != "1234555"):
            return "An dieser Studie haben Sie bereits teilgenommen!"

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.vars["DecisionLabId"] = player.DecisionLabId
        player.participant.label = player.DecisionLabId

        import datetime
        player.participant.time_start = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


page_sequence = [IdPage]