import os
import re
import math
import string
import sys

def read_contig(organism):
     try:
          f_dna = open(organism+'/contigs','r')
     except:
          print('cant open contig file ',organism)
          return ''

     dna = {}
     seq = ''
     name = ''
     for i in f_dna:
          if i[0]=='>':
               if len(seq)>10:
                    dna[name]=seq
               name = i.strip()
               if ' ' in name: #12149.1
                    temp = re.split(' ',name)
                    name = temp[0]
               '''
               if '_' in name:
                    temp = re.split('_',name)
                    name = temp[len(temp)-1]
               else:
               '''
               name = name[1:len(name)]

               seq = ''
          else:
               seq = seq+i.strip()


     dna[name]=seq
     f_dna.close()
     return dna

def find_repeat(fn,st,INSTALLATION_DIR,ppno,extraDNA,output_dir):
    if len(fn) == 0:
        print("Len sequence is 0 so ignoring\n")
        return {}
    #write dna in file
    tempOutFile = "tempRepeatDNA." + str(os.getpid()) + ".pp." + str(ppno) + ".fasta"
    try:
        outfile = open(output_dir+"/"+tempOutFile,"w")
    except:
        sys.exit("ERROR: Cannot open " + tempOutFile + " for writing\n")

    outfile.write('>pp' + str(ppno) + '\n'+fn)
    outfile.close()

    # call repeat finder
    try:
         cmd1 =INSTALLATION_DIR+"source/repeatFinder -f " + output_dir + tempOutFile
         os.system(cmd1)
    except:
         print('repeat finder did not work for ',len(fn))
         return {}

    #read repeats
    try:
        infile = open(output_dir + tempOutFile+".repeatfinder","r")
    except:
        sys.stderr.write("can't open " + output_dir + tempOutFile + ".repeatfinder\n")
        return {}

    rep = {}
    index = 0
    for line in infile:
        '''
        if 'note' in line:
            continue
        temp = re.split('join',line.strip())
        temp1 = temp[1][1:len(temp[1])-1]
        temp = re.split(',',temp1)
        t1 = re.split('\.\.',temp[0])
        t2 = re.split('\.\.',temp[1])
        if math.fabs(int(t1[0]) - int(t2[1])) > 10000:
            rep[index] = {}
            rep[index]['s1'] = int(t1[0])+st
            rep[index]['s2'] = int(t2[0])+st
            rep[index]['e1'] = int(t1[1])+st
            rep[index]['e2'] = int(t2[1])+st
            index = index + 1

       # Sajia's version 2
        temp = re.split('\t',line.strip())
        if math.fabs(int(temp[0]) - int(temp[3])) > 10000:
            rep[index] = {}
            rep[index]['s1'] = int(temp[0])+st
            rep[index]['s2'] = int(temp[2])+st
            rep[index]['e1'] = int(temp[1])+st
            rep[index]['e2'] = int(temp[3])+st
            index = index + 1
        '''
        # Robs version modified to allow searching slightly inside prophage
        temp = list(map(int, re.split('\t',line.strip())))
        # check if the repeats flank the prophage
        if( (temp[0] < (3*extraDNA)) and (temp[3] > (len(fn) - (3*extraDNA))) ):
            # check that start is always less than end
            #
            # This always causes an off by one error, so we have to increment our ends
            if temp[1] < temp[0]:
                [temp[0], temp[1]] = [temp[1]+1, temp[0]+1]
            if temp[3] < temp[2]:
                [temp[2], temp[3]] = [temp[3]+1, temp[2]+1]
            rep[index] = {}
            rep[index]['s1'] = temp[0]+st
            rep[index]['e1'] = temp[1]+st
            rep[index]['s2'] = temp[2]+st
            rep[index]['e2'] = temp[3]+st
            index += 1
    infile.close()
    return rep

