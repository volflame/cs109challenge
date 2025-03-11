import pandas as pd
import csv
import numpy as np
from loader import load_prof_data
import matplotlib
matplotlib.use('Agg')  # Prevents GUI issues on macOS

import matplotlib.pyplot as plt

def main():
    prof_pmf, question_data = load_prof_data('professors.csv')
    #print(prof_pmf)
    #while not is_certain(prof_pmf):
    while not is_certain(prof_pmf):
        print("--------------------------")
        print_probs(prof_pmf)
        print(f"=> Uncertainty: {compute_uncertainty(prof_pmf):.2f}")
        best_question = chose_best_question(prof_pmf, question_data)
        answer = parse_yes_no(input(f"{best_question} "))
        prof_pmf = compute_posterior(prof_pmf, question_data[best_question], answer)
        plot(prof_pmf).show()
        
    print("====================================\n")
    print(f"=> Uncertainty: {compute_uncertainty(prof_pmf):.2f}")
    print(f"Your culprit is {max(prof_pmf, key=prof_pmf.get)}")

def chose_best_question(prof_pmf, question_data):
    # select the question which minimizes the expected uncertainty
    best_question = None
    best_uncertainty = None
    for question in question_data:
        expected_uncertainty = compute_expected_uncertainty(prof_pmf, question_data[question])
        if best_question is None or expected_uncertainty < best_uncertainty:
            best_question = question
            best_uncertainty = expected_uncertainty
    return best_question

def compute_expected_uncertainty(prof_pmf, question_data):
    # compute the entropy of the distribution
    prob_yes = compute_prob_yes(prof_pmf, question_data)
    prob_no = 1 - prob_yes

    pmf_yes = compute_posterior(prof_pmf, question_data, True)
    pmf_no = compute_posterior(prof_pmf, question_data, False)

    uncertainty_yes = compute_uncertainty(pmf_yes)
    uncertainty_no = compute_uncertainty(pmf_no)

    return prob_yes * uncertainty_yes + prob_no * uncertainty_no

def compute_uncertainty(prof_pmf):
    entropy = 0
    for prof_i in prof_pmf:
        p_i = prof_pmf[prof_i]
        entropy += -np.log2(p_i) * p_i
    return entropy

def compute_posterior(prof_pmf, question_data, answer):
    # compute the posterior distribution
    pmf = {}
    for prof in prof_pmf:
        if question_data[prof] == answer:
            pmf[prof] = prof_pmf[prof]
    normalize_pmf(pmf)
    return pmf

def compute_prob_yes(prof_pmf, question_data):
    # compute the probability of the animal being a yes
    prob_yes = 0
    for prof in prof_pmf:
        if question_data[prof]:
            prob_yes += prof_pmf[prof]
    return prob_yes


def is_certain(prof_pmf):
    # if any animal has a probability of 1, we are certain
    for prof in prof_pmf:
        if prof_pmf[prof] == 1:
            return True
    return False

def parse_yes_no(response):
    if response.lower() == 'yes':
        return True
    if response.lower() == 'no':
        return False
    raise ValueError("Response must be 'yes' or 'no'")

def calc_uncertainty(prof_pmf):
    uncertainty = 0
    for prof in prof_pmf:
        p_x = prof_pmf[prof]
        if p_x == 0: continue
        surprise_x = np.log2(1/p_x)
        uncertainty += surprise_x * p_x  
    return uncertainty

def is_certain(prof_pmf):
    # if any animal has a probability of 1, we are certain
    for prof in prof_pmf:
        if prof_pmf[prof] == 1:
            return True
    return False

def print_probs(prof_pmf):
    for prof in prof_pmf:
        print(prof + ": " + str(prof_pmf[prof]))
        
def normalize_pmf(prof_pmf):
    total = sum(prof_pmf.values())
    for prof in prof_pmf:
        prof_pmf[prof] /= total
        
def plot(prof_pmf):
    plt.rcParams['font.family'] = 'Comic Sans MS'
    plt.rcParams['axes.facecolor'] = '#27445D'
    plt.rcParams['figure.facecolor'] = '#27445D'
    
    COLOR = 'white'
    plt.rcParams['text.color'] = COLOR
    plt.rcParams['axes.labelcolor'] = COLOR
    plt.rc('axes',edgecolor=COLOR)
    plt.rcParams['xtick.color'] = COLOR
    plt.rcParams['ytick.color'] = COLOR
    #plt.plot(prof_pmf.keys(), prof_pmf.values())
    plt.bar(prof_pmf.keys(), prof_pmf.values(), color='white')
    plt.xticks(rotation=90, fontsize=5)
    # Add labels and title
    plt.xlabel("Prof Names")
    plt.ylabel("Probabilities")
    plt.title("Probability of your culprit")

    # Display the plot
    return plt
    
if __name__ == '__main__':
    main()