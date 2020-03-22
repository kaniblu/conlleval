__all__ = ["FormatError", "Statistics", "evaluate", "report"]

import io
import re

import collections


class FormatError(Exception):
    pass


class Statistics(object):

    def __init__(self):
        # counts by chunk type
        self.chunks_gold = collections.defaultdict(int)
        self.chunks_correct = collections.defaultdict(int)
        self.chunks_pred = collections.defaultdict(int)
        # counts by tag type
        self.tags_gold = collections.defaultdict(int)
        self.tags_correct = collections.defaultdict(int)
        self.tags_pred = collections.defaultdict(int)

    def slot_set(self):
        return (set(self.chunks_gold) | set(self.chunks_pred) |
                set(self.chunks_correct) | set(self.tags_gold) |
                set(self.tags_correct) | set(self.tags_pred))


def parse_tag(t):
    m = re.match(r'^([^-]*)-(.*)$', t)
    return m.groups() if m else (t, '')


def evaluate(lines, delimiter=None, boundary="-X-", otag="O"):
    """
    Python equivalent for the `conlleval.pl` Perl script, which was
    used for measuring slot filling performance in the CoNLL-2000 shared task.

    Arguments:
        lines (iterator-like object): an iterator-like object that returns
            one line of a `conlleval`-style prediction-target text file
            at a time.
        delimiter (str): the delimiting character used to split tokens in
            a line. (default: default python `str.split` behavior)
        boundary (str): the boundary string that is used to indicate an end of
            a sentence (default: -X-)
        otag (str): the tag for items that do not belong any slots.
            (default: O)

    Returns:
        a dictionary object that contains all information that used to be
        returned by the old `conlleval.pl` perl script.
    """
    stats = Statistics()
    num_features = None  # number of features per line
    in_correct = False  # currently processed chunks is correct until now
    last_correct = otag  # previous chunk tag in corpus
    last_correct_type = ''  # type of previously identified chunk tag
    last_guessed = otag  # previously identified chunk tag
    last_guessed_type = ''  # type of previous chunk tag in corpus

    for line in lines:
        if delimiter is None:
            features = line.split()
        else:
            features = line.split(delimiter)
        if num_features is None:
            num_features = len(features)
        elif num_features != len(features) and len(features) != 0:
            raise FormatError('unexpected number of features: %d (%d)' %
                              (len(features), num_features))
        if len(features) == 0 or features[0] == boundary:
            features = [boundary, otag, otag]
        if len(features) < 3:
            raise FormatError(
                'unexpected number of features in line %s' % line)
        guessed, guessed_type = parse_tag(features.pop())
        correct, correct_type = parse_tag(features.pop())
        first_item = features.pop(0)
        if first_item == boundary:
            guessed = otag
        end_correct = end_of_chunk(last_correct, correct,
                                   last_correct_type, correct_type, otag)
        end_guessed = end_of_chunk(last_guessed, guessed,
                                   last_guessed_type, guessed_type, otag)
        start_correct = start_of_chunk(last_correct, correct,
                                       last_correct_type, correct_type, otag)
        start_guessed = start_of_chunk(last_guessed, guessed,
                                       last_guessed_type, guessed_type, otag)
        if in_correct:
            if (end_correct and end_guessed and
                    last_guessed_type == last_correct_type):
                in_correct = False
                stats.chunks_correct[last_correct_type] += 1
            elif end_correct != end_guessed or guessed_type != correct_type:
                in_correct = False
        if start_correct and start_guessed and guessed_type == correct_type:
            in_correct = True
        if start_correct:
            stats.chunks_gold[correct_type] += 1
        if start_guessed:
            stats.chunks_pred[guessed_type] += 1
        if first_item != boundary:
            if correct == guessed and guessed_type == correct_type:
                stats.tags_correct[correct_type] += 1
            stats.tags_gold[correct_type] += 1
            stats.tags_pred[guessed_type] += 1
        last_guessed = guessed
        last_correct = correct
        last_guessed_type = guessed_type
        last_correct_type = correct_type
    if in_correct:
        stats.chunks_correct[last_correct_type] += 1
    return summarize_all(stats)


def summarize(correct, pred, gold):
    prec = 1 if pred == 0 else correct / pred
    rec = 0 if gold == 0 else correct / gold
    f1 = 0 if prec + rec == 0 else 2 * prec * rec / (prec + rec)
    return {
        "stats": {
            "gold": gold,
            "pred": pred,
            "correct": correct,
        },
        "evals": {"f1": f1, "prec": prec, "rec": rec}
    }


