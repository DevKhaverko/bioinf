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
`pip install prefect`
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

@flow
def parse():
    f = open(sys.argv[1], "r")
    lines = f.readlines()
    for line in lines:
        if re.match("[0-9]+ \+ [0-9]+ mapped", line.strip()):
            percent = get_percent(line)
            ok_or_not(percent)

def main():
    parse()

		
    

if __name__ == "__main__":
    main()
```
```
18:44:06.402 | INFO    | prefect.engine - Created flow run 'pygmy-snail' for flow 'parse'
18:44:06.485 | INFO    | Flow run 'pygmy-snail' - Created task run 'get_percent-0' for task 'get_percent'
18:44:06.485 | INFO    | Flow run 'pygmy-snail' - Executing 'get_percent-0' immediately...
18:44:06.532 | INFO    | Task run 'get_percent-0' - Finished in state Completed()
18:44:06.545 | INFO    | Flow run 'pygmy-snail' - Created task run 'ok_or_not-0' for task 'ok_or_not'
18:44:06.546 | INFO    | Flow run 'pygmy-snail' - Executing 'ok_or_not-0' immediately...
Not OK
18:44:06.593 | INFO    | Task run 'ok_or_not-0' - Finished in state Completed()
18:44:06.611 | INFO    | Flow run 'pygmy-snail' - Finished in state Completed('All states completed.')
 ~/Desktop/NSU/ python3 script2.py res_samtools
18:44:18.683 | INFO    | prefect.engine - Created flow run 'premium-boobook' for flow 'parse'
18:44:18.765 | INFO    | Flow run 'premium-boobook' - Created task run 'get_percent-0' for task 'get_percent'
18:44:18.766 | INFO    | Flow run 'premium-boobook' - Executing 'get_percent-0' immediately...
18:44:18.814 | INFO    | Task run 'get_percent-0' - Finished in state Completed()
18:44:18.827 | INFO    | Flow run 'premium-boobook' - Created task run 'ok_or_not-0' for task 'ok_or_not'
18:44:18.828 | INFO    | Flow run 'premium-boobook' - Executing 'ok_or_not-0' immediately...
OK
18:44:18.876 | INFO    | Task run 'ok_or_not-0' - Finished in state Completed()
18:44:18.894 | INFO    | Flow run 'premium-boobook' - Finished in state Completed('All states completed.')
```
