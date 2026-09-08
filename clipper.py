#!/usr/bin/env python3

import pysam
import argparse

parser = argparse.ArgumentParser(
    description="Remove terminal soft-clipped portions from BAM reads"
)

parser.add_argument("-i", "--input", required=True, help="Input BAM file")
parser.add_argument("-o", "--output", required=True, help="Output BAM file")

args = parser.parse_args()

in_bam = pysam.AlignmentFile(args.input, "rb")
out_bam = pysam.AlignmentFile(args.output, "wb", template=in_bam)


def trim_softclips(read):
    if not read.cigartuples:
        return read

    seq = read.query_sequence
    qual = read.query_qualities
    cig = read.cigartuples

    # If the BAM has no sequence for this read, we cannot trim it
    if seq is None:
        return read

    # trim left soft clip
    if cig[0][0] == 4:
        clip_len = cig[0][1]
        seq = seq[clip_len:]

        if qual is not None:
            qual = qual[clip_len:]

        cig = cig[1:]

    # trim right soft clip
    if cig and cig[-1][0] == 4:
        clip_len = cig[-1][1]
        seq = seq[:-clip_len]

        if qual is not None:
            qual = qual[:-clip_len]

        cig = cig[:-1]

    read.query_sequence = seq
    read.query_qualities = qual
    read.cigartuples = cig

    return read


for read in in_bam:

    if read.is_unmapped:
        out_bam.write(read)
        continue

    try:
        read = trim_softclips(read)
        out_bam.write(read)

    except Exception as e:
        print(f"ERROR processing {read.query_name}: {e}")
        raise


in_bam.close()
out_bam.close()
