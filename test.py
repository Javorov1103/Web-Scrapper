import os

files= os.listdir('./Product links csvs')

for file in files:
    print(file.replace('.csv',''))
    
print(files)