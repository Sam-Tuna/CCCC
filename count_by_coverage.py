import pandas as pd
import click
@click.command()
@click.option('--classes', '-c', required=True, help='file with contig names and classifications', type=click.Path(exists=True))
@click.option('--mapstats', '-s', required=True, help='samtools idxstats output', type=click.Path(exists=True))
@click.option('--suffix', '-u', required=True, help='suffix of output files', default="", type=str)
#classes="sorted_classes.tsv"
#mapstats="mapped_stats.txt"
#print(kaiju_file)

def main (classes, mapstats, suffix):
#get names from file
    with open (classes) as kaijin:
        classifications = kaijin.readlines()
    kaijin.close
    #parse the alignment stats
    stats=pd.read_csv(mapstats, sep="\t", header=None)
    #create dictionaries for genera and phyla
    gen={}
    phy={}
    kin={}
    #print(stats.loc[stats[0] == 'contig_10'])

    #for each entry in the classification file, find the contig coverage and add it to the taxa dictionary
    for j in classifications:
        classplit=j.split('\t')
        if (len(classplit[1])>1):
            count=stats.loc[stats[0] == classplit[0]]
    #        print(count)
            if (count.empty==False):
                tkingdom=classplit[1].split(';')[0]
#                print (len(tkingdom))
#if it's already in the dictionary add to the value there, else create the key and input the value
                if (tkingdom in kin):
#                    print('aqui: '+tkingdom)
                    k=int(kin[tkingdom])
                    k+=int(count[2].iloc[0])
                    kin[tkingdom]=k
                else:
                    kin[tkingdom]=int(count[2].iloc[0])
            if (count.empty==False):
                tphylum=classplit[1].split(';')[1]
                #if it's already in the dictionary add to the value there, else create the key and input the value
                if (tphylum in phy): #and len(count)>=3):
                    k=int(phy[tphylum])
                    k+=int(count[2].iloc[0])
                    phy[tphylum]=k
                else:
                    phy[tphylum]=int(count[2].iloc[0])
                #same thing but for genera
                tgenus=classplit[1].split(';')[5]
                if (tgenus in gen): # and len(count)>=3):
                    k=int(gen[tgenus])
                    k+=int(count[2].iloc[0])
                    gen[tgenus]=k
                else:
                    gen[tgenus]=int(count[2].iloc[0])
 #           print(classplit[1].split(';')[0])
    #remove NAs from the dicts
    kin.pop('unassigned', None)
    phy.pop('unassigned', None)
    gen.pop('unassigned', None)
    print(phy)
#    print(gen['Pseudomonas'])
#    print(int(stats.loc[stats[0]=='contig_5311'][1]))
#    print(int(stats.loc[stats[0]=='contig_10'][1]))

    #convert the dictionaries to dataframes and sort them

    ki=pd.DataFrame.from_dict(kin, orient='index', columns=['coverage'])
    ki=ki.sort_values(by='coverage', ascending=False)
    print(ki)
    p=pd.DataFrame.from_dict(phy, orient='index', columns=['coverage'])
    p=p.sort_values(by='coverage', ascending=False)
    print(p)
    g=pd.DataFrame.from_dict(gen, orient='index', columns=['coverage'])
    g=g.sort_values(by='coverage', ascending=False)
    print(g)
    suffix="_"+suffix
    #convert the absolute values in the dataframes to percentages
    total=ki['coverage'].sum()
    ki['coverage'] = ki['coverage'].divide(total, axis=0)*100
    ki['coverage'] = ki['coverage'].round(4).astype(str) + ' %'
    ki.to_csv("kingdom_percentages"+suffix+".tsv", sep="\t")
    print(ki)

    total=p['coverage'].sum()
    p['coverage'] = p['coverage'].divide(total, axis=0)*100
    p['coverage'] = p['coverage'].round(4).astype(str) + ' %'
    p.to_csv("phyla_percentages"+suffix+".tsv", sep="\t")
    print(p)

    total=g['coverage'].sum()
    g['coverage'] = g['coverage'].divide(total, axis=0)*100
    g['coverage'] = g['coverage'].round(4).astype(str) + ' %'
    g.to_csv("genera_percentages"+suffix+".tsv", sep="\t")
    print(g)
if __name__ == '__main__':
    main()
