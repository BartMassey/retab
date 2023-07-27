#!/usr/bin/python3
# Copyright © 2016 Bart Massey
# Substitute hard tabs for strings of spaces.

import argparse
from sys import stdin, stdout, stderr
from pathlib import Path

parser = argparse.ArgumentParser()
program = parser.prog
required = program not in ("entab", "detab")
# https://stackoverflow.com/q/7869345/364875
group = parser.add_mutually_exclusive_group(required=required)
group.add_argument("--entab", action='store_true')
group.add_argument("--detab", action='store_true')

parser.add_argument('path', nargs='?')
parser.add_argument('-e', '--edit-file', action='store_true')
parser.add_argument('--edit-dir')
parser.add_argument('-4', '--four-space', action='store_true')
parser.add_argument('--full', action='store_true')
args = parser.parse_args()

if args.entab:
    program = "entab"
if args.detab:
    program = "detab"

tabwidth = 8
if args.four_space:
    tabwidth = 4

def detab_line(line):
    result = ""
    p = 0
    for i in range(len(line)):
        if line[i] == '\t':
            m = tabwidth - (p % tabwidth)
            result += ' '*m
            p += m
            continue
        result += line[i]
        p += 1
    return result

def entab_line(line):
    result = ""
    for i in range(0, len(line), tabwidth):
        segment = line[i:i+tabwidth]
        if segment == ' '*tabwidth:
            result += '\t'
            continue
        if args.full and len(segment) == tabwidth:
            for j in range(tabwidth - 1, 0, -1):
                if segment[j] != ' ':
                    break
            if j <= tabwidth / 2:
                result += segment[:j+1]
                result += '\t'
                continue
        result += segment
    return result

if program == "detab":
    if args.full:
        print("detab: --full not allowed", file=stderr)
        exit(1)
    tabf = detab_line
elif program == "entab":
    tabf = entab_line
else:
    print("usage: [entab|detab]", file=stderr)
    exit(1)

def convert(tabf, source):
    source_text = source.read().splitlines()
    dest_text = map(tabf, source_text)
    return '\n'.join(dest_text)

def convert_path(file_path=None, edit=False):
    global tabf
    if file_path:
        source = open(file_path, "r")
    else:
        source = stdin
    dest_text = convert(tabf, source)
    if edit:
        assert file_path
        source.close()
        dest = open(file_path, "w")
        print(dest_text, file=dest)
    else:
        print(dest_text)

if args.edit_dir:
    if not args.path:
        print("--edit-dir requires root directory path", file=stderr)
        exit(1)
    path=Path(args.path)
    glob = args.edit_dir

    edited = False
    for p in path.glob(glob):
        convert_path(file_path=p, edit=True)
        edited = True
    if not edited:
        print("warning: no edits", file=stderr)
elif args.edit_file:
    if not args.path:
        print("-e requires file path", file=stderr)
        exit(1)
    path = Path(args.path)
    if path.is_dir():
        print("must use --edit-dir for directory", file=stderr)
        exit(1)
    convert_path(file_path=path, edit=True)
else:
    convert_path(file_path=args.path)