def check_intg(prophage_sta,prophage_sto,rep,integ,con):
    for m in integ:
        if(integ[m]['contig'] != con):
            continue
        if integ[m]['start'] < (prophage_sta+(prophage_sto-prophage_sta)/2):
            l = integ[m]['start']
        else:
            l = integ[m]['stop']
        if (l - rep['s1'] <= 500 and l - rep['s1'] > 0) or (l - rep['e1'] <= 500 and l - rep['e1'] > 0) :
            return 1
        if (l - rep['s2'] <= 500 and l - rep['s2'] > 0) or (l - rep['e2'] <= 500 and l - rep['e2'] > 0) :
            return 1
    return 0

def find_smallest(a,b):
    mm = 1000000
    for i in a:
        for j in b:
            if math.fabs(i-j)<mm:
                mm = math.fabs(i-j)
    return mm

def find_rna(prophage_start,prophage_stop,repeat_list,organismPath,cont,integrs):
    try:
        infile = open(organismPath+'/Features/rna/tbl','r')
    except:
        sys.exit('Cannot open ' + organismPath + "/Features/rna/tbl")
    my_start = 1000000
    start_end = 0
    end_start = 0
    my_end = 1000000
    mydiff = 1000000
    for line in infile:
        temp = re.split('\t',line.strip())
        if len(temp)<3:
            continue
        if 'trna' in temp[2].lower() or 'tmrna' in temp[2].lower():
            if ',' in temp[1]:
                 ttemp = re.split(',',temp[1])
                 temp[1] = ttemp[len(ttemp)-1]
            temp1 = re.split('_',temp[1])

            #contig = temp1[len(temp1)-3]
            contig = temp[1][:temp[1][:temp[1].rfind('_')].rfind('_')]

            start = int(temp1[len(temp1)-2])
            stop = int(temp1[len(temp1)-1])
            if( cont == contig ):
                i = 0
                while( i < len(repeat_list) ):
                    a = find_smallest([start,stop],[repeat_list[i]['s1'],repeat_list[i]['s2'],repeat_list[i]['e1'],repeat_list[i]['e2']])

                    if check_intg(prophage_start,prophage_stop,repeat_list[i],integrs,cont) == 1:
                        if (math.fabs(repeat_list[i]['s1'] - repeat_list[i]['e2'])>math.fabs(my_start-my_end)) or mydiff == 1000000:
                            my_start = repeat_list[i]['s1']
                            my_end = repeat_list[i]['e2']
                            start_end = repeat_list[i]['e1']
                            end_start = repeat_list[i]['s2']
                            mydiff = a

                    if (a <= 500 and a < mydiff):
                        my_start = repeat_list[i]['s1']
                        my_end = repeat_list[i]['e2']
                        start_end = repeat_list[i]['e1']
                        end_start = repeat_list[i]['s2']
                        mydiff = a

                    i += 1
    infile.close()
    if mydiff == 1000000:
        return '0_0' #'null'
    return str(my_start)+'_'+ str(my_end)+'_'+ str(start_end)+'_'+ str(end_start)

def check_pp(contig,start,stop,pp):
    if( start > stop ):
        t = start
        start =stop
        stop = t

    j = 1
    while j < len(pp):
        if contig == pp[j]['contig']:
          if( pp[j]['start'] < start and pp[j]['stop'] > stop ):
              return j
        j += 1
    return 0


def check_phage_word_Start(sjcontig,a,b,c):
     j = 0
     tot = 0
     for i in c:
          start = c[i]['start']
          stop = c[i]['stop']
          if start>stop:
               t = start
               start = stop
               stop = t
          if a <= start and stop <= b  and c[i]['contig'] == sjcontig:
               if c[i]['pp']>0.5:
                    j += 1
               tot += 1
     if tot < 4 * j:
          return a
     else:
          return b


def check_phage_word_End(sjcontig,a,b,c):
     j = 0
     tot = 0
     for i in c:
          start = c[i]['start']
          stop = c[i]['stop']
          if start>stop:
               t = start
               start = stop
               stop = t
          if a <= start and stop <= b  and c[i]['contig'] == sjcontig:
               if c[i]['pp']>0.5:
                    j = j +1
               tot = tot + 1
     if tot < 4 * j:
          return b
     else:
          return a

