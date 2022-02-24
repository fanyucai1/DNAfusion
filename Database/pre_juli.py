infile=open("CosmicFusionExport_v95.tsv","r")
outfile=open("CosmicFusionExport_v95_hg38.tsv","w")
outfile.write("id_sample\tSample name\tPrimary site\tSite subtype 1\t"
              "Site subtype 2\tSite subtype 3\tPrimary histology\tHistology subtype 1\t"
              "Histology subtype 2\tHistology subtype 3\tFusion ID\tTranslocation Name\t"
              "Fusion Type\tPUBMED_PMID\tID_STUDY")
for line in infile:
    array = line.strip().split("\t")
    outfile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n"%(array[0],array[1],array[2],array[3],
                      array[4],array[5],array[6],array[7],
                      array[8],array[9],array[10],array[11],
                      array[-2],array[-1]))
infile.close()
outfile.close()
