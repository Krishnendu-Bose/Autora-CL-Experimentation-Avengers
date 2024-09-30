from sweetbean.parameter import TimelineVariable, DerivedParameter, DerivedLevel, DataVariable
from sweetbean.sequence import Block, Experiment
from sweetbean.stimulus import TextStimulus


# DEFINE CONGRUENCY FACTOR
def congruent(color, word):
    return color == word

def incongruent(color, word):
    return not congruent(color, word)

# DEFINE RESPONSE FACTOR
def response_left(color):
    return color == "red"

def response_right(color):
    return color == "green"

# DEFINE RESPONSE TRANSITION FACTOR
def response_repeat(response):
    return response[0] == response[-1]

def response_switch(response):
    return not response_repeat(response)

# defining the predicate for the f-level of the "correct response" parameter
def is_correct_f(color):
    return color == 'red'

# defining the predicate for the j-level of the "correct response" parameter
def is_correct_j(color):
    return color == 'green'

# positive feedback after correct responses (remember the correct data variable has boolean levels itself)
def is_positive_feedback(correct):
    return correct

# negative feedback after incorrect responses
def is_negative_feedback(correct):
    return not correct

def stimulus_sequence(timeline):
    # Creating the Instructions
    welcome = TextStimulus(
        text="Welcome to our experiment.<br />Here, you will have to react to the ink color of a color word.<br />Press "
             "SPACE to continue",
        color='black',
        choices=[' '])
    instruction_red = TextStimulus(
        text="If the ink color is <b>red</b>,<br />press <b>F</b> with your left index finger as fast as "
             "possible.<br />Press F to continue",
        color='black',
        choices=['f'])
    instruction_green = TextStimulus(
        text="If the ink color is <b>green</b>,<br />press <b>J</b> with your right index finger as fast as "
             "possible.<br />Press J to continue",
        color='black',
        choices=['j'])
    instructions_end = TextStimulus(
        text="The experiment will start now.<br />React as fast an as accurate as possible.<br />Remember:<br />React to "
             "the ink color not the meaning of the word.<br />Press SPACE to continue",
        color='black',
        choices=[' '])

    # Creating the stimulus sequence
    instructions_sequence = [welcome, instruction_red, instruction_green, instructions_end]

    # Creating the block
    instructions_block = Block(instructions_sequence)

    # declare the timeline variables
    # color: The name has to be color (it is the name in the timeline), and it has the levels red and green
    color = TimelineVariable(name="color", levels=["red", "green"])

    # word: The name has to be word (it is the name in the timeline), and it has the levels RED and GREEN
    word = TimelineVariable(name="word", levels=["RED", "GREEN"])

    # declare the f level
    correct_response_f = DerivedLevel(value='f', predicate=is_correct_f, factors=[color])

    # declare the j level
    correct_response_j = DerivedLevel('j', is_correct_j, [color])

    # declare the "correct response" parameter
    correct_response = DerivedParameter(name='correct_response', levels=[correct_response_f, correct_response_j])

    # declaring the stimulus
    stroop = TextStimulus(duration=2500, text=word, color=color, choices=['j', 'f'], correct_key=correct_response)

    # declare the data variable
    correct = DataVariable('correct', [True, False])

    positive_word_feedback = DerivedLevel('correct', is_positive_feedback, [correct], 1)
    negative_word_feedback = DerivedLevel('false', is_negative_feedback, [correct], 1)

    feedback_word = DerivedParameter('feedback_word', [positive_word_feedback, negative_word_feedback])
    # create the levels
    positive_color_feedback = DerivedLevel('green', is_positive_feedback, [correct], 1)
    negative_color_feedback = DerivedLevel('red', is_negative_feedback, [correct], 1)
    # create the parameter
    feedback_color = DerivedParameter('feedback_color', [positive_color_feedback, negative_color_feedback])
    feedback = TextStimulus(duration=1000, text=feedback_word, color=feedback_color)

    # fixation stimulus
    fixation = TextStimulus(800, '+')

    # create a stimulus sequence
    stimulus_sequence = [fixation, stroop, feedback]

    # create the trial block
    trial_block = Block(stimulus_sequence, timeline)

    # create the experiment from the two blocks
    experiment = Experiment([instructions_block, trial_block])
    # return a js string to transfer to autora
    return experiment.to_js_string(as_function=True, is_async=True)