def final_check_phage_word(sjcontig,a,b,c):
     j = 0
     tot = 0
     for i in c:
          start = c[i]['start']
          stop = c[i]['stop']
          if start>stop:
               t = start
               start = stop
               stop = t
          if a <= start and stop <= b and c[i]['contig'] == sjcontig:
               if c[i]['pp']>0:
                    j = j +1
               tot = tot + 1
     if j>5 and tot< 2*j:
          return str(a)+'_'+str(b)
     else:
          return '0_0'

def clarification_byPhageWord(sjcontig,bef_start,bef_stop,aft_start,aft_stop,genome):

     if aft_start == 0 and aft_stop == 0:
          return '0_0'
     if bef_start <= aft_start:
          s = check_phage_word_Start(sjcontig,bef_start,aft_start,genome)
     else:
          s = check_phage_word_Start(sjcontig,aft_start,bef_start,genome)

     if bef_stop <= aft_stop:
          e = check_phage_word_End(sjcontig,bef_stop,aft_stop,genome)
     else:
          e = check_phage_word_End(sjcontig,aft_stop,bef_stop,genome)
     se = final_check_phage_word(sjcontig,s,e,genome)

     return se


def fixing_start_end(output_dir,organismPath,INSTALLATION_DIR):
    try:
        infile = open(output_dir+'initial_tbl.txt','r')
    except:
        sys.exit('ERROR: Cannot open ' + output_dir + 'initial_tbl.txt')

    #make all predicted pp list
    print("Checking prophages in " + output_dir + "initial_tbl.txt\n")
    pp = {}
    i = 0
    flag = 0
    intg = {}
    intg_index = 1
    genome = {}
    index = 1
    temp = {}
    oldtemp = {}
    for line in infile:
        oldtemp = temp
        temp = re.split('\t',line.strip())
        if temp[1]=='function':
            continue
        # Find location of all prophage regions
        if( int(temp[7]) == 1 ):
            if( (temp[2] != oldtemp[2]) or (flag == 0) ):
                i += 1
                pp[i]={}
                pp[i]['contig'] = temp[2]
                pp[i]['start'] = min(int(temp[3]), int(temp[4]))
            pp[i]['stop'] = max(int(temp[3]),int(temp[4]))
            flag = 1
        else:
            flag = 0
        # Find location of integrases
        if float(temp[8]) == 1.5:
            if int(temp[3]) < int(temp[4]):
                intg[intg_index] = {}
                intg[intg_index]['start']=int(temp[3])
                intg[intg_index]['stop']=int(temp[4])
                intg[intg_index]['contig']=str(temp[2])
            else:
                intg[intg_index] = {}
                intg[intg_index]['start']=int(temp[4])
                intg[intg_index]['stop']=int(temp[3])
                intg[intg_index]['contig']=str(temp[2])
            intg_index += 1
        # Find
        genome[index]={}
        genome[index]['start'] = int(temp[3])
        genome[index]['stop'] = int(temp[4])
        genome[index]['pp'] = float(temp[8])
        genome[index]['contig'] = temp[2]
        index += 1
    infile.close()
    # find start end for all pp using repeat finder
    dna = read_contig(organismPath)
    extraDNA = 2000
    for i in pp:
        start = pp[i]['start'] - extraDNA
        if(start < 1):
            start = 1
        if 'stop' in pp[i]:
             stop = pp[i]['stop'] + extraDNA
        else:
             stop = genome[len(genome)-1]['stop']
             sys.exit("Not sure what this does")
        if(stop > len(dna[pp[i]['contig']])):
            stop = len(dna[pp[i]['contig']])
        if stop - start >200000:
            print("Not checking repeats for pp " + str(i) + " because it is too big: " + str(stop - start) + "\n")
            continue
        print("Finding repeats in pp " + str(i) + " from " + str(start) + " to " + str(stop))
        repeat_list = find_repeat(dna[pp[i]['contig']][start:stop],start,INSTALLATION_DIR,i,extraDNA,output_dir)
        s_e = find_rna(start,stop,repeat_list,organismPath,pp[i]['contig'],intg)
        if s_e != 'null':
            t = re.split('_',s_e)
            if s_e == '0_0':
                 s_e1 = clarification_byPhageWord(pp[i]['contig'],pp[i]['start'],pp[i]['stop'],pp[i]['start'],pp[i]['stop'],genome)
            else:
                 s_e1 = clarification_byPhageWord(pp[i]['contig'],pp[i]['start'],pp[i]['stop'],float(t[0]),float(t[1]),genome)
            t1 = re.split('_',s_e1)
            pp[i]['start'] = float(t1[0])
            pp[i]['stop'] = float(t1[1])
            if( (float(t[0]) != 0) and (pp[i]['start'] == float(t[0])) and (pp[i]['stop'] == float(t[1])) ):
            #if (float(t[0])!= 0) and (float(t1[0]) == float(t[0])) and (float(t1[1]) == float(t[1])):
                 temps1 = min(t[0],t[2])
                 tempe1 = max(t[0],t[2])
                 temps2 = min(t[1],t[3])
                 tempe2 = max(t[1],t[3])
                 pp[i]['att'] = t[0] +'\t'+t[2]+'\t'+t[3]+'\t'+t[1]+'\t'+dna[pp[i]['contig']][int(temps1)-1:int(tempe1)]+'\t'+dna[pp[i]['contig']][int(temps2)-1:int(tempe2)]+'Repeat exactly at the end'

            else:
               # this approach will just append the longest repeat
                longestrep = 0
                bestrep = None
                for idx in repeat_list:
                    lengthrep = math.fabs(repeat_list[idx]['e1'] - repeat_list[idx]['s1'])
                    if (lengthrep > longestrep) and (lengthrep < 150):
                        longestrep = lengthrep
                        bestrep = repeat_list[idx]

                if bestrep:
                    attLseq = dna[pp[i]['contig']][int(bestrep['s1'])-1:int(bestrep['e1'])-1]
                    attRseq = dna[pp[i]['contig']][int(bestrep['s2'])-1:int(bestrep['e2'])-1]
                    if len(attLseq) == 0:
                        print("Could not get a sequence from " + str(int(bestrep['s1'])-1) + " to " + str(int(bestrep['e1'])-1) + " from " + str(pp[i]['contig']) + " (length: " + str(len(dna[pp[i]['contig']])) + ")\n")
                    if len(attRseq) == 0:
                        print("Could not get a sequence from " + str(int(bestrep['s2'])-1) + " to " + str(int(bestrep['e2'])-1) + " from " + str(pp[i]['contig']) + " (length: " + str(len(dna[pp[i]['contig']])) + ")\n")
                    pp[i]['att'] = "\t".join(map(str, [bestrep['s1'], bestrep['e1'], bestrep['s2'], bestrep['e2'], attLseq, attRseq, "Longest Repeat flanking phage and within " + str(extraDNA) + " bp"]))




    # fix start end for all pp
    try:
        infile = open(output_dir+'initial_tbl.txt','r')
        outfile = open(output_dir+'prophage_tbl_temp.txt','w')
    except:
        sys.exit('ERROR: Cannot open ' + output_dir + 'initial_tbl.txt')

    for line in infile:
        temp = re.split('\t',line.strip())
        if temp[1]=='function':
            outfile.write(line)
            continue
        me = check_pp(temp[2],int(temp[3]),int(temp[4]),pp)
        if me == 0:
             outfile.write(line.strip()+'\t0'+'\n')
        else:
             outfile.write(line.strip()+'\t1'+'\n')

    infile.close()
    outfile.close()
    os.remove(output_dir + 'initial_tbl.txt')

