1. https://trace.ncbi.nlm.nih.gov/Traces/?view=run_browser&acc=SRR24650906&display=download
2. Установка, использование minimap2, samtools
```
инструкция по установке samtools
http://www.htslib.org/download/
```
```
git clone repo_url minimap2
cd minimap2
make arm_neon=1 aarch64=1 // собирал под арм
```
```
./minimap2 -d ../index.mmi GCF_000005845.2_ASM584v2_genomic.fna // -d выходной файл индекса
./minimap2 -a ../index.mmi GCF_000005845.2_ASM584v2_genomic.fna > ../res.sam // -a файл индекса, *.sam выходной файл для samtools
```
3. Результат samtools flagstat
```
1 + 0 in total (QC-passed reads + QC-failed reads)
1 + 0 primary
0 + 0 secondary
0 + 0 supplementary
0 + 0 duplicates
0 + 0 primary duplicates
1 + 0 mapped (100.00% : N/A)
1 + 0 primary mapped (100.00% : N/A)
0 + 0 paired in sequencing
0 + 0 read1
0 + 0 read2
0 + 0 properly paired (N/A : N/A)
0 + 0 with itself and mate mapped
0 + 0 singletons (N/A : N/A)
0 + 0 with mate mapped to a different chr
0 + 0 with mate mapped to a different chr (mapQ>=5)
```
4. Скрипт для получения процента(путь до файла передается аргументом), скрипт для оценки
```
#!/bin/bash
grep -E "[0-9]+ \+ [0-9]+ mapped" $1 | cut -d " " -f 5 | sed 's/^.//;s/.$//' | cut -d "." -f 1
```
```
#!/bin/bash
percent=$(grep -E "[0-9]+ \+ [0-9]+ mapped" $1 | cut -d " " -f 5 | sed 's/^.//;s/.$//' | cut -d "." -f 1)
if [[ "$percent" -lt "90" ]]; then
	echo "Not ok"
else
	echo "OK"
fi
```
