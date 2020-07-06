import re
import subprocess
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from typing import List, Optional

from coverage import Coverage
from coverage.misc import CoverageException


def get_changed_files(branch1: str, branch2: str, diff_filter: str, include_regexp: str) -> List[str]:
    """Get changed files by specified diff types and filter with regexp."""
    r = subprocess.run(
        f'git diff "{branch1}" "{branch2}" --name-only -b -M -C --diff-filter="{diff_filter}"',
        shell=True,
        capture_output=True,
    )
    if r.stderr:
        print(r.stderr.decode())
        exit(1)
    files = r.stdout.decode().splitlines()
    files = filter(lambda name: re.search(include_regexp, name), files)
    return list(files)


def show_coverage(
    cov: Coverage, 
    changed_files: Optional[bool] = None, 
    show_missing: Optional[bool] = None, 
    fail_under: Optional[int] = None,
) -> bool:
    """Print coverage for specified files"""
    try:
        coverage_value = cov.report(include=changed_files, show_missing=show_missing)
    except CoverageException as e:
        if 'No data to report.' in e.args:
            print(e)
            return True
        else:
            raise
    minimum_coverage = fail_under if fail_under is not None else cov.config.fail_under
    return coverage_value >= minimum_coverage


def read_args():
    parser = ArgumentParser(
        description='Show coverage only for changed files',
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('branch1', nargs='?', default='HEAD', help='first branch for git diff')
    parser.add_argument('branch2', nargs='?', default='origin/master', help='second branch for git diff')
    parser.add_argument('--diff-filter', default='dr', metavar='DIFFS', help="diff types for include files for coverage (more info at git diff's --diff-filter option)")
    parser.add_argument('--include-regexp', default='\\.py$', metavar='REGEXP', help='filter changed files by regexp')
    parser.add_argument('--full-branches', default='master', metavar='BRANCH', help='show full coverage for specified branches (delimited by comma)')
    parser.add_argument('--show-missing', '-m', action='store_true', help='show missed lines for changed files')
    parser.add_argument('--show-missing-full', '-mf', action='store_true', help='show missed lines for --full-branches')
    parser.add_argument('--fail-under', '-f', type=int, metavar='PERCENT', help='override minimum coverage percent (0 - disabled)')
    parser.add_argument('--current-branch', '-c', metavar='BRANCH', help='current branch name from CI (used for compare with --full-branches); if missed - will be used branch1')
    args = parser.parse_args()
    args.full_branches = args.full_branches.split(',')
    return args


def exit_with_status(passed: bool) -> None:
    if passed:
        exit(0)
    exit(1)


def main():
    args = read_args()

    cov = Coverage()
    cov.load()

    if (args.current_branch or args.branch1) in args.full_branches:
        passed = show_coverage(cov, show_missing=args.show_missing_full, fail_under=args.fail_under)
        exit_with_status(passed)

    changed_files = get_changed_files(args.branch1, args.branch2, args.diff_filter, args.include_regexp)
    if changed_files:
        passed = show_coverage(cov, changed_files, show_missing=args.show_missing, fail_under=args.fail_under)
        exit_with_status(passed)

    print('No changes.')


if __name__ == '__main__':
    main()
