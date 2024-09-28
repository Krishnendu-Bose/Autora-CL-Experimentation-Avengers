import json

from autora.variable import VariableCollection, Variable
from autora.experimentalist.random import pool
from autora.experiment_runner.firebase_prolific import firebase_runner
from autora.state import StandardState, on_state, Delta

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sweetbean.sequence import Block, Experiment
from sweetbean.stimulus import TextStimulus
from trial_sequence import trial_sequences
from stimulus_sequence import stimulus_sequence

variables = VariableCollection(
    independent_variables=[
        Variable(name="word", allowed_values=["red", "green"]),
        Variable(name="color", allowed_values=["red", "green"]),
        Variable(name="response_transition", allowed_values=["f", "j"]),
    ],
    dependent_variables=[
        Variable(name="rt", value_range=(0, 10000)),
        Variable(name="response", allowed_values=["f", "j"]),
    ]
)

state = StandardState(
    variables=variables,
)

@on_state()
def theorist_on_state(experiment_data, variables):
    X_train = conditions[['word', 'color', 'response_transition']]
    y_train = conditions['rt']
    model = LinearRegression()
    model.fit(X_train, y_train)
    return Delta(models=[model])

@on_state()
def experimentalist_on_state(variables, num_samples):
    return Delta(conditions=pool(variables, num_samples))

firebase_credentials = {
    # TO RUN IT: PUT CREDENTIALS HERE!
}


experiment_runner = firebase_runner(
    firebase_credentials=firebase_credentials,
    time_out=100,
    sleep_time=5,
)

@on_state()
def runner_on_state(conditions):
    res = []
    for idx, row in conditions.iterrows():
        trials = trial_sequences("initial") if idx == 0 else trial_sequences("update")
        res.append(stimulus_sequence(trials))

    conditions_to_send = conditions.copy()
    conditions_to_send['experiment_code'] = res

    data_raw = experiment_runner(conditions_to_send)
    experiment_data = pd.DataFrame()

    for item in data_raw:
        _lst = json.loads(item)['trials']
        _df = trial_list_to_experiment_data(_lst)
        experiment_data = pd.concat([experiment_data, _df], axis=0)
    return Delta(experiment_data=experiment_data)

def trial_list_to_experiment_data(trial_sequence):
    """
    Parse a trial sequence (from jsPsych) into dependent and independent variables
    independent: word, color, response_transition
    dependent: rt, response
    """
    res_dict = {
        'word': [],
        'color': [],
        'response_transition': [],
        'rt': [],
        'response': []
    }
    for trial in trial_sequence:
        # Filter trials that are not ROK (instructions, fixation, ...)
        if trial['trial_type'] != 'rok':
            continue
        # Filter trials without rt
        if 'rt' not in trial or trial['rt'] is None:
            continue
        # the intensity is equivalent to the number of oobs (set in sweetBean script)
        # rt is a default value of every trial
        word = trial['number_of_oobs'][0]
        color = trial['number_of_oobs'][1]
        rt = trial['rt']
        response = trial['response']

        res_dict['word'].append(word)
        res_dict['color'].append(color)
        res_dict['rt'].append(float(rt))
        res_dict['response'].append(response)

    dataframe_raw = pd.DataFrame(res_dict)

    # Calculate the mean rt for each word/color combination
    grouped = dataframe_raw.groupby(['word', 'color']).mean().reset_index()

    return grouped

def run_iteration(i, beta_samples_train, n_samples_mcmc, step_size):
    timelines = experiment_runner.sample_trials("initial")

    stimulus_sequence(timelines[0])

    timeline0 = DataFrame.from_dict(timelines[0])

    time.sleep(50)

    filtered_df = read_experiment_data.read_experiment_data()

    timeline0['rt'] = filtered_df['rt']
    timeline0['response'] = filtered_df['response']
    df_encoded = pd.get_dummies(timeline0[['word', 'color', 'response_transition']], drop_first=True)
    X_train = df_encoded.values
    y_train = timeline0['rt'].values

    if i == 0:
        return theorist.run_theory("initial", 0, 0, n_samples_mcmc, step_size, X_train, y_train)
    else:
        posterior_means = np.mean(beta_samples_train, axis=0)
        posterior_variances = np.var(beta_samples_train, axis=0)
        return theorist.run_theory("update", posterior_means, posterior_variances, n_samples_mcmc, step_size, X_train,
                                   y_train)


def run_experiment_with_max_uncertainty(beta_samples_train, n_samples_mcmc, step_size):
    timelines = experiment_runner.sample_trials("initial")

    timeline0 = DataFrame.from_dict(timelines[0])
    max_uncertainty = experimentalist.sample_condition(timeline0, beta_samples_train)
    timeline0_dict = timeline0.iloc[max_uncertainty].to_dict()
    timelines = experiment_runner.sample_trials("update")
    max_freq_timeline = max(timelines, key=lambda t: sum(1 for trial in t if
                                                         trial["word"] == timeline0_dict["word"] and trial["color"] ==
                                                         timeline0_dict["color"] and trial["response_transition"] ==
                                                         timeline0_dict["response_transition"]))
    stimulus_sequence(max_freq_timeline)
    time.sleep(50)
    filtered_df = read_experiment_data.read_experiment_data()
    timeline0 = DataFrame.from_dict(max_freq_timeline)
    timeline0['rt'] = filtered_df['rt']
    timeline0['response'] = filtered_df['response']
    df_encoded = pd.get_dummies(timeline0[['word', 'color', 'response_transition']], drop_first=True)
    X_train = df_encoded.values
    y_train = timeline0['rt'].values
    posterior_means = np.mean(beta_samples_train, axis=0)
    posterior_variances = np.var(beta_samples_train, axis=0)

    return theorist.run_theory("update", posterior_means, posterior_variances, n_samples_mcmc, step_size, X_train,
                               y_train)

for i in range(5):
    n_samples_mcmc = 5000
    step_size = 0.1
    beta_samples_train, sigma2_samples_train = None, None

    for i in range(5):
        if i < 2:
            # beta_samples_train, sigma2_samples_train = run_iteration(i, beta_samples_train, n_samples_mcmc, step_size)
            state = experimentalist_on_state(state, num_samples=2)  # Collect 2 conditions per iteration
            state = runner_on_state(state)
            state = theorist_on_state(state)
        else:
            # beta_samples_train, sigma2_samples_train = run_experiment_with_max_uncertainty(beta_samples_train, n_samples_mcmc, step_size)
            state = experimentalist_on_state(state, num_samples=2)  # Collect 2 conditions per iteration
            state = runner_on_state(state)
            state = theorist_on_state(state)

def report_linear_fit(m: LinearRegression, precision=4):
    s = f"y = {np.round(m.coef_[0].item(), precision)} x " \
        f"+ {np.round(m.intercept_.item(), 4)}"
    return s

print(report_linear_fit(state.models[0]))
print(report_linear_fit(state.models[-1]))
