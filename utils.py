import json

import numpy as np
import pandas as pd
pd.set_option('display.expand_frame_repr', False)


def print_table_one_to_one(dual_matrix, candidates):
    d = {}

    for idx, name in sorted(candidates.items()):
        d[name] = pd.Series(
            np.array(dual_matrix[:, idx], dtype=int),
            index=[candidates[i] for i in range(len(candidates))]
        )

    print('*' * 50)
    print('One-to-one majority contest (X wins or looses vs Y)')
    print(pd.DataFrame(d))
    print('*' * 50)


def print_plurality(candidates, scores):
    d = pd.Series(
        np.sort(scores)[::-1],
        index=[candidates[i] for i in np.argsort(scores)[::-1]]
    )

    print('*' * 50)
    print('Plurality results')
    print(pd.DataFrame(d))
    print('*' * 50)


def print_ranking(candidates, scores, title='Ranking'):
    d = pd.Series(
        np.sort(scores)[::-1],
        index=[candidates[i] for i in np.argsort(scores)[::-1]]
    )

    print('*' * 50)
    print(title)
    print(pd.DataFrame(d))
    print('*' * 50)


def import_strict_order(filename, params):

    """
    returns a matrix of votes
    rows: each order of preferences present in the file
    cols: each candidate index
    data: filled with ints corresponding to the ranking of the candidate
    For instance, if candidate number 0 is ranked 2,
    candidate number 1 is ranked 0,
    candidate number 2 is ranked 1,
    and then candidate 1 > candidate 2 > candidate 0

    the matrix:
    [
        [2, 0, 1]
        ...
    ]

    Also returns an array containing
    the number of votes for each preferences (each line
    in the matrix)
    """

    with open(filename) as f:

        lines = f.readlines()

        n_candidates = int(lines[0])

        votes_beginning_line = params['votes_beginning_line']

        n_rows = len(lines) - votes_beginning_line
        n_votes_for_each_preferences = np.ones(n_rows) * -1

        # Initialize at -1 in order to
        # set candidate absent from a preference ranking to -1
        vote_matrix = np.ones((n_rows, n_candidates)) * -1

        for i, line in enumerate(lines[votes_beginning_line:]):

            data = [int(i) for i in line.split(',')]

            n_votes_for_each_preferences[i] = data[0]

            values = np.array([v - 1 for v in data[1:]])

            preferences = np.array(vote_matrix[i, :])
            preferences[values] = np.arange(len(values))
            vote_matrix[i, :] = preferences

    return vote_matrix, n_votes_for_each_preferences


def import_pairwise(filename, params):

    with open(filename) as f:

        lines = f.readlines()

        votes_beginning_line = params['votes_beginning_line']

        pairs = {}

        for i, line in enumerate(lines[votes_beginning_line:]):

            data = [int(i) for i in line.split(',')]

            n_votes = data[0]
            values = tuple(v - 1 for v in data[1:])

            pairs[values] = n_votes

    return pairs


def import_params(filename):

    return json.load(open(f'{filename}-parameters.json'))


def import_candidates(filename):

    candidates_json = json.load(open(f'{filename}-candidates.json'))
    candidates = {int(k): v for k, v in candidates_json.items()}
    return candidates

