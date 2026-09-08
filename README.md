# clipper
This tool quickly removes any softclips from a nanopore bam. This is convienient for any adaptors , ligation products, etc. 

NOTE: Not recommended in cases where structural events matter (fusions | insertions | deletions | etc) adaptors should usually also be removed before alignment*. 

<p align="center">
  <img src="/clipper.jpeg" width="500">
</p>


usage: clipper [-h] -i INPUT -o OUTPUT

Remove terminal soft-clipped portions from BAM reads

options:

  -h, --help           show this help message and exit
  -i, --input INPUT    Input BAM file
  -o, --output OUTPUT  Output BAM file
