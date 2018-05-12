import utils
import libchoice


def main():

    dataset = {
        'north_ireland_2012': 'ED-00001-00000001',
        'debian_logo': 'ED-00002-00000008'
    }

    filename = dataset['north_ireland_2012']

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

    dual_matrix = libchoice.get_dual_matrix_from_pairwise(
        pairs=pairs, candidates=candidates
    )

    winner, scores = libchoice.compute_winner(
        dual_matrix=dual_matrix, candidates=candidates
    )

    utils.print_table_one_to_one(dual_matrix, candidates)
    utils.print_ranking(
        candidates=candidates, scores=scores, title='Ranking'
    )

    # ----------------- Condorcet winner ---------------------------- #

    condorcet_winner = libchoice.compute_condorcet_winner(
        dual_matrix=dual_matrix, candidates=candidates
    )

    print(f'The condorcet winner is {condorcet_winner}.')


if __name__ == '__main__':
    main()
