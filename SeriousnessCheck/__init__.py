from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'SeriousnessCheck'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    effort = models.IntegerField(
        choices=[
            [1, 'fast keine'],
            [2, 'sehr wenig'],
            [3, 'etwas'],
            [4, 'ziemlich viel'],
            [5, 'sehr viel'],
        ],
        widget=widgets.RadioSelect
    )
    attention = models.IntegerField(
        choices=[
            [1, 'fast keine'],
            [2, 'sehr wenig meiner'],
            [3, 'etwas meiner'],
            [4, 'die meiste meiner'],
            [5, 'meine volle'],
        ],
        widget=widgets.RadioSelect
    )
    use_data = models.BooleanField(
        choices=[
            [True, 'Ja'],
            [False, 'Nein'],
        ]
    )
    comments = models.LongStringField(
        label = '',
        blank = True
    )
    study_completed = models.BooleanField()


# PAGES

class SeriousnessCheck(Page):
    form_model = 'player'
    form_fields = ['effort','attention','use_data']

    def before_next_page(player, timeout_happened):
        player.study_completed = True

        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        with open('LabIds/CountParticipation.txt', 'r') as file:
            txt = int(file.read())
            print(txt)
            txt += 1
            print(txt)
        if(player.participant.label != "1234555"):
            if player.use_data:
                with open('LabIds/CountParticipation.txt', 'w') as file:
                    file.write(str(txt))

class Debriefing(Page):
    form_model = 'player'
    form_fields = ['comments']

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

class Finish(Page):
    pass



page_sequence = [
    SeriousnessCheck,
    Debriefing,
    Finish
]
