import argparse
import sys

from .conlleval import *


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


def stripr(iterable):
    for line in iterable:
        yield line.rstrip("\r\n")


def main():
    args = parse_args()
    input = sys.stdin
    output = sys.stdout
    if args.input is not None:
        input = open(args.input, "r")
    res = evaluate(
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
