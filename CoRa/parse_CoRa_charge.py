import glob
import re


def parse_bppml_out(indir, outfile):
    results = glob.glob(indir + "*.CoRa_charge.params.txt")
    of = open(outfile, "w")
    print("Writing to {}".format(outfile))
    of.write("file\titer\tL_M0\tL_CoRa_charge\tLR\tOmega_M0\tOmega_Co\tOmega_Ra\tsig_LR\tCo_greater\n")
    # of.write("file\titer\tL_M0\tL_CoRa_charge\tLR\tOmega_M0\tOmega_Co\tOmega_Ra\tlength\tsig_LR\tCo_greater\n")
    for r in results:
        output_CoRa = open(r, "r").read()
        output_M0 = open(r.replace("CoRa_charge", "M0"), "r").read()
        i = r.split(".")[1].split("/")[-1]
        try:
            L_M0 = re.search("# Log likelihood = ([\-0-9.]+)\n", output_M0).group(1)
            print(1)
            L_CoRa = re.search("# Log likelihood = ([\-0-9.]+)\n", output_CoRa).group(1)
            print(2)
            Omega_M0 = re.search(",omega=([0-9.]+)", output_M0).group(1)
            print(3)
            Omega_Co = re.search(",omegaC=([0-9.]+)", output_CoRa).group(1)
            print(4)
            Omega_Ra = re.search(",omegaR=([0-9.]+)", output_CoRa).group(1)
            # length = re.search("# Number of sites = ([0-9]+)\n", output_M0).group(1)
            LR = 2 * (abs(float(L_M0)) - abs(float(L_CoRa)))
            of.write("\t".join([str(t) for t in [r, i, L_M0, L_CoRa, LR, Omega_M0, Omega_Co, Omega_Ra, int(LR > 3.841), int(Omega_Co > Omega_Ra)]]) + "\n") #convert columns to nucs
            # of.write("\t".join([str(t) for t in [r, i, L_M0, L_CoRa, LR, Omega_M0, Omega_Co, Omega_Ra, float(length)*3, int(LR > 3.841), int(Omega_Co > Omega_Ra)]]) + "\n") #convert columns to nucs
        except AttributeError:
            of.write("{}\t{}\t{}\n".format(r, i, "\t".join(["NA"]*8)))
            # of.write("{}\t{}\t{}\n".format(r, i, "\t".join(["NA"]*9)))
            print ("NA")
    return

parse_bppml_out("./data/output/", "parsed_bppml_CoRa_charge.txt")
