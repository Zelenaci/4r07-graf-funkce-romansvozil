#!/usr/bin/env python

#Tento progam prepise neprehledna data do lehce zpracovatelnzch json
import json

txt = input('Jmeno .txt: ')
with open('{0}.txt'.format(txt)) as file:
    new_file = []
    for radek in file:
        new_file.append([])
        radek = radek.split()
        for slovo in radek:
            new_file[len(new_file) - 1].append(slovo)

with open('{0}JSON.txt'.format(txt), 'w+') as outfile:
    json.dump(new_file, outfile, indent=4)

print('Hotovo.. ')