############################## added in new version  ##################################################
def fixing_false_negative(output_dir, threshold_for_FN, phageWindowSize):
     try:
          infile = open(output_dir+'prophage_tbl_temp.txt','r')
     except:
          sys.exit("ERROR: Cannot open "+output_dir+"prophage_tbl_temp.txt")

     pp_change = []
     fn_end = 0
     fn_start = 0
     fn_contig = ''
     count_fn = 0
     temp = []
     oldtemp = []
     print("Threshold for fn is ", threshold_for_FN)
     for line in infile:
        oldtemp = temp
        temp = re.split('\t',line.strip())
        if temp[1]=='function':
            continue

        me = int(temp[9])
        pp = float(temp[8])

        if(temp[2] != oldtemp[2]): #new contig
            count_fn = 0

        if( count_fn == 0 ):
            if( me == 0 and pp >= 1 ):
                count_fn =  1
                fn_start = int(temp[5])
            elif( me == 1 or pp >= 1 ):
                count_fn =  1
                fn_start = int(temp[5])
                fn_end = int(temp[5])
        else:
            if( me == 1 or pp >= 1 ):
                count_fn += 1 # we are in a run of prophage genes
                fn_end = int(temp[5])
            else:
                # we are not in a run of prophage genes, or in the midst of one, but we'll go to the last
                # gene we've seen
                if( (int(temp[5])-fn_start) > 2 * phageWindowSize ):
                     if( count_fn > threshold_for_FN ):
                          while( fn_start <= fn_end ):
                               pp_change.append(fn_start)
                               fn_start = fn_start + 1
                     count_fn = 0
     infile.close()

     try:
          infile = open(output_dir+'prophage_tbl_temp.txt','r')
          outfile = open(output_dir+"prophage_tbl.txt",'w')
     except:
          sys.exit("ERROR: Cannot open "+output_dir+"prophage_tbl.txt")

     for line in infile:
          temp = re.split('\t',line.strip())
          if temp[1]=='function':
               outfile.write(line)
               continue

          position = int(temp[5])
          if position in pp_change:
               line = line.strip()
               line = line[0:len(line)-1] + '1' + '\n'
          outfile.write(line)
     infile.close()
     outfile.close()
     os.remove(output_dir + 'prophage_tbl_temp.txt')


