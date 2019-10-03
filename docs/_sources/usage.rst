Usage
=====

Setting design parameters
-------------------------

Design parameters can be set using built in preset methods:

.. code-block:: python

    # a new task
    design = Design()

    # set template sequence
    design.presets.template("AGGTTGCGTGTGTATGGTCGTGTAGTGTGT")

    # set left primer sequence
    design.presets.left_sequence("GTTGCGTGTGT)

    # set as a cloning task
    design.presets.as_cloning_task()

    # run the design task
    design.run()

Parameters can be set more directly, but this requires knowing the names of the
parameters:

.. code-block:: python

    design.update({
        'SEQUENCE_TEMPLATE': 'AGGTTGCGTGTGTATGGTCGTGTAGTGTGT',
        'SEQUENCE_PRIMER': 'GTTGCGTGTGT',
        'PRIMER_PICK_LEFT_PRIMER': 0,
        'PRIMER_TASK': 'cloning_task'
    })
    design.run()

If using an interactive terminal, descriptors are provided to the :class:`Design <primer3plus.Design>`,
which usually can be accessed by typing `design.[TAB]`

.. code-block:: python

    print(design.SEQUENCE_TEMPLATE)
    print(design.SEQUENCE_TEMPLATE))

setting using presets
*********************

The :meth:`presets <primer3plus.Design.presets>` (returning a
:class:`DesignPresets <primer3plus.design.DesignPresets>`) provides several
convenient methods for setting common tasks:

.. testsetup::

    from primer3plus import Design

.. testcode::

    design = Design()
    design.presets.template("ACGGGGAGTTGTCTGTAGGTTGATTATGTGTGTCGTGTGTGTATATGGGTCTGA")
    print(design.get('SEQUENCE_TEMPLATE').value)

.. testoutput::

    ACGGGGAGTTGTCTGTAGGTTGATTATGTGTGTCGTGTGTGTATATGGGTCTGA

setting from a single key-value pair
************************************

Preferred way to set parameters not available in the presets, is to use
:meth:`set <primer3plus.Design.set>`:

.. code-block::

    # preferred
    design.set('SEQUENCE_TEMPLATE', 'foo')

setting from a dictionary
*************************

If setting many parameters, use :meth:`update <primer3plus.Design.update>`:

.. code-block::

    design.update({
        'SEQUENCE_TEMPLATE': "AGGGGTAGTAGTATGTGAAGGGGTAGTAGTATGTGAAGGGGTAGTAGTATGTGAAGGGGTAGTAGTATGTGA",
        'LEFT_SEQUENCE': 'TAGTAGTATGTGAAGG'
    })

getting help
************

To get help with a parameter, access it using :meth:`get <primer3plus.Design.get>`
or as a descriptor and call :meth:`help <primer3plus.params.Parameter.help>`

.. testcode::

    print(design.SEQUENCE_TEMPLATE.help())
    # print(design.get('SEQUENCE_TEMPLATE').help())

.. testoutput::

    http://primer3.ut.ee/primer3web_help.htm#SEQUENCE_TEMPLATE

Design cloning primers
------------------------

.. testcode::

    import json

    design = Design()
    design.presets.template('TCATGTAATTAGTTATGTCACGCTTACATTCACGCCCTCCCCCCACATCCGCTCTAACCGAAAAGGAAGGAGTTAGACAACCTGAAGTCTAGGTCCCTATTTATTTTTTTATAGTTATGTTAGTATTAAGAACGTTATTTATATTTCAAATTTTTCTTTTTTTTCTGTACAGACGCGTGTACGCATGTAACATTATACTGAAAACCTTGCTTGAGAAGGTTTTGGGACGCTCGAAGGCTTTAATTTGC')
    design.presets.as_cloning_task()
    design.presets.primer_num_return(1)
    results, explain = design.run()

    print(json.dumps(results, indent=1))
    print(json.dumps(explain, indent=1))

