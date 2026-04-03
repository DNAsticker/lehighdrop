b = 8  # bases per bit_is_0 or bit_is_1 region
c = 6  # bases per common region
t = 4  # bases per toehold 
#b = 6  # bases per bit_is_0 or bit_is_1 region
#c = 2  # bases per common region
#t = 3  # bases per toehold 
n = 3  # bits per strand
len_bit = 2*b + c
len_strand = n*len_bit
len_seq = len_strand + 2*n*t
print('sticker system implmented with strand displacement')
print('b='+str(b)+' c='+str(c)+' t='+str(t)+' n='+str(n))
print('len_bit='+str(len_bit)+' len_strand='+str(len_strand)+' len_seq='+str(len_seq))

global rawseq
complement_dict=dict()
complement_dict['c']='G'
complement_dict['g']='C'
complement_dict['a']='T'
complement_dict['t']='A'
complement_dict['C']='G'
complement_dict['G']='C'
complement_dict['A']='T'
complement_dict['T']='A'


def getbit_is_0():
    global rawseq
    bit_is_0 = rawseq[0:b]
    rawseq = rawseq[b:]
    return bit_is_0

def gettoe_0():
    global rawseq
    bit_is_0 = rawseq[0:t]
    rawseq = rawseq[t:]
    return bit_is_0

def getcommon():
    global rawseq
    common = rawseq[0:c]
    rawseq = rawseq[c:]
    return common 

def getbit_is_1():
    global rawseq
    bit_is_1 = rawseq[0:b]
    rawseq = rawseq[b:]
    return bit_is_1

def gettoe_1():
    global rawseq
    bit_is_1 = rawseq[0:t]
    rawseq = rawseq[t:]
    return bit_is_1

def reverse(s):
    return s[-1:-len(s)-1:-1]

def complement(s):
    c=''
    for i in s:
        c+=complement_dict[i]
    return c

def getbit():
    is_0 = getbit_is_0()
    toe0 = gettoe_0()
    comm = getcommon()
    is_1 = getbit_is_1()
    toe1 = gettoe_1()
    if toe0 == toe1:
        print("****toe uniq violation: "+toe0)
    stick_bit_is_0 = complement(is_0 + comm)
    probe_bit_is_0 = complement(is_0 + toe0)
    stick_bit_is_1 = complement(comm + is_1)   #sept 12,2025 correction since is_1 + comm was backwards
    probe_bit_is_1 = complement(is_1 + toe1)
    strand_bit = is_0 + comm + is_1
    print ( ( is_0, toe0, comm, is_1, toe1 ))
    #print(rawseq)
    return ((strand_bit, stick_bit_is_0, probe_bit_is_0, stick_bit_is_1, probe_bit_is_1))

def checkselfhybrid(strand):
    for i in range(0,33):
        if strand.count(complement(reverse(strand[i:i+4]))) != 0 :
            print(strand[i:i+4], end=' hybridizes with ')
            print(complement(reverse(strand[i:i+4])),end=" at ")
            print(i)
            if strand[i:i+4]==complement(reverse(strand[i:i+4])):
                print(" which is OK since too tight for hairpin")



