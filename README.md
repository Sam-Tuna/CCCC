# CCCC
Contig Classification Coverage Calculator

CCCC is an utility script that receives a mpa format contig classification file and an ```samtools idxstats``` output file and outputs a tab separated file with the classifications and their relative percentage according to contig coverage in the kingdom, phylum and genus level.

## Flags:
```
'--classes', '-c': mpa style classifications file
'--mapstats', '-s': samtools idxstats output of the alignment file between the reads and the metagenome assembly that was classified
'--suffix', '-u': suffix in output files name, for identification
```