.. testoutput::

    {
     "0": {
      "PAIR": {
       "PENALTY": 11.204301707622733,
       "COMPL_ANY_TH": 0.0,
       "COMPL_END_TH": 0.0,
       "PRODUCT_SIZE": 248
      },
      "LEFT": {
       "PENALTY": 9.027129166714644,
       "SEQUENCE": "TCATGTAATTAGTTATGTCACGCTTAC",
       "location": [
        0,
        27
       ],
       "TM": 57.972870833285356,
       "GC_PERCENT": 33.333333333333336,
       "SELF_ANY_TH": 0.0,
       "SELF_END_TH": 0.0,
       "HAIRPIN_TH": 0.0,
       "END_STABILITY": 2.34
      },
      "RIGHT": {
       "PENALTY": 2.1771725409080886,
       "SEQUENCE": "GCAAATTAAAGCCTTCGAGCG",
       "location": [
        247,
        21
       ],
       "TM": 58.82282745909191,
       "GC_PERCENT": 47.61904761904762,
       "SELF_ANY_TH": 0.0,
       "SELF_END_TH": 0.0,
       "HAIRPIN_TH": 38.006257959698985,
       "END_STABILITY": 5.03
      }
     }
    }
    {
     "PRIMER_LEFT_EXPLAIN": "considered 10, low tm 9, ok 1",
     "PRIMER_RIGHT_EXPLAIN": "considered 10, low tm 3, high tm 4, ok 3",
     "PRIMER_PAIR_EXPLAIN": "considered 1, ok 1",
     "PRIMER_LEFT_NUM_RETURNED": 1,
     "PRIMER_RIGHT_NUM_RETURNED": 1,
     "PRIMER_INTERNAL_NUM_RETURNED": 0,
     "PRIMER_PAIR_NUM_RETURNED": 1
    }

Design primers that target the region


Designing the right primer only
-------------------------------

.. code-block::

    design = Design()
    design.presets.template("TCATGTAATTAGTTATGTCACGCTTACATTCACGCCCTCCCCCCACATCCGCTCTAACCGAAAAGGAAGGAGTTAGACAACCTGAAGTCTAGGTCCCTATTTATTTTTTTATAGTTATGTTAGTATTAAGAACGTTATTTATATTTCAAATTTTTCTTTTTTTTCTGTACAGACGCGTGTACGCATGTAACATTATACTGAAAACCTTGCTTGAGAAGGTTTTGGGACGCTCGAAGGCTTTAATTTGC")
    design.presets.left_sequence('GTTATGTCACGCTTACATTCACG')
    design.presets.as_cloning_task()
    design.run()


Design primers targeting interval
---------------------------------

.. code-block::

    design = Design()
    design.presets.template("TCATGTAATTAGTTATGTCACGCTTACATTCACGCCCTCCCCCCACATCCGCTCTAACCGAAAAGGAAGGAGTTAGACAACCTGAAGTCTAGGTCCCTATTTATTTTTTTATAGTTATGTTAGTATTAAGAACGTTATTTATATTTCAAATTTTTCTTTTTTTTCTGTACAGACGCGTGTACGCATGTAACATTATACTGAAAACCTTGCTTGAGAAGGTTTTGGGACGCTCGAAGGCTTTAATTTGC")
    design.presets.target((50, 150))
    design.run()


Relaxing parameters
-------------------

In this example, the parameter conditions are too strict to find a primer pair
the first time around:

.. testcode::

    design = Design()
    design.presets.template("TCATGTAATTAGTTATGTCACGCTTACATTCACGCCCTCCCCCCACATCCGCTCTAACCGAAAAGGAAGGAGTTAGACAACCTGAAGTCTAGGTCCCTATTTATTTTTTTATAGTTATGTTAGTATTAAGAACGTTATTTATATTTCAAATTTTTCTTTTTTTTCTGTACAGACGCGTGTACGCATGTAACATTATACTGAAAACCTTGCTTGAGAAGGTTTTGGGACGCTCGAAGGCTTTAATTTGC")
    design.presets.target((25, 150))
    res, explain = design.run()
    print("Results: ", json.dumps(res, indent=1))
    print("Explain: ", json.dumps(explain, indent=1))

.. testoutput::

    Results:  {}
    Explain:  {
     "PRIMER_LEFT_EXPLAIN": "considered 36, low tm 36, ok 0",
     "PRIMER_RIGHT_EXPLAIN": "considered 515, low tm 238, high tm 104, ok 173",
     "PRIMER_PAIR_EXPLAIN": "considered 0, ok 0",
     "PRIMER_LEFT_NUM_RETURNED": 0,
     "PRIMER_RIGHT_NUM_RETURNED": 0,
     "PRIMER_INTERNAL_NUM_RETURNED": 0,
     "PRIMER_PAIR_NUM_RETURNED": 0
    }

We can run the relaxation procedure using :meth:`run_and_optimize <primer3plus.Design.run_and_optimize>`:

