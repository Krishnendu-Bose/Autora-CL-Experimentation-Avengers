from sweetpea import Factor, CrossBlock, synthesize_trials, CMSGen, experiments_to_dicts, WithinTrial, \
    DerivedLevel, Transition, AtMostKInARow, RandomGen


def congruent(color, word):
    return color == word

def incongruent(color, word):
    return not congruent(color, word)

def response_left(color):
    return color == "red"

def response_right(color):
    return color == "green"

def response_repeat(response):
    return response[0] == response[-1]

def response_switch(response):
    return not response_repeat(response)

def trial_sequences(iteration):
    color = Factor("color", ["red", "green"])
    word = Factor("word", ["red", "green"])

    congruency = Factor("congruency", [
        DerivedLevel("con", WithinTrial(congruent, [color, word])),
        DerivedLevel("inc", WithinTrial(incongruent, [color, word]))
    ])

    response = Factor("correct_response", [
        DerivedLevel("f", WithinTrial(response_left, [color])),
        DerivedLevel("j", WithinTrial(response_right, [color]))
    ])

    resp_transition = Factor("response_transition", [
        DerivedLevel("repeat", Transition(response_repeat, [response])),
        DerivedLevel("switch", Transition(response_switch, [response]))
    ])

    constraints = [AtMostKInARow(7, resp_transition)]
    design = [color, word, congruency, resp_transition, response]
    crossing = [color, word, resp_transition]
    block = CrossBlock(design, crossing, constraints)

    if iteration == "initial":
        experiments = synthesize_trials(block, 5, CMSGen)
    else:
        experiments = synthesize_trials(block, 5, RandomGen(acceptable_error=3))

    return experiments_to_dicts(block, experiments)
