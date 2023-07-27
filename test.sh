#!/bin/sh
TMPDIR="/tmp/retab-test-$$"

mkdir "$TMPDIR"
echo "	x" >"$TMPDIR"/1.x
echo "	y" >"$TMPDIR"/1.y
echo "        x" >"$TMPDIR"/2.x
mkdir "$TMPDIR"/sub
echo "	x	y" >"$TMPDIR"/sub/3.x

python3 ./retab.py --detab -4 --edit-dir '**/*.x' "$TMPDIR"
if [ "`cat "$TMPDIR"/1.x`" != "    x" ]
then
    echo "$TMPDIR:test 1.x failed" >&2
    exit 1
fi
if [ "`cat "$TMPDIR"/1.y`" != "	y" ]
then
    echo "$TMPDIR:test 1.y failed" >&2
    exit 1
fi
if [ "        x"  != "`cat $TMPDIR/2.x`" ]
then
    echo "$TMPDIR:test 2.x failed" >&2
    exit 1
fi
if [ "    x	y" != "`cat $TMPDIR/sub/3.x`" ]
then
    echo "$TMPDIR:test 3.x failed" >&2
    exit 1
fi

rm -rf $TMPDIR
