# Ranks candidates by the Schulze method
# Basile Garcia
import libchoice
import utils


def compute_paths(pairs, candidates):

    """
    Computes strongest paths
    following the algorithm from
     https://en.wikipedia.org/wiki/Schulze_method#Implementation
    """

    paths = {}

    for a, b in pairs.keys():

        if pairs[(a, b)] > pairs[(b, a)]:

            paths[(a, b)] = pairs[(a, b)]

        else:

            paths[(a, b)] = 0

    for i in candidates.keys():

        other_candidates = candidates.copy()

        # remove candidate 'a'
        # in order to not make encounter themselves
        other_candidates.pop(i)

        for j in other_candidates.keys():

            other_candidates_2 = candidates.copy()

            # remove candidate 'a' and 'c'
            # in order to not make encounter themselves
            other_candidates_2.pop(i)
            other_candidates_2.pop(j)

            for k in other_candidates_2.keys():

                paths[(j, k)] = max(paths[(j, k)], min(paths[(j, i)], paths[(i, k)]))

    return paths


if __name__ == '__main__':

    def _wikipedia_example():
        """
        Wikipedia example schulz method example
        https://en.wikipedia.org/wiki/Schulze_method#Example
        """

        import string

        candidates = {k: v for k, v in enumerate(string.ascii_lowercase[:5])}

        a = 0
        b = 1
        c = 2
        d = 3
        e = 4

        pairs = {
            (a, b):  20,
            (a, c):  26,
            (a, d):  30,
            (a, e):  22,
            (b, a):  25,
            (b, c):  16,
            (b, d):  33,
            (b, e):  18,
            (c, a):  19,
            (c, b):  29,
            (c, d):  17,
            (c, e):  24,
            (d, a):  15,
            (d, b):  12,
            (d, c):  28,
            (d, e):  14,
            (e, a):  23,
            (e, b):  27,
            (e, c):  21,
            (e, d):  31
        }

        paths = compute_paths(pairs=pairs, candidates=candidates)

        one_to_one_matrix = libchoice.get_dual_matrix_from_pairwise(pairs=paths, candidates=candidates)

        winner, scores = libchoice.compute_winner(one_to_one_matrix, candidates)

        utils.print_ranking(candidates=candidates, scores=scores)

    _wikipedia_example()
