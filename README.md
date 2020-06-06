# Diffusor
[![CircleCI](https://circleci.com/gh/kobaltcore/diffusor.svg?style=svg)](https://circleci.com/gh/kobaltcore/diffusor)
[![Downloads](https://pepy.tech/badge/diffusor)](https://pepy.tech/project/diffusor)

A pure-python diffing utility using Google's [diff-match-patch](https://github.com/google/diff-match-patch).

This is a utility script for a very specific purpose, namely easy generation and application of diffs for Python-centric projects, programmatically from within Python.

This tool serves exactly two functions:
1. Create diffs between two versions of the same file
2. Apply diffs to a file

It works on a per-file basis.

If you don't have a specific use case for this, you're probably better off using Git diffs and the ubiquitous Linux `patch` tool. Diffusor exists specifically for easing the patch-apply workflow within Python programs, nothing more, nothing less.

## Installation
Diffusor can be installed via pip:
```bash
$ pip install diffusor
```

Please note that Diffusor requires Python 3 and will not provide backwards compatibility for Python 2 for the foreseeable future.

## Usage
To create a diff:
```bash
diffusor diff <source_file> <modified_file> -n <target_file>
```

To apply a diff:
```bash
diffusor apply <patch_file> -t <target_file>
```

### Command Line Interface
```
Usage: diffusor.py [OPTIONS] COMMAND [ARGS]...

  A pure-python diffing utility using Google's diff-match-patch.

  This tool serves exactly two functions:
  1. Create diffs between two versions of the same file
  2. Apply diffs to a file

  Commands can be abbreviated by the shortest unique string.

  For example:
      diff -> d
      apply -> a

  Examples of full commands:
      diffusor diff <source_file> <modified_file> -n <target_file>
      diffusor apply <patch_file> -t <target_file>

Options:
  -d, --debug / -nd, --no-debug  Print debug information or only regular
                                 output

  --help                         Show this message and exit.

Commands:
  apply
  diff
```
