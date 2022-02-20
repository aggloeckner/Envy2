from otree.api import *
import csv
import random
import math

class C(BaseConstants):
    NAME_IN_URL = 'Interaction'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    benign_option = models.BooleanField()


class Player(BasePlayer):
    solvedSliders = models.IntegerField()
    winner = models.BooleanField()
    benignity = models.IntegerField(min = 0, max = 250)
    maliciousness = models.CurrencyField(min = 0, max = 2.5)
    expected_benignity = models.IntegerField(min = 0, max = 250)
    expected_maliciousness = models.CurrencyField(min = 0, max = 2.5)
    benignity_attractiveness = models.FloatField(min = 0, max = 100)
    maliciousness_attractiveness = models.FloatField(min = 0, max = 100)
    repay = models.CurrencyField(min = 0, max = 5)
    pade_scale_1 = models.IntegerField(widget=widgets.RadioSelect, choices=[1, 2, 3, 4, 5, 6, 7], label="Ich will mich bei jemand anderem über Spieler/in B beschweren.")
    pade_scale_2 = models.IntegerField(widget=widgets.RadioSelect, choices=[1, 2, 3, 4, 5, 6, 7], label="Ich fühle mich deprimiert.")
    pade_scale_3 = models.IntegerField(widget=widgets.RadioSelect, choices=[1, 2, 3, 4, 5, 6, 7], label="Ich will härter arbeiten, um auch genau 5€ zu erreichen.")
    pade_scale_4 = models.IntegerField(widget=widgets.RadioSelect, choices=[1, 2, 3, 4, 5, 6, 7], label="Ich leide.")
    pade_scale_5 = models.IntegerField(widget=widgets.RadioSelect, choices=[1, 2, 3, 4, 5, 6, 7], label="Ich fühle Hass.")
    pade_scale_6 = models.IntegerField(widget=widgets.RadioSelect, choices=[1, 2, 3, 4, 5, 6, 7], label="Ich habe feindselige Gefühle gegenüber Spieler/in B.")
    pade_scale_7 = models.IntegerField(widget=widgets.RadioSelect, choices=[1, 2, 3, 4, 5, 6, 7], label="Spieler/in B motiviert mich dazu, genauso wie sie zu werden.")
    pade_scale_8 = models.IntegerField(widget=widgets.RadioSelect, choices=[1, 2, 3, 4, 5, 6, 7], label="Ich will mir einen Plan ausdenken, um ebenfalls 5€ zu bekommen.")
    pade_scale_9 = models.IntegerField(widget=widgets.RadioSelect, choices=[1, 2, 3, 4, 5, 6, 7], label="Ich fühle ein sehnsüchtiges Verlangen ebenfalls 5€ zu bekommen.")
    pade_scale_10 = models.IntegerField(widget=widgets.RadioSelect, choices=[1, 2, 3, 4, 5, 6, 7], label="Ich wünsche mir heimlich, dass Spieler/in B seine 5€ verliert.")
    pade_scale_11 = models.IntegerField(widget=widgets.RadioSelect, choices=[1, 2, 3, 4, 5, 6, 7], label="Ich fühle mich unzulänglich.")
    additionalSlidersStart_A = models.IntegerField()
    additionalSlidersEnd_A = models.IntegerField()
    slider_rating = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[
            [1, "Gar nicht anstrengend"],
            [2, ""],
            [3, ""],
            [4, ""],
            [5, "Sehr anstrengend"]
        ],
        label="Bitte geben Sie im Folgenden an, wie anstrengend Sie die Aufgabe empfunden haben.")
    svo_choices_B = models.CharField()
    svo_tot_ego_B = models.IntegerField()
    svo_tot_alter_B = models.IntegerField()
    svo_mean_ego_B = models.FloatField()
    svo_mean_alter_B = models.FloatField()
    svo_ratio_B = models.FloatField()
    svo_angle_B = models.FloatField()

# DEFS

