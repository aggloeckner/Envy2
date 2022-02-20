from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'Consent'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consentGiven = models.BooleanField(
        widget = widgets.CheckboxInput,
        blank = True
    )


# PAGES
class InformedConsent(Page):
    form_model = 'player'
    form_fields = ['consentGiven']

    @staticmethod
    def error_message(player, values):
        print('value is', values['consentGiven'])
        if values['consentGiven'] == False:
            return 'Um fortfahren zu können, müssen Sie Ihre Zustimmung geben.'


page_sequence = [
    InformedConsent
]
