### Coverage-diff

Show / check coverage only for changed files

### Example

Show coverage for all changed files (except deleted & renamed) 
between current branch and master with numbers of missing lines.

```sh
coverage-diff HEAD master --show-missing
```

### Options

```
usage: main.py [-h] [--diff-filter DIFFS] [--include-regexp REGEXP]
               [--full-branches BRANCH] [--show-missing] [--show-missing-full]
               [branch1] [branch2]

Show coverage only for changed files

positional arguments:
  branch1               first branch for git diff (default: HEAD)
  branch2               second branch for git diff (default: origin/master)

optional arguments:
  -h, --help            show this help message and exit
  --diff-filter DIFFS   diff types for include files for coverage (more info
                        at git diff's --diff-filter option) (default: dr)
  --include-regexp REGEXP
                        filter changed files by regexp (default: \.py$)
  --full-branches BRANCH
                        show full coverage for specified branches (delimited
                        by comma) (default: master)
  --show-missing, -m    show missed lines for changed files (default: False)
  --show-missing-full, -mf
                        show missed lines for --full-branches (default: False)
  --fail-under PERCENT, -f PERCENT
                        override minimum coverage percent (0 - disabled)
                        (default: None)
```
