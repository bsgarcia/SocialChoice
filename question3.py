import itertools
import string
import numpy as np

import utils
import libchoice
import schulze



def main():

    dataset = {
        'north_ireland_2012': 'ED-00001-00000001',
        'debian_logo': 'ED-00002-00000008'
    }

    filename = dataset['debian_logo']

    # ------------------- Load extra json files -------------------- #

    params = utils.import_params(
        filename=f'json/{filename}'
    )

    candidates = utils.import_candidates(
        filename=f'json/{filename}'
    )

    # -------------------- Load preflib files ---------------------- #

    pairs = utils.import_pairwise(
        filename=f'data/{filename}.pwg', params=params
    )

    vote_matrix, n_votes = utils.import_strict_order(
        filename=f'data/{filename}.soi', params=params
    )

    # -------------------  Plurality rule ---------------------------- #

    plurality_rule_winner, scores = libchoice.plurality_rule(
        votes=vote_matrix, candidates=candidates, n_votes=n_votes
    )

    utils.print_plurality(candidates, scores=scores)
    print(f'The plurality rule winner is {plurality_rule_winner}.')

    # ------------------- Pairwise methods --------------------------- #

    # From soi file
    dual_results_soi = libchoice.get_dual_matrix_from_soi(votes=vote_matrix, n_votes=n_votes, candidates=candidates)

    winner, scores = libchoice.compute_winner(dual_matrix=dual_results_soi, candidates=candidates)

    utils.print_ranking(candidates, scores, title='Pair ranking from SOI file no particular method')

    # From pairwise file
    paths = schulze.compute_paths(
        pairs=pairs, candidates=candidates
    )
    dual_results_schulze = libchoice.get_dual_matrix_from_pairwise(
        pairs=paths, candidates=candidates
    )

    winner, scores = libchoice.compute_winner(
        dual_matrix=dual_results_schulze, candidates=candidates
    )

    utils.print_table_one_to_one(dual_results_schulze, candidates)
    utils.print_ranking(candidates=candidates, scores=scores, title='Schulz ranking')

    # ----------------- Condorcet winner ---------------------------- #

    condorcet_winner = libchoice.compute_condorcet_winner(
        dual_matrix=dual_results_schulze, candidates=candidates
    )

    print(f'The condorcet winner is {condorcet_winner}.')


# def long_randomized_dataset():
#
#     candidates = {k: v for k, v in enumerate(string.ascii_uppercase[:2])}
#
#     combinations = itertools.permutations(candidates.keys(), r=len(candidates))
#
#     n_candidates = len(candidates)
#     n_ranking = round(np.math.factorial(n_candidates) / np.math.factorial(n_candidates - n_candidates))
#
#     vote_matrix = np.zeros((n_ranking, n_candidates))
#
#     for i in range(n_ranking):
#
#         vote_matrix[i, :] = [string.ascii_letters.index(i) for i in combinations]
#
#     n_votes = np.random.randint(1000, size=n_ranking)
#
#     print(f'Generated {n_candidates} and {n_ranking}.')
#
#     # -------------------  Plurality rule ---------------------------- #
#     plurality_rule_winner, scores = libchoice.plurality_rule(
#         votes=vote_matrix, candidates=candidates, n_votes=n_votes
#     )
#
#     utils.print_plurality(candidates, scores=scores)
#     print(f'The plurality rule winner is {plurality_rule_winner}.')
#
#     # ------------------- Pairwise methods --------------------------- #
#
#     pairs = {k: np.random.randint(100) for k in itertools.permutations(candidates.keys(), r=2)}
#
#     dual_results_soi = libchoice.get_dual_matrix_from_pairwise(pairs=pairs, candidates=candidates)
#
#     winner, scores = libchoice.compute_winner(dual_matrix=dual_results_soi, candidates=candidates)
#
#     utils.print_ranking(candidates, scores, title='Pair ranking from SOI file no particular method')
#
#     # From pairwise file
#     paths = schulze.compute_paths(
#         pairs=pairs, candidates=candidates
#     )
#     dual_results_schulze = libchoice.get_dual_matrix_from_pairwise(
#         pairs=paths, candidates=candidates
#     )
#
#     winner, scores = libchoice.compute_winner(
#         dual_matrix=dual_results_schulze, candidates=candidates
#     )
#
#     utils.print_table_one_to_one(dual_results_schulze, candidates)
#     utils.print_ranking(candidates=candidates, scores=scores, title='Schulz ranking')
#
#     # ----------------- Condorcet winner ---------------------------- #
#
#     condorcet_winner = libchoice.compute_condorcet_winner(
#         dual_matrix=dual_results_schulze, candidates=candidates
#     )
#
#     print(f'The condorcet winner is {condorcet_winner}.')


if __name__ == '__main__':
    main()