def group_by_arrival_time_method(player, waiting_players):
    if len(waiting_players) >= 2:
        p1 = waiting_players[0]
        p2 = waiting_players[1]

        with open("SVO_Example.csv") as f:
            r = csv.reader(f, delimiter=";")
            c = [line for line in r]
            h = c[0]
            d = [dict(zip(h, l)) for l in c[1:]]
            player.session.vars["SVO_Example"] = [
                [[l["A" + str(i + 1)], l["B" + str(i + 1)], i == int(l["C"])] for i in range(int(l["N"]))] for l in d]
        with open(player.session.config['svo_file']) as f:
            r = csv.reader(f, delimiter=";")
            c = [line for line in r]
            h = c[0]
            d = [dict(zip(h, l)) for l in c[1:]]
            player.session.vars["SVO_Full"] = [[[r, l["A" + str(i + 1)], l["B" + str(i + 1)]] for i in range(int(l["N"]))]
                                             for r, l in enumerate(d)]

        return [p1, p2]

def assign_roles(group):
    players = group.get_players()

    weights = [
        math.floor(players[0].solvedSliders/10),
        math.floor(players[1].solvedSliders/10)
    ]

    if players[0].solvedSliders < 10 and players[1].solvedSliders < 10:
        weights = [1,1]
        choice = random.choices([True, False], weights=weights, k=1)
    elif players[0].solvedSliders < 10:
        choice = [False]
    elif players[1].solvedSliders < 10:
        choice = [True]
    else:
        choice = random.choices([True, False], weights=weights, k=1)

    players[0].winner = choice[0]
    players[1].winner = not choice[0]

    for p in players:
        if p.winner:
            p.payoff = 5
        else:
            p.payoff = 2.5

# PAGES

class GroupingWaitPage(WaitPage):
    group_by_arrival_time = True

    def vars_for_template(player):
        return {'body_text': 'Sobald Ihnen eine andere Person zugeteilt wurde, geht es los.',
                'title_text': 'Bitte warten Sie.'}

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class PageBeforeTask(Page):
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

class SliderTask(Page):
    form_model = 'player'
    form_fields = ['solvedSliders']
    timeout_seconds = 12

    def vars_for_template(player):
        num_columns = player.session.config['slider_columns']
        column_width = math.floor(100 / num_columns)
        num_sliders = player.session.config['sliders_per_column']
        max_slider_offset = player.session.config['max_slider_offset']

        offsets = [[random.randint(0, max_slider_offset) for _ in range(num_sliders)] for _ in range(num_columns)]

        return {
            'num_columns': num_columns,
            'num_sliders': num_sliders,
            'offsets': offsets,
            'column_width': column_width}

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

class InstructionsWaitPage(WaitPage):
    after_all_players_arrive = 'assign_roles'

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

class InstructionsPlayerA(Page):
    form_model = 'player'
    form_fields = ['benignity','maliciousness']

    @staticmethod
    def is_displayed(player):
        return not player.winner

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

class AttractivenessRatingA(Page):
    form_model = 'player'
    form_fields = ['benignity_attractiveness','maliciousness_attractiveness']

    @staticmethod
    def is_displayed(player):
        return not player.winner

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

class PaDeScaleA(Page):
    form_model = 'player'
    pa_de_scale = ['pade_scale_1','pade_scale_2','pade_scale_3','pade_scale_4','pade_scale_5','pade_scale_6','pade_scale_7','pade_scale_8','pade_scale_9','pade_scale_10','pade_scale_11']
    random.shuffle(pa_de_scale)
    form_fields = pa_de_scale

    @staticmethod
    def is_displayed(player):
        return not player.winner

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.group.benign_option = random.choice([True,False])

        if not player.group.benign_option:
            player.get_others_in_group()[0].payoff -= player.maliciousness

        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

class RamdomDrawA(Page):
    @staticmethod
    def is_displayed(player):
        return not player.winner

    @staticmethod
    def vars_for_template(player):
        possible_benefit = cu(player.benignity / 10)
        number_sliders = player.benignity
        maliciousness = player.maliciousness
        results_player_b = player.get_others_in_group()[0].payoff

        return dict(
            possible_benefit = possible_benefit,
            number_sliders = number_sliders,
            maliciousness = maliciousness,
            results_player_b = results_player_b
        )

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

