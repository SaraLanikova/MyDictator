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
