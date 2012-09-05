from pySar.lib import sar
from json import dumps
import argparse

def run(reporttype=None, pretty=False):
    'Gets sar output from pySar as JSON output'
    results = sar(sarbin='sar', saroptions=reporttype)
    if pretty:
        data = dumps(results, indent = 4)
    else:
        data = dumps(results)
    return data

def main():
    'Main function'
    reports = {'memory': '-r', 'cpu': '', 'swap': '-S', 'load': '-q'}

    parser = argparse.ArgumentParser()
    parser.add_argument('--pretty', action="store_true", dest="pretty",
                    default=False,
                    help='Print json output in human readable form.')
    parser.add_argument('reporttype', 
                    metavar='sysstat report type to pull. %s' % \
                    sorted(reports.keys()), type=str)
    args = parser.parse_args()

    if args.reporttype in reports.keys():
        print run(pretty=args.pretty, reporttype=reports[args.reporttype])
    else:
        raise Exception('Invalid Report type, the types are %s' % reports.keys())

if __name__ == "__main__":
    main()