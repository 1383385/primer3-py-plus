import random

from primer3plus.design import Design
from primer3plus.utils import anneal
from primer3plus.utils import reverse_complement


def test_init():
    design = Design()


def test_set(gfp):
    design = Design()
    design.presets.template(gfp)
    design.presets.left_sequence(gfp[60:85])
    design.presets.as_generic_task()
    results = design.run()
    print(results)
    assert results


def check_primers(gfp, primerlist):

    fwd, rev = anneal(gfp, primerlist, n_bases=16)

    span_region_ok = []
    for primer in fwd:
        s = primer["start"]
        l = len(primer["anneal"])
        span_region_ok.append([s, l, -1, -1])
    for primer in rev:
        s = primer["start"]
        l = len(primer["anneal"])
        span_region_ok.append([-1, -1, s, l])
    return span_region_ok


def test_gfp(gfp, iter_random_primer):
    fwd_primers = list(iter_random_primer(25, gfp[:250], 16))
    rev_primers = list(iter_random_primer(25, reverse_complement(gfp)[:250], 16))

    primers = fwd_primers + rev_primers

    # from itertools import product
    #
    # for f, r in product(fwd_primers,  rev_primers):
    #     design = Design()
    #     design.presets.left_sequence(f)
    #     design.presets.right_sequence(r)
    #     design.presets.task('check_primers')
    #     design.presets.template(gfp)
    #     design.run()

    region_ok = check_primers(gfp, primers)
    # print(region_ok[:1])
    design = Design()
    design.presets.template(gfp)
    print(region_ok)
    design.presets.pair_region_list(region_ok[:10])
    design.presets.product_size([50, 2000])
    pairs, explain = design.run()
    print(explain)
    print(pairs)


def test_product_size_list(gfp):

    design = Design()
    design.presets.template(gfp)
    design.presets.product_size([(50, 100), (200, 300)])
    design.run()
