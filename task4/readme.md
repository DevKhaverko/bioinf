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
5. Установка prefect
```
pip install prefect
prefect server start
```
6. Hello world
```
from prefect import flow

@flow
def my_favorite_function():
    print("Hello world")

my_favorite_function()
```
```
18:45:22.146 | INFO    | prefect.engine - Created flow run 'pragmatic-barracuda' for flow 'my-favorite-function'
Hello world
18:45:22.235 | INFO    | Flow run 'pragmatic-barracuda' - Finished in state Completed()
```
7. Пайплайн парсинга файла
```
import sys
import re
from prefect import task, flow
import subprocess
@task
def get_percent(line):
    t = line.split(" ")[4][1:][:-1]
    return float(t)

@task
def ok_or_not(percent):
    if percent < 90:
        print("Not OK")
    else:
        print("OK")

@task(name="index.mmi")
def get_index():
    p = subprocess.Popen("./minimap2/minimap2 -d index.mmi GCF_000005845.2_ASM584v2_genomic.fna", shell=True)
    p.wait()
    return "index.mmi"

@task(name="res.sam")
def create_sam(index_file):
    p = subprocess.Popen(str.format("./minimap2/minimap2 -a {0} GCF_000005845.2_ASM584v2_genomic.fna > res.sam", index_file), shell=True)
    p.wait()
    return "res.sam"

@task(name="flagstat")
def flagstat(sam_file):
    p = subprocess.Popen(str.format("./bin/samtools flagstat {0} > res_samtools", sam_file), shell=True)
    p.wait()

@flow(name="оценка качества")
def estiamte():
    index_file = get_index()
    sam_file = create_sam(index_file)
    flagstat(sam_file)
    f = open("res_samtools", "r")
    lines = f.readlines()
    for line in lines:
        if re.match("[0-9]+ \+ [0-9]+ mapped", line.strip()):
            percent = get_percent(line)
            ok_or_not(percent)

def main():
    estiamte()

		
    

if __name__ == "__main__":
    main()
```
```
19:32:49.988 | INFO    | prefect.engine - Created flow run 'impartial-scorpion' for flow 'оценка качества'
19:32:50.063 | INFO    | Flow run 'impartial-scorpion' - Created task run 'index.mmi-0' for task 'index.mmi'
19:32:50.063 | INFO    | Flow run 'impartial-scorpion' - Executing 'index.mmi-0' immediately...
[M::mm_idx_gen::0.093*1.03] collected minimizers
[M::mm_idx_gen::0.111*1.35] sorted minimizers
[M::main::0.172*1.19] loaded/built the index for 1 target sequence(s)
[M::mm_idx_stat] kmer size: 15; skip: 10; is_hpc: 0; #seq: 1
[M::mm_idx_stat::0.180*1.18] distinct minimizers: 838542 (98.18% are singletons); average occurrences: 1.034; average spacing: 5.352; total length: 4641652
[M::main] Version: 2.26-r1175
[M::main] CMD: ./minimap2/minimap2 -d index.mmi GCF_000005845.2_ASM584v2_genomic.fna
[M::main] Real time: 0.188 sec; CPU: 0.220 sec; Peak RSS: 0.075 GB
19:32:50.316 | INFO    | Task run 'index.mmi-0' - Finished in state Completed()
19:32:50.330 | INFO    | Flow run 'impartial-scorpion' - Created task run 'res.sam-0' for task 'res.sam'
19:32:50.330 | INFO    | Flow run 'impartial-scorpion' - Executing 'res.sam-0' immediately...
[M::main::0.048*1.02] loaded/built the index for 1 target sequence(s)
[M::mm_mapopt_update::0.058*1.02] mid_occ = 12
[M::mm_idx_stat] kmer size: 15; skip: 10; is_hpc: 0; #seq: 1
[M::mm_idx_stat::0.065*1.02] distinct minimizers: 838542 (98.18% are singletons); average occurrences: 1.034; average spacing: 5.352; total length: 4641652
[M::worker_pipeline::1.620*1.00] mapped 1 sequences
[M::main] Version: 2.26-r1175
[M::main] CMD: ./minimap2/minimap2 -a index.mmi GCF_000005845.2_ASM584v2_genomic.fna
[M::main] Real time: 1.626 sec; CPU: 1.626 sec; Peak RSS: 0.115 GB
19:32:52.016 | INFO    | Task run 'res.sam-0' - Finished in state Completed()
19:32:52.031 | INFO    | Flow run 'impartial-scorpion' - Created task run 'flagstat-0' for task 'flagstat'
19:32:52.031 | INFO    | Flow run 'impartial-scorpion' - Executing 'flagstat-0' immediately...
19:32:52.094 | INFO    | Task run 'flagstat-0' - Finished in state Completed()
19:32:52.107 | INFO    | Flow run 'impartial-scorpion' - Created task run 'get_percent-0' for task 'get_percent'
19:32:52.107 | INFO    | Flow run 'impartial-scorpion' - Executing 'get_percent-0' immediately...
19:32:52.150 | INFO    | Task run 'get_percent-0' - Finished in state Completed()
19:32:52.163 | INFO    | Flow run 'impartial-scorpion' - Created task run 'ok_or_not-0' for task 'ok_or_not'
19:32:52.164 | INFO    | Flow run 'impartial-scorpion' - Executing 'ok_or_not-0' immediately...
OK
19:32:52.206 | INFO    | Task run 'ok_or_not-0' - Finished in state Completed()
19:32:52.224 | INFO    | Flow run 'impartial-scorpion' - Finished in state Completed('All states completed.')
```
8. Как таковой у меня получилось такая же зависимость между файлами