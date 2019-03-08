import io
import argparse
import sys
import re
import collections

from . import conlleval


def parse_args():
    parser = argparse.ArgumentParser(
        description="evaluate tagging results using CoNLL criteria",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-b", "--boundary", default="-X-",
                        help="sentence boundary")
    parser.add_argument("-d", "--delimiter",
                        help="character delimiting items in input")
    parser.add_argument("-o", "--otag", default="O",
                        help="alternative outside tag")
    parser.add_argument("-O", "--output",
                        help="output file path")
    parser.add_argument("-f", "--output-format", default="conlleval",
                        help="output format",
                        choices=["yaml", "json", "conlleval"])
    parser.add_argument("input")
    return parser.parse_args()


def report(summary):
    overall = summary["overall"]
    stats, evals = overall["stats"], overall["evals"]
    out = io.StringIO()
    out.write(f"processed {stats['all']} tokens "
              f"with {stats['gold']} phrases; ")
    out.write(f"found: {stats['pred']} phrases; "
              f"correct: {stats['correct']}.\n")

    if not stats['all']:
        return out.getvalue()

    acc = stats['correct'] / stats['all']
    out.write(f"accuracy: {acc * 100:6.2f}%; ")
    out.write(f"precision: {evals['prec'] * 100:6.2f}%; ")
    out.write(f"recall: {evals['rec'] * 100:6.2f}%; ")
    out.write(f"FB1: {evals['f1'] * 100:6.2f}\n")

    items = sorted(summary["slots"].items(), key=lambda x: x[0])
    for slot, data in items:
        out.write(f"{slot:>17s}: ")
        out.write(f"precision: {data['evals']['prec'] * 100:6.2f}%; ")
        out.write(f"recall: {data['evals']['rec'] * 100:6.2f}%; ")
        out.write(f"FB1: {data['evals']['f1'] * 100:6.2f}  ")
        out.write(f"{data['stats']['pred']:d}\n")

    return out.getvalue()


def stripr(iterable):
    for line in iterable:
        yield line.rstrip("\r\n")


def main():
    args = parse_args()
    input = sys.stdin
    output = sys.stdout
    if args.input is not None:
        input = open(args.input, "r")
    res = conlleval.evaluate(
        lines=stripr(input),
        boundary=args.boundary,
        delimiter=args.delimiter,
        otag=args.otag
    )
    if args.input is not None:
        input.close()
    if args.output is not None:
        output = open(args.output, "w")
    if args.output_format == "json":
        import json
        fmt = json.dumps(res, indent=2, ensure_ascii=False)
    elif args.output_format == "yaml":
        try:
            import yaml
        except ImportError:
            raise ImportError(f"`yaml` module not found. Try installing it by "
                              f"running `pip install pyyaml`")
        fmt = yaml.dump(
            res,
            allow_unicode=True,
            indent=2,
            default_flow_style=False
        )
    elif args.output_format == "conlleval":
        fmt = report(res)
    else:
        raise ValueError(f"unrecognized format type: {args.output_format}")
    output.write(fmt)
    if args.output is not None:
        output.close()


if __name__ == '__main__':
    main()