.. testcode::

    design = Design()
    design.presets.template("TCATGTAATTAGTTATGTCACGCTTACATTCACGCCCTCCCCCCACATCCGCTCTAACCGAAAAGGAAGGAGTTAGACAACCTGAAGTCTAGGTCCCTATTTATTTTTTTATAGTTATGTTAGTATTAAGAACGTTATTTATATTTCAAATTTTTCTTTTTTTTCTGTACAGACGCGTGTACGCATGTAACATTATACTGAAAACCTTGCTTGAGAAGGTTTTGGGACGCTCGAAGGCTTTAATTTGC")
    design.presets.target((25, 150))
    design.presets.primer_num_return(1)
    res, explain = design.run_and_optimize(5)
    print("Gradient used: ", design.DEFAULT_GRADIENT)
    print("Results: ", json.dumps(res, indent=1))
    print("Explain: ", json.dumps(explain, indent=1))

.. testoutput::

    Gradient used:  {'PRIMER_MAX_SIZE': (1, 27, 36), 'PRIMER_MIN_SIZE': (-1, 16, 27), 'PRIMER_MAX_TM': (1, 27, 80), 'PRIMER_MIN_TM': (-1, 48, 57.0), 'PRIMER_MAX_HAIRPIN_TH': (1, 47.0, 60)}
    Results:  {
     "0": {
      "PAIR": {
       "PENALTY": 7.892226720976964,
       "COMPL_ANY_TH": 0.0,
       "COMPL_END_TH": 0.0,
       "PRODUCT_SIZE": 235
      },
      "LEFT": {
       "PENALTY": 7.713186819997588,
       "SEQUENCE": "TCATGTAATTAGTTATGTCACGCT",
       "location": [
        0,
        24
       ],
       "TM": 56.28681318000241,
       "GC_PERCENT": 33.333333333333336,
       "SELF_ANY_TH": 0.0,
       "SELF_END_TH": 0.0,
       "HAIRPIN_TH": 0.0,
       "END_STABILITY": 5.07
      },
      "RIGHT": {
       "PENALTY": 0.17903990097937594,
       "SEQUENCE": "TTCGAGCGTCCCAAAACCTT",
       "location": [
        234,
        20
       ],
       "TM": 60.179039900979376,
       "GC_PERCENT": 50.0,
       "SELF_ANY_TH": 0.0,
       "SELF_END_TH": 0.0,
       "HAIRPIN_TH": 0.0,
       "END_STABILITY": 3.5
      }
     }
    }
    Explain:  {
     "PRIMER_LEFT_EXPLAIN": "considered 45, low tm 43, ok 2",
     "PRIMER_RIGHT_EXPLAIN": "considered 618, GC content failed 1, low tm 250, high tm 99, ok 268",
     "PRIMER_PAIR_EXPLAIN": "considered 1, ok 1",
     "PRIMER_LEFT_NUM_RETURNED": 1,
     "PRIMER_RIGHT_NUM_RETURNED": 1,
     "PRIMER_INTERNAL_NUM_RETURNED": 0,
     "PRIMER_PAIR_NUM_RETURNED": 1
    }


Indexing with the primer3 results
---------------------------------

Note the adjustments that must be made to retrieve the correct slicing indices
for the RIGHT primer location:

.. testcode::

    from primer3plus.utils import reverse_complement

    design = Design()
    design.presets.template('TCATGTAATTAGTTATGTCACGCTTACATTCACGCCCTCCCCCCACATCCGCTCTAACCGAAAAGGAAGGAGTTAGACAACCTGAAGTCTAGGTCCCTATTTATTTTTTTATAGTTATGTTAGTATTAAGAACGTTATTTATATTTCAAATTTTTCTTTTTTTTCTGTACAGACGCGTGTACGCATGTAACATTATACTGAAAACCTTGCTTGAGAAGGTTTTGGGACGCTCGAAGGCTTTAATTTGC')
    design.presets.as_cloning_task()
    design.presets.primer_num_return(1)
    results, explain = design.run()
    result = results[0]

    lloc = result['LEFT']['location']
    lseq = result['LEFT']['SEQUENCE']
    rloc = result['RIGHT']['location']
    rseq = result['RIGHT']['SEQUENCE']

    print('LEFT')
    print(lseq)
    print(design.SEQUENCE_TEMPLATE.value[lloc[0]:lloc[0]+lloc[1]])
    print()
    print('RIGHT')
    print(rseq)
    print(reverse_complement(design.SEQUENCE_TEMPLATE.value[rloc[0]+1-rloc[1]:rloc[0]+1]))

.. testoutput::

    LEFT
    TCATGTAATTAGTTATGTCACGCTTAC
    TCATGTAATTAGTTATGTCACGCTTAC

    RIGHT
    GCAAATTAAAGCCTTCGAGCG
    GCAAATTAAAGCCTTCGAGCG