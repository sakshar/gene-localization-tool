from Bio import SeqIO
import sys
import pandas as pd
import openpyxl
from reportlab.lib.units import cm
from Bio.Graphics import BasicChromosome


def geneFamilyPlotter(chrLenMap, colorMap):
    chrs = list(chrLenMap.keys())
    gfs = list(colorMap.keys())
    max_len = chrLenMap[max(chrLenMap, key=chrLenMap.get)]  # Could compute this from the entries dict
    telomere_length = 10000  # For illustration

    chr_diagram = BasicChromosome.Organism()
    chr_diagram.page_size = (32 * cm, 21 * cm)  # A4 landscape

    for ch in chrs:
        record = SeqIO.read("tmp/"+ch+".gb", "genbank")
        length = len(record)
        # Record an Artemis style integer color in the feature's qualifiers,
        # 1 = dark grey, 2 = red, 3 = green, 4 = blue, 5 =cyan, 6 = magenta, 10 = orange
        features = []
        for f in record.features:
            if f.type in gfs:
                f.qualifiers["color"] = [colorMap[f.type]]
                features.append(f)
            elif f.type == "centromere":
                f.qualifiers["color"] = [1]
                features.append(f)


        cur_chromosome = BasicChromosome.Chromosome(ch)
        # Set the scale to the MAXIMUM length plus the two telomeres in bp,
        # want the same scale used on all five chromosomes so they can be
        # compared to each other
        cur_chromosome.scale_num = max_len + 2 * telomere_length

        # Add an opening telomere
        start = BasicChromosome.TelomereSegment()
        start.scale = telomere_length
        cur_chromosome.add(start)

        # Add a body - again using bp as the scale length here.
        body = BasicChromosome.AnnotatedChromosomeSegment(length, features)
        body.scale = length
        cur_chromosome.add(body)

        # Add a closing telomere
        end = BasicChromosome.TelomereSegment(inverted=True)
        end.scale = telomere_length
        cur_chromosome.add(end)

        # This chromosome is done
        chr_diagram.add(cur_chromosome)

    chr_diagram.draw("geneFamilies.pdf", "")


def chrLenMapper(fileName):
    chrLenMap = dict()
    f = open(fileName, "r")
    while True:
        line = f.readline().strip()
        if not line:
            break
        words = line.split(',')
        chrLenMap[words[0]] = int(words[1])
    return chrLenMap


def colorMapper(fileName):
    colorMap = dict()
    f = open(fileName, "r")
    while True:
        line = f.readline().strip()
        if not line:
            break
        words = line.split(',')
        colorMap[words[0]] = int(words[1])
    return colorMap


def gfDataParser(fileName, chrs):
    gene_list = pd.read_excel(fileName, engine="openpyxl")
    gene_dict = dict()
    for chr in chrs:
        gene_dict[chr] = dict()
    for index, row in gene_list.iterrows():
        gene_dict[str(row['chr'])][str(row['ID'])] = (str(row['family']), int(row['start']), int(row['end']), int(row['sign']))
    return gene_dict


def gbCreator(gene_dict, chrLenMap):
    chrs = list(chrLenMap.keys())
    for chr in chrs:
        gb = open("tmp/"+chr+".gb", 'w')
        gb.write("LOCUS       BdWA1           "+str(chrLenMap[chr])+" bp    DNA     linear   CON 27-APR-2022\n")
        gb.write("DEFINITION  Babesia duncani chromosome "+chr[3:]+" sequence.\n")
        gb.write("ACCESSION   BdWA1\n")
        gb.write("VERSION     BdWA1.0\n")
        gb.write("KEYWORDS    RefSeq.\n")
        gb.write("SOURCE      Babesia duncani (parasite)\n")
        gb.write("FEATURES             Location/Qualifiers\n")
        gb.write("     source          1.."+str(chrLenMap[chr])+"\n")
        gb.write("                     /organism=\"Babesia duncani\"\n")
        gb.write("                     /mol_type=\"genomic DNA\"\n")
        gb.write("                     /chromosome=\""+chr[3:]+"\"\n")
        genes = list(gene_dict[chr].keys())
        for gene in genes:
            tup = gene_dict[chr][gene]
            if tup[3] == 0:
                gb.write("     "+tup[0])
                gb.write("             "+str(tup[1])+".."+str(tup[2])+"\n")
                gb.write("                     /gene="+"\""+gene+"\"\n")
                gb.write("     "+tup[0])
                gb.write("             complement(" + str(tup[1]) + ".." + str(tup[2]) + ")\n")
                gb.write("                     /gene="+"\""+gene+"\"\n")
            else:
                gb.write("     "+tup[0])
                if tup[3] == 1:
                    gb.write("             "+str(tup[1])+".."+str(tup[2])+"\n")
                elif tup[3] == -1:
                    gb.write("             complement(" + str(tup[1]) + ".." + str(tup[2]) + ")\n")
                gb.write("                     /gene="+"\""+gene+"\"\n")
        gb.write("CONTIG      1.."+str(chrLenMap[chr])+"\n")
        gb.write("//")
        gb.close()


if __name__ == "__main__":
    data = sys.argv[1]
    chrLenFile = sys.argv[2]
    colorFile = sys.argv[3]
    chrLenMap = chrLenMapper(chrLenFile)
    colorMap = colorMapper(colorFile)
    gfs = list(colorMap.keys())
    chrs = list(chrLenMap.keys())
    geneDict = gfDataParser(data, chrs)
    gbCreator(geneDict, chrLenMap)
    geneFamilyPlotter(chrLenMap, colorMap)
    