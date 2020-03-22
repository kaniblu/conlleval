# conlleval

This is a pure python port of the perl evaluation script for the CoNLL-2000 
shard task. Supports both IOB2 and IOBES formats.

## Getting Started ##

Either get this package through PyPI (`pip install conlleval`) or install
it from this repository after cloning it (`python setup.py install`).

You can run this package directly:

```
python -m conlleval tests/cases/input-001.txt
```

or import it as a library:

```python
>>> import conlleval
>>> lines = """Rockwell NNP B-NP I-NP
International NNP I-NP I-NP
Corp. NNP I-NP I-NP
's POS B-NP B-NP
Tulsa NNP I-NP I-NP
unit NN I-NP I-NP
said VBD B-VP B-VP
it PRP B-NP B-NP
signed VBD B-VP B-VP
a DT B-NP B-NP
tentative JJ I-NP I-NP
agreement NN I-NP I-NP
extending VBG B-VP B-VP
its PRP$ B-NP B-NP
contract NN I-NP I-NP
with IN B-PP B-PP
Boeing NNP B-NP I-NP
Co. NNP I-NP I-NP
to TO B-VP B-PP
provide VB I-VP I-VP
structural JJ B-NP I-NP
parts NNS I-NP I-NP
for IN B-PP B-PP
Boeing NNP B-NP I-NP
's POS B-NP B-NP
747 CD I-NP I-NP
jetliners NNS I-NP I-NP
. . O O
""".splitlines()
>>> res = conlleval.evaluate(lines)
>>> import pprint
>>> pprint.pprint(res)
{'overall': {'chunks': {'evals': {'f1': 0.9032258064516129,
                                  'prec': 0.875,
                                  'rec': 0.9333333333333333},
                        'stats': {'correct': 14, 'gold': 15, 'pred': 16}},
             'tags': {'evals': {'f1': 0.8214285714285714,
                                'prec': 0.8214285714285714,
                                'rec': 0.8214285714285714},
                      'stats': {'correct': 23, 'gold': 28, 'pred': 28}}},
 'slots': {'chunks': {'NP': {'evals': {'f1': 1.0, 'prec': 1.0, 'rec': 1.0},
                             'stats': {'correct': 9, 'gold': 9, 'pred': 9}},
                      'PP': {'evals': {'f1': 0.8,
                                       'prec': 0.6666666666666666,
                                       'rec': 1.0},
                             'stats': {'correct': 2, 'gold': 2, 'pred': 3}},
                      'VP': {'evals': {'f1': 0.75, 'prec': 0.75, 'rec': 0.75},
                             'stats': {'correct': 3, 'gold': 4, 'pred': 4}}},
           'tags': {'NP': {'evals': {'f1': 0.8000000000000002,
                                     'prec': 0.8,
                                     'rec': 0.8},
                           'stats': {'correct': 16, 'gold': 20, 'pred': 20}},
                    'PP': {'evals': {'f1': 0.8,
                                     'prec': 0.6666666666666666,
                                     'rec': 1.0},
                           'stats': {'correct': 2, 'gold': 2, 'pred': 3}},
                    'VP': {'evals': {'f1': 0.888888888888889,
                                     'prec': 1.0,
                                     'rec': 0.8},
                           'stats': {'correct': 4, 'gold': 5, 'pred': 4}}}}}
>>> print(conlleval.report(res))
processed 28 tokens with 15 phrases; found: 16 phrases; correct: 14.
accuracy:  82.14%; precision:  87.50%; recall:  93.33%; FB1:  90.32
               NP: precision: 100.00%; recall: 100.00%; FB1: 100.00  9
               PP: precision:  66.67%; recall: 100.00%; FB1:  80.00  3
               VP: precision:  75.00%; recall:  75.00%; FB1:  75.00  4
```

**Breaking Changes in v0.2**

* Now `evaluate` function returns evaluation results for chunks (consecutive tags of identical types) and tags separately. In the previous version, the distinction wasn't clear, causing confusion regarding the counts shown in `['overall']['stats']['all']` specifically.

## Notes ##

* The original perl script is not available at the official website anymore. 
You can access it [here](https://github.com/robertostling/efselab/blob/master/3rdparty/conlleval.perl)
instead.
* Latex format is not supported yet. (Any contribution is welcomed)
