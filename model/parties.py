from enum import Enum


class Parties(Enum):
    # 10 largest parties according to last poll
    BlueAndWhite = 0
    Likud = 1
    Labor = 2
    HadashTaal = 3
    UnitedTorah = 4
    UnionOfRightWing = 5
    NewRight = 6
    Meretz = 7
    Shas = 8
    Zehut = 9
    Kulanu = 10
    Unknown = 99


# Top 10 politicians from each party list for 2019 elections
# Some parties has less than 10 candidates since they simply does not have a twitter accounts...
categorized_twitter_accounts = {
    'gantzbe': Parties.BlueAndWhite,
    'yairlapid': Parties.BlueAndWhite,
    'bogie_yaalon': Parties.BlueAndWhite,
    'avinissenkorn': Parties.BlueAndWhite,
    'netanyahu': Parties.Likud,
    'giladerdan1': Parties.Likud,
    'YuliEdelstein': Parties.Likud,
    'israel_katz': Parties.Likud,
    'GabbayAvi': Parties.Labor,
    'rousso_tal': Parties.Labor,
    'ishmuli': Parties.Labor,
    'StavShaffir': Parties.Labor,
    'AyOdeh': Parties.HadashTaal,
    'ahmad_tibi': Parties.HadashTaal,
    'AidaTuma': Parties.HadashTaal,
    'ofercass': Parties.HadashTaal,
    'gafni_moshe': Parties.UnitedTorah,
    'realrafiperets': Parties.UnionOfRightWing,
    'bezalelsm': Parties.UnionOfRightWing,
    'MotiYogev': Parties.UnionOfRightWing,
    'ofir885': Parties.UnionOfRightWing,
    'naftalibennett': Parties.NewRight,
    'ayelet__shaked': Parties.NewRight,
    'alonabarkat': Parties.NewRight,
    'Shuli_MR': Parties.NewRight,
    'tamarzandberg': Parties.Meretz,
    'mkgilon': Parties.Meretz,
    'Michal_Rozin': Parties.Meretz,
    'EsawiFr': Parties.Meretz,
    'ariyederi': Parties.Shas,
    'yakmargi': Parties.Shas,
    'BentzurYoav': Parties.Shas,
    'moshefeiglin': Parties.Zehut,
    'haimamsalem': Parties.Zehut,
    'ronitdror': Parties.Zehut,
    'albertlevy': Parties.Zehut,
    'kahlonmoshe': Parties.Kulanu,
    'elicoh1': Parties.Kulanu,
    'sbyifat': Parties.Kulanu,
    'Roy_Folkman': Parties.Kulanu,
}