def buildstrandisp(rawseqparam):
    global rawseq
    rawseq=rawseqparam
    #rawseq = "AGTATCCGGTAGTCGAGTCCGAAAGTAGCGCTGCTTATATAGTACGATGAGGTCACGAGA"
    #rawseq = "AACACGGTAGAACCCAATTTGTGCCTTCAATGATTATGCGATCGTCGAGCTGTAGTTTCG"
    rawseq = rawseq.upper()
    if len(rawseq)!=len_seq:
        print("wrong rawseq length")
        quit()
    print("using rawseq:")
    print(rawseq)
    checkselfhybrid(rawseq)
    print("")

    strand = ""
    bit2 = getbit()
    strand += bit2[0]
    (stick_bit2_is_0, probe_bit2_is_0, stick_bit2_is_1, probe_bit2_is_1) = bit2[1:]
    bit1 = getbit()
    strand += bit1[0]
    (stick_bit1_is_0, probe_bit1_is_0, stick_bit1_is_1, probe_bit1_is_1) = bit1[1:]
    bit0 = getbit()
    strand += bit0[0]
    (stick_bit0_is_0, probe_bit0_is_0, stick_bit0_is_1, probe_bit0_is_1) = bit0[1:]

    checkselfhybrid(strand)

    print("")
    print("data strand= 5' " + strand+" 3'")
    print("")
    print("stick_bit2_is_0= 3' " + stick_bit2_is_0 + " 5' = 5' " + reverse(stick_bit2_is_0) + " 3'")
    print("stick_bit2_is_1= 3' " + stick_bit2_is_1 + " 5' = 5' " + reverse(stick_bit2_is_1) + " 3'")
    print("stick_bit1_is_0= 3' " + stick_bit1_is_0 + " 5' = 5' " + reverse(stick_bit1_is_0) + " 3'") 
    print("stick_bit1_is_1= 3' " + stick_bit1_is_1 + " 5' = 5' " + reverse(stick_bit1_is_1) + " 3'")
    print("stick_bit0_is_0= 3' " + stick_bit0_is_0 + " 5' = 5' " + reverse(stick_bit0_is_0) + " 3'")
    print("stick_bit0_is_1= 3' " + stick_bit0_is_1 + " 5' = 5' " + reverse(stick_bit0_is_1) + " 3'") 
    print("")
    print("probe_bit2_is_0= 3' " + probe_bit2_is_0 + " 5' = 5' " + reverse(probe_bit2_is_0) + " 3'")
    print("probe_bit2_is_1= 3' " + probe_bit2_is_1 + " 5' = 5' " + reverse(probe_bit2_is_1) + " 3'")
    print("probe_bit1_is_0= 3' " + probe_bit1_is_0 + " 5' = 5' " + reverse(probe_bit1_is_0) + " 3'")
    print("probe_bit1_is_1= 3' " + probe_bit1_is_1 + " 5' = 5' " + reverse(probe_bit1_is_1) + " 3'")
    print("probe_bit0_is_0= 3' " + probe_bit0_is_0 + " 5' = 5' " + reverse(probe_bit0_is_0) + " 3'")
    print("probe_bit0_is_1= 3' " + probe_bit0_is_1 + " 5' = 5' " + reverse(probe_bit0_is_1) + " 3'")
    print("")
    print("antiprobe_bit2_is_0= 5' " + complement(probe_bit2_is_0)+" 3'")
    print("antiprobe_bit2_is_1= 5' " + complement(probe_bit2_is_1)+" 3'")
    print("antiprobe_bit1_is_0= 5' " + complement(probe_bit1_is_0)+" 3'") 
    print("antiprobe_bit1_is_1= 5' " + complement(probe_bit1_is_1)+" 3'")
    print("antiprobe_bit0_is_0= 5' " + complement(probe_bit0_is_0)+" 3'") 
    print("antiprobe_bit0_is_1= 5' " + complement(probe_bit0_is_1)+" 3'")

#buildstrandisp('GTCTTTCACTTCGGTTAACGCCTGCAAGCTCGTAGATAGATATGTTCCTTTAAGCCACTA')
#buildstrandisp('CTACCCTCTATCGAGAATTCGACTTTGCATAACCAGTATACTATTGTAGCCAGCACTCTG')
#buildstrandisp('GTTGGTTGAACATAGTACCCTCCCTAGCTCACTACGACTGTCTGAATACGCTCCGTCTAT')
#buildstrandisp('AACACGGTAGAACCCAATTTGTGCCTTCAATGATTATGCGATCGTCGAGCTGTAGTTTCG')
#buildstrandisp('AGTATCCGGTAGTCGAGTCCGAAAGTAGCGCTGCTTATATAGTACGATGAGGTCACGAGA')
#buildstrandisp('GATCGCAGCACTTCTAAAGTTGCCCTACAGAAACTCGTATAACTATATTGGGTCCAAGCA')
#buildstrandisp('TACAGGTACCGAGTTATAATTCAATAAACAGCATGCAGTCGAAATGTCCAACGTTTCTCT')

#checkselfhybrid('ACAGAAACCATTGGCTGATTTCGGAACTTTGCACGGATCACTCTATATCGAACCCTCGTACACTTG')
#checkselfhybrid('TATATTTGAGAGAATAGAACAACGCTGCTACGAACGACTAACGGAAGACTCACACATTAACATACT')

#this is 60-bp strand in powerpoint as raw input
buildstrandisp('CGACCATACCACTCCCTTAGGTTGTAGATACCAGGCGAAATCGTAGAAAATAGACCGTAACTCCTCTGCGCTAGTAATTGTGCGTTTAAC')

