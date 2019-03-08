# conlleval

Another python port of the perl evaluation script for the CoNLL-2000 shard 
task.

## Getting Started ##

Either get this package through PyPI (`pip install conlleval`) or install
from this repository (`python setup.py install`).

You can call this package directly to run as a script:

```
python -m conlleval tests/cases/input-001.txt
```

Or, you can use this package as a library:

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
"""
>>> res = conlleval.evaluate(lines.splitlines())
>>> import pprint
>>> pprint.pprint(res)
{'overall': {'evals': {'f1': 0.9032258064516129,
                       'prec': 0.875,
                       'rec': 0.9333333333333333},
             'stats': {'all': 28, 'correct': 14, 'gold': 15, 'pred': 16}},
 'slots': {'NP': {'evals': {'f1': 1.0, 'prec': 1.0, 'rec': 1.0},
                  'stats': {'correct': 9, 'gold': 9, 'pred': 9}},
           'PP': {'evals': {'f1': 0.8, 'prec': 0.6666666666666666, 'rec': 1.0},
                  'stats': {'correct': 2, 'gold': 2, 'pred': 3}},
           'VP': {'evals': {'f1': 0.75, 'prec': 0.75, 'rec': 0.75},
                  'stats': {'correct': 3, 'gold': 4, 'pred': 4}}}}
```

## Notes ##

* The original perl script is not available at the official website anymore. 
You can access it [here](https://github.com/robertostling/efselab/blob/master/3rdparty/conlleval.perl)
instead.

* Latex format is not supported yet. (Any contribution is welcome)