def make_prophage_tbl(input,output):
     try:
          f = open(input,'r')
          fw = open(output,'w')
     except:
          print('Cant open',input)

     pp = {}
     ppindx = 0
     flag = 0
     total_phage_gene = 0
     prev_contig = ''

     for line in f:
          if flag == 0:
               flag = 1
               continue
          temp = re.split('\t',line.strip())
          if int(temp[9]) == 1:
               if total_phage_gene == 0 or prev_contig != temp[2]:
                    id_temp = temp[0][:len(temp[0])-temp[0][::-1].find('.')-4]
                    id_temp = id_temp + 'pp.' + str(ppindx)
                    loc_temp = temp[2]+'_'
                    if int(temp[3])>int(temp[4]):
                         loc_temp = loc_temp + temp[4] + '_'
                    else:
                         loc_temp = loc_temp + temp[3] + '_'

                    pp[ppindx] = id_temp + '\t' + loc_temp
                    ppindx = ppindx + 1
                    prev_contig = temp[2]
                    total_phage_gene = 0

               total_phage_gene = total_phage_gene+1

               if int(temp[3])>int(temp[4]):
                    pp[ppindx-1] = pp[ppindx-1][:len(pp[ppindx-1])-pp[ppindx-1][::-1].find('_')] +temp[3]
               else:
                    pp[ppindx-1] = pp[ppindx-1][:len(pp[ppindx-1])-pp[ppindx-1][::-1].find('_')] +temp[4]
          else:
               total_phage_gene = 0

     for i in pp:
          fw.write(pp[i]+'\n')

     f.close()
     fw.close()



################################################################################

def call_start_end_fix(output_dir, organismPath, INSTALLATION_DIR, threshold_for_FN, phageWindowSize):
     # Make the prophage_tbl_temp.txt file.
     fixing_start_end(output_dir,organismPath,INSTALLATION_DIR)
     fixing_false_negative(output_dir, threshold_for_FN, phageWindowSize)
     #make_prophage_tbl(output_dir+'prophage_tbl.txt',output_dir+'prophage.tbl')