#60-bp strands (4-4-4 regions (4 bit_is region - 4 common - 4 toehold)):
#CGGACGAATGACCAGGTTCACTAGAGGGGATTATATGGAGACATGGAATAGGTACTGCAC
#GCGGGCAGCGGGTTTTTGTCTGGTTCCTCCTATTGAATTATGTTCGCACAGGGCGGGACT -- great strand, no hybridizing
#TTTCTAGTACCGCGCCCCGTGAGATAAGAGTAGTTAGCGAGTATGTCAATGTCGATCCCG
#CTCACCGGCTTCTAGTCAGTTTTGTGTACCTGGATGCTGCTGTCTTAACCTATAAATAAA
#GCCTGCGTTGAAAACTCCAGCTTTATTCTGTGCTTTACATCGCCTGTGCTCTCCTGAAAA
#ACTCCTTCGCAAAGATACTCTAGCCGCCCTCCATCAGCCCCCCAGACACGTACCTCACCC

#72-bp strands (6-4-4 regions):
#TACTCGCATCTCTTACGCCCTGTCCCGCCCCCAGTCATATCGGAATAGTGCCCTTACATCTTTTTTTGGCTT
#GTACCGCGACTTTCAGGACTACCAGGCACAACACAGAGCGATCTATATCAACATTGCACCAAGAGAAGAGCG
#ACAGCCTCCGCAGGTAGAACACGCTAATCACATCACGCATAACCCTCACCAGTAGTGCAGACCATCCCTCAG -- great strand, no hybridizing
#TAGGCACCTGCGGGCTTATCTGTAACAATTTCATCACTTAGCGTGTGGCTTTTCGCGGAGTAGGAGGCTTAA
#CGATTATTACCCGTACCCCGACACCGATCCCCCAACGAAGGCTACTACTATGGACGAGGTTAGAATGCCAAC -- meh strand, but check anyways
#GTTTTGCATACTGTGACTCAAGGCGGGTAAATTCGGTGATGTGACCAGCTACTGAACAATCCCCATTATAGG

#78-bp strands (6-6-4 regions)
#AAGATAAGACAGGAAAGCAGAGAAGAGAAAGATGCACTCGACGAAAAATTAAAACCTACACAGCACACGGGCTAGAGC -- great strand, two ok hybridizations
#AGGAGAACGAAATTCATGCTCTTCCGCAAACACAGGCCAAAGCCCAGCCGCGAGACTACATAGGCGCTACTAAGGTAA -- meh strand
#GCGACGGCTACACCACGACAAAAACTCCCCTACGACAATACTACTACCAGCAGGACACCAGCGGGCATGGATTAAGTC -- great strand, no hybridizing
#TTGAAGGCCGAGGGGGATGACAAGAAGAAGTAACAGGCGTCCAATTAGAAGAGAACTAGGTCGTGCGTAAACACATAA -- great strand
#ACCCAGGCATAGAGTCACCCAATAGACCGTATCGGCAGTTTGTCCATATAAAGATGTCCCACCTCAGCCCGTAGTTAC -- great strand
#AAAGCAAGGCCGCCCACAAAAAACTAACCTCTTCCCGTAACGTAAACATCTACTAACGCCCTCATCCGCGCTCCACCC -- great strand

#90-bp (8-6-2 regions) -- these are harder to generate
#CCGCTCACAATACTACCTGGAGATGTACGAAGGATAGGCTTAGGCGTTGGCCGATTAGAAGATGCACTAGGGGAATGCTACGACACCGAT -- meh
#AATTTTCCAGGCGATGACGGGGCACGAAGGTTTAGTGATGAGGTTCCGGCCATAAGCGACGAAGCGTTGTCCTATAAGAGCGTTTGGGCG -- good, not great
#TCGGACTTCCCCCGGTCTTTCAATCGTTCAGCCCCTGGGTGTCACTCTTCTACTCGACTAACTGGTACATCCCTTCTCCTTCTCTGGGTG -- great strand
#CCCTTTTCAAACTCGATAGCTGTCAACAACATGATACAAGCCAACGCTCCTCAGTAGACCATTCCATTACCCTGCAATTCTTATTCTTAC -- meh
#CCTTCGGGCCTTGAATGCGGGCTGGGATGTAGGTCGGGTTTGGCTGTGAGAGATTGGCGGATAGCTTTGTTGGGGTTGTGCTGTGCGGGT -- great strand
#CCAGCGAGGCTTCCCCTACAAACTACCAGGTTATGGAGCACACGATTCACTTTCACATGCACGGCAACTAAATAGCGGGCCACATTGACC -- great strand
#CGACCATACCACTCCCTTAGGTTGTAGATACCAGGCGAAATCGTAGAAAATAGACCGTAACTCCTCTGCGCTAGTAATTGTGCGTTTAAC -- great strand