def summarize_all(s: Statistics):
    slot_set = s.slot_set() - {""}
    return {
        "overall": {
            "chunks": summarize(sum(s.chunks_correct.values()),
                                sum(s.chunks_pred.values()),
                                sum(s.chunks_gold.values())),
            "tags": summarize(sum(s.tags_correct.values()),
                              sum(s.tags_pred.values()),
                              sum(s.tags_gold.values()))
        },
        "slots": {
            "chunks": {
                slot: summarize(
                    s.chunks_correct.get(slot, 0),
                    s.chunks_pred.get(slot, 0),
                    s.chunks_gold.get(slot, 0)
                ) for slot in slot_set
            },
            "tags": {
                slot: summarize(
                    s.tags_correct.get(slot, 0),
                    s.tags_pred.get(slot, 0),
                    s.tags_gold.get(slot, 0)
                ) for slot in slot_set
            }
        }
    }


def end_of_chunk(prev_tag, tag, prev_type, type_, otag="O"):
    # check if a chunk ended between the previous and current word
    # arguments: previous and current chunk tags, previous and current types
    chunk_end = False

    if prev_tag == 'E':
        chunk_end = True
    if prev_tag == 'S':
        chunk_end = True

    if prev_tag == 'B' and tag == 'B':
        chunk_end = True
    if prev_tag == 'B' and tag == 'S':
        chunk_end = True
    if prev_tag == 'B' and tag == otag:
        chunk_end = True
    if prev_tag == 'I' and tag == 'B':
        chunk_end = True
    if prev_tag == 'I' and tag == 'S':
        chunk_end = True
    if prev_tag == 'I' and tag == otag:
        chunk_end = True

    if prev_tag != otag and prev_tag != '.' and prev_type != type_:
        chunk_end = True

    # these chunks are assumed to have length 1
    if prev_tag == ']':
        chunk_end = True
    if prev_tag == '[':
        chunk_end = True

    return chunk_end


def start_of_chunk(prev_tag, tag, prev_type, type_, otag):
    # check if a chunk started between the previous and current word
    # arguments: previous and current chunk tags, previous and current types
    chunk_start = False

    if tag == 'B':
        chunk_start = True
    if tag == 'S':
        chunk_start = True

    if prev_tag == 'E' and tag == 'E':
        chunk_start = True
    if prev_tag == 'E' and tag == 'I':
        chunk_start = True
    if prev_tag == 'S' and tag == 'E':
        chunk_start = True
    if prev_tag == 'S' and tag == 'I':
        chunk_start = True
    if prev_tag == otag and tag == 'E':
        chunk_start = True
    if prev_tag == otag and tag == 'I':
        chunk_start = True

    if tag != otag and tag != '.' and prev_type != type_:
        chunk_start = True

    # these chunks are assumed to have length 1
    if tag == '[':
        chunk_start = True
    if tag == ']':
        chunk_start = True

    return chunk_start


def report(summary):
    chunk_overall = summary["overall"]["chunks"]
    tag_overall = summary["overall"]["tags"]
    stats, evals = chunk_overall["stats"], chunk_overall["evals"]
    out = io.StringIO()
    out.write(f"processed {tag_overall['stats']['gold']} tokens "
              f"with {stats['gold']} phrases; ")
    out.write(f"found: {stats['pred']} phrases; "
              f"correct: {stats['correct']}.\n")
    acc = tag_overall['stats']['correct'] / tag_overall['stats']['gold']
    out.write(f"accuracy: {acc * 100:6.2f}%; ")
    out.write(f"precision: {evals['prec'] * 100:6.2f}%; ")
    out.write(f"recall: {evals['rec'] * 100:6.2f}%; ")
    out.write(f"FB1: {evals['f1'] * 100:6.2f}\n")
    items = sorted(summary["slots"]["chunks"].items(), key=lambda x: x[0])
    for slot, data in items:
        out.write(f"{slot:>17s}: ")
        out.write(f"precision: {data['evals']['prec'] * 100:6.2f}%; ")
        out.write(f"recall: {data['evals']['rec'] * 100:6.2f}%; ")
        out.write(f"FB1: {data['evals']['f1'] * 100:6.2f}  ")
        out.write(f"{data['stats']['pred']:d}\n")
    return out.getvalue()
