import random
from otree.api import *

doc = """
One player decides how to divide a certain amount between himself and the other
player.
See: Kahneman, Daniel, Jack L. Knetsch, and Richard H. Thaler. "Fairness
and the assumptions of economics." Journal of business (1986):
S285-S300.
"""

class C(BaseConstants):
    NAME_IN_URL = 'dictator'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = cu(20)

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    computer_decided = models.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.computer_decided = random.randint(0, 1)

    kept = models.CurrencyField(
        doc="""Amount dictator decided to keep for himself""",
        min=0,
        max=C.ENDOWMENT,
        label="I will keep",
    )

    computer_decision = models.CurrencyField(
        doc="""Amount decided by computer""",
        min=0,
        max=C.ENDOWMENT,
        label="Computer decision",
    )

class Player(BasePlayer):
    pass

# FUNCTIONS

def computer_decision(group: Group):
    for p in group.get_players():
        if p.id_in_group == 2: # If the player is the receiver
            if group.computer_decided == 1:
                group.computer_decision = random.choice([0, C.ENDOWMENT])
                group.kept = group.computer_decision  # Set group.kept for consistency
                break # Only one player needs to have their decision set


def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    if p1.id_in_group == 1:  # Dictator
        if group.computer_decided == 0:
            p1.payoff = group.kept
            p2.payoff = C.ENDOWMENT - group.kept
        else:
            p1.payoff = group.computer_decision
            p2.payoff = C.ENDOWMENT - group.computer_decision
    else:  # Receiver
        if group.computer_decided == 1:
            p1.payoff = group.computer_decision
            p2.payoff = C.ENDOWMENT - group.computer_decision
        else:
            p1.payoff = group.kept
            p2.payoff = C.ENDOWMENT - group.kept

# PAGES
class Introduction(Page):
    def before_next_page(self, timeout_happened):
        group = self.group
        for p in group.get_players():
            if p.id_in_group == 2: # If the player is the receiver
                if group.computer_decided == 1:
                    group.computer_decision = random.choice([0, C.ENDOWMENT])
                    group.kept = group.computer_decision  # Set group.kept for consistency
                    break

class OfferD(Page):
    form_model = 'group'
    form_fields = ['kept']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 1 and player.group.computer_decided == 0

class OfferC(Page):
    form_model = 'group'

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 1 and player.group.computer_decided == 1


class OfferR(Page):
    form_model = 'group'

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 2

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        computer_decision(self.group)
        set_payoffs(self.group)


class Results(Page):
    @staticmethod
    def vars_for_template(player):
        group = player.group
        return dict(offer=C.ENDOWMENT - group.kept)

class PaymentInfo(Page):
    pass


page_sequence = [Introduction, OfferD, OfferC, OfferR, ResultsWaitPage, Results, PaymentInfo]