class AdditionalSlidersA(Page):
    form_model = 'player'
    form_fields = ['additionalSlidersStart_A','additionalSlidersEnd_A']

    @staticmethod
    def is_displayed(player):
        return not player.winner and player.group.benign_option and player.benignity > 0

    @staticmethod
    def vars_for_template(player):
        num_columns = player.session.config['slider_columns']
        column_width = math.floor(100 / num_columns)
        num_sliders = math.ceil(player.benignity/num_columns)
        max_slider_offset = player.session.config['max_slider_offset']

        offsets = [[random.randint(0, max_slider_offset) for _ in range(num_sliders)] for _ in range(num_columns)]

        for n in range(3):
            if player.benignity < len(offsets[0] + offsets[1] + offsets[2]):
                if len(offsets[2]) > 0:
                    offsets[2].pop()
                elif len(offsets[1]) > 0:
                    offsets[1].pop()
                else:
                    offsets[0].pop()

        return {
            'num_columns': num_columns,
            'num_sliders': num_sliders,
            'offsets': offsets,
            'column_width': column_width
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.payoff += player.benignity / 10

        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")



class SliderRatingA(Page):
    form_model = 'player'
    form_fields = ['slider_rating']

    @staticmethod
    def is_displayed(player):
        return not player.winner and player.group.benign_option and player.benignity > 0

    @staticmethod
    def vars_for_template(player):
        possible_benefit = cu(player.benignity / 10)
        results_player_a = player.payoff
        results_player_b = player.get_others_in_group()[0].payoff

        return dict(
            possible_benefit = possible_benefit,
            results_player_a = results_player_a,
            results_player_b = results_player_b
        )

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

class InstructionsPlayerB(Page):
    @staticmethod
    def is_displayed(player):
        return player.winner

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

class ExpectationsPlayerB(Page):
    form_model = 'player'
    form_fields = ['expected_benignity','expected_maliciousness']

    @staticmethod
    def is_displayed(player):
        return player.winner

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

class DictatorGameB(Page):
    form_model = 'player'
    form_fields = ['repay']

    @staticmethod
    def is_displayed(player):
        return player.winner

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

class SVOExampleB(Page):
    @staticmethod
    def is_displayed(player):
        return player.winner

    @staticmethod
    def vars_for_template(player):
        print(player.session.vars["SVO_Example"])
        SVO = player.session.vars["SVO_Example"][0]

        return dict(
            SVO = SVO
        )

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

class SVOTaskB(Page):
    form_model = 'player'
    form_fields = [
        "svo_choices_B", "svo_tot_ego_B", "svo_tot_alter_B",
        "svo_mean_ego_B", "svo_mean_alter_B", "svo_ratio_B", "svo_angle_B"
    ]

    @staticmethod
    def is_displayed(player):
        return player.winner

    @staticmethod
    def vars_for_template(player):
        SVO = player.session.vars["SVO_Full"]

        return dict(
            SVO = SVO
        )

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

class RandomDrawWaitPage(Page):
    @staticmethod
    def is_displayed(player):
        return player.winner and player.group.field_maybe_none('benign_option') == None

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

class RamdomDrawB(Page):
    @staticmethod
    def is_displayed(player):
        return player.winner

    @staticmethod
    def vars_for_template(player):
        sliders_player_a = player.get_others_in_group()[0].benignity
        profit_player_a = cu(player.get_others_in_group()[0].benignity / 10)
        if player.group.benign_option:
            results_player_a = 2.5 + cu(player.get_others_in_group()[0].benignity / 10)
        else:
            results_player_a = 2.5
        maliciousness_player_a = player.get_others_in_group()[0].maliciousness
        results_player_b = player.payoff

        return dict(
            sliders_player_a = sliders_player_a,
            profit_player_a = profit_player_a,
            results_player_a = results_player_a,
            maliciousness_player_a = maliciousness_player_a,
            results_player_b = results_player_b
        )

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


page_sequence = [
    GroupingWaitPage,
    PageBeforeTask,
    SliderTask,
    InstructionsWaitPage,
    InstructionsPlayerA,
    AttractivenessRatingA,
    PaDeScaleA,
    RamdomDrawA,
    AdditionalSlidersA,
    SliderRatingA,
    InstructionsPlayerB,
    ExpectationsPlayerB,
    DictatorGameB,
    SVOExampleB,
    SVOTaskB,
    RandomDrawWaitPage,
    RamdomDrawB
]
