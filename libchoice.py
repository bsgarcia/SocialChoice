import itertools

import numpy as np


def plurality_rule(votes, candidates, n_votes):

    count = np.zeros(len(candidates))

    for idx in range(len(candidates)):

        count[idx] = sum(n_votes[votes[:, idx] == 0])

    idx_winners = np.arange(len(count))[count == max(count)]

    # Handle ties
    if len(idx_winners) > 1:

        # The winner is the candidate with last name first alphabetically
        winner = sorted([candidates[i] for i in idx_winners])[0]

    else:
        winner = candidates[np.argmax(count)]

    return winner, count


def get_dual_matrix_from_soi(votes, candidates, n_votes):

    """
    runs a one-to-one contest
    for each candidate
    using Strict Order File
    and returns the results
    in a matrix (0 looses, 1 wins)
    """

    pairs = {k: 0 for k in itertools.permutations(candidates.keys(), r=2)}

    n = len(candidates)

    # Fill with -1 in order to detect errors
    dual_matrix = np.ones((n, n)) * -1
    np.fill_diagonal(dual_matrix, 1)

    for a, b in pairs.keys():

        # condition 1: 'a' != -1 (meaning he is ranked)
        a_is_ranked = np.array(votes[:, a] != -1)

        # condition 2: 'a' is ranked higher than 'b'
        # we take the absolute values in case b is absent (-1)
        # in this event we count 'a' as better ranked
        a_is_ranked_higher_than_b = votes[:, a] < np.abs(votes[:, b])

        pairs[(a, b)] = sum(n_votes[a_is_ranked * a_is_ranked_higher_than_b])

    for a, b in pairs.keys():

        # is number of votes higher for a than b
        dual_matrix[a, b] = pairs[(a, b)] > pairs[(b, a)]

    return dual_matrix


def get_dual_matrix_from_pairwise(pairs, candidates):

    """
    runs a one-to-one contest
    for each candidate
    using pairwise file (.pwg)
    and returns the results
    in a matrix (0 looses, 1 wins)
    """
    n = len(candidates)

    # Fill with -1 in order to detect errors
    dual_matrix = np.ones((n, n)) * -1
    np.fill_diagonal(dual_matrix, 1)

    for a, b in pairs.keys():

        # is number of votes higher for a than b
        dual_matrix[a, b] = pairs[(a, b)] > pairs[(b, a)]

    return dual_matrix


def compute_condorcet_winner(dual_matrix, candidates):

    n = len(candidates)
    condorcet_winners = np.zeros(n)

    for x in range(n):

        # set to 1 only if the candidates wins
        # against all candidates
        condorcet_winners[x] = \
            np.all(dual_matrix[x, :])

    if not np.any(condorcet_winners):
        print('No condorcet winner found.')
        return None

    return candidates[np.argmax(condorcet_winners)]


def compute_winner(dual_matrix, candidates):

    """
    returns the candidate that
    won the largest number of the duals
    as well as a score array (idx == candidate idx)
    """

    n = len(candidates)
    scores = np.zeros(n)

    for x in range(n):

        scores[x] = \
            np.sum(dual_matrix[x, :] == 1)

    idx_winners = np.arange(n)[scores == max(scores)]

    # Handle ties
    if len(idx_winners) > 1:

        # The winner is the candidate with last name first alphabetically
        winner = sorted([candidates[i] for i in idx_winners])[0]

    else:
        winner = candidates[np.argmax(scores)]

    return winner, scores


