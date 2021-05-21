# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 15:37:47 2018

@author: mzell & Kingslayer


C version includes hoga update 1660 Ti
D version includes 3rd gpu-unit
"""
import matplotlib.pyplot as plt
import re
import mysql.connector
import json

def remove_non_number(text):
   a = re.sub(r'\x1b(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])',' ', text)
   b = re.sub(' +',' ',a)
   c = b.split(" ")
   #print(c)
   #print("len=",len(c))
   return (c)
    
def remove_fan_hundert(text):
   return re.sub(r'm100 %','m 99 %', text)

def insert_varibles_into_table(user, algo, gpu, temp, fan, speed, share, core, mem, power, eff, logtime, uptime, energy, gpunr):
    try:
        connection = mysql.connector.connect(host='DATABASE IP OR DYNDNS',
                                             database='DATABASE-NAME',
                                             user='DATABASE-USER',
                                             password='PASSWORD',
					     ssl_cert='ca-cert.pem',
                                             ssl_key='ca-key.pem')
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO xmrig (user, algo, gpu, temp, fan, speed, share, core, mem, power, eff, logtime, uptime, energy, gpunr) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """

        record = (user, algo, gpu, temp, fan, speed, share, core, mem, power, eff, logtime, uptime, energy, gpunr)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        print("Record inserted successfully into xmrig table")

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def read_json_config(file):
    try:                              # Try to:
        with open (file, 'r') as f:        # open file for reading text.
            # parse file
            js = json.loads(f.read())
            # show values
            #print("name: " + str(js['logfilename']))
            #for i in range(len(js['pattern'])):
            #    print("pattern" +str(i) +" " + str(js['pattern'][i]))
            return(js)
                                
    except FileNotFoundError:                   # If log file not found,
               print("gpu_parse.json file not found.")                # print an error message. 		
                    
    finally:
        if f is not None:
            f.close()    


def algo_read_save(file, newdata):
    try:                              # Try to:
        with open(file,'r+') as myfile:
            data = myfile.read()
            if(newdata != ''):
                myfile.seek(0)
                myfile.write(newdata)
                myfile.truncate()
            return(data)
                                
    except FileNotFoundError:                   # If log file not found,
        print("algo.log file not found.")                # print an error message. 		
                    
    finally:
        if myfile is not None:
            myfile.close()    
   

patt = []
pat_occur_t0 = []
pat_occur_t1 = []
pat_occur_t2 = []
pat_occur_t3 = []
pat_occur_t4 = []

logtime =[]
uptime = []
energy = []
algo = []

id0 = []
id1 = []
id2 = []
gpu0 = []
gpu1 = []
gpu2 = []
temp0 = []
temp1 = []
temp2 = []
fan0 = []
fan1 = []
fan2 = []
speed0 = []
speed1 = []
speed2 = []
share0 = []
share1 = []
share2 = []
core0 = []
core1 = []
core2 = []
mem0 = []
mem1 = []
mem2 = []
power0 = []
power1 = []
power2 = []
eff0 = []
eff1 = []
eff2 = []

gpu0_found = False
gpu1_found = False
gpu2_found = False
removestr0 = " "
removestr1 = " "
removestr2 = " "

try:                              # Try to:

    js = read_json_config("gminer-log.json")

    #Username
    user = js['username']
       
    #build pattern lines   
    for i in range(len(js['pattern'])):
        patt.append(re.compile(r'%s' % js['pattern'][i], re.IGNORECASE))
    
   
    #look for gpu sub type - space in gpu type   
    for i in range(len(js['gputype'])):
        if (' ' in js['gputype'][i]):
            if (i == 0):
                removestr0 = (js['gputype'][i].rsplit(" ",1)[-1])
            if (i == 1):
                removestr1 = (js['gputype'][i].rsplit(" ",1)[-1])
            if (i == 2):
                removestr2 = (js['gputype'][i].rsplit(" ",1)[-1])

    
    with open (js['logfilename'], 'r+') as in_file:        # open file for reading text.
            
        for linenum, line in enumerate(in_file):        # Keep track of line numbers. 
            if patt[0].search(line) != None:          # Uptime pattern,
                pat_occur_t0.append((linenum, line.rstrip('\n'))) # strip linebreaks, store line and line number in list as tuple.
            if patt[1].search(line) != None:          # Algorithm pattern,
                pat_occur_t1.append((linenum, line.rstrip('\n'))) # strip linebreaks, store line and line number
            if patt[2].search(line) != None:          # GPU0 pattern,
                pat_occur_t2.append((linenum, line.rstrip('\n'))) # strip linebreaks, store line and line numb
                gpu0_found = True  
                
            if (len(js['pattern'])) > 3:            # if 2nd gpu pattern
                if patt[3].search(line) != None:          # GPU1 pattern,
                    pat_occur_t3.append((linenum, line.rstrip('\n'))) # strip linebreaks, store line and line numb
                    gpu1_found = True 
            if (len(js['pattern'])) > 4:            # if 3rd gpu pattern
                if patt[4].search(line) != None:          # GPU2 pattern,
                    pat_occur_t4.append((linenum, line.rstrip('\n'))) # strip linebreaks, store line and line numb
                    gpu2_found = True

        if (js["clearlog"]):
            in_file.truncate(0)                             # clear file

        for linenum, line in pat_occur_t0:              # logtime & uptime & energy
            line_asc = remove_non_number(line)
            #print("line2_asc= ",line_asc)
            logtime.append(line_asc[1:3])
            uptime.append(line_asc[4:6])
            energy.append(line_asc[7].rstrip("kWh"))

        for linenum, line in pat_occur_t1:              # logtime & uptime & energy
            line_asc = remove_non_number(line)
            #print("line3_asc= ",line_asc)
            algo.append(line_asc[2])
            if(algo != None):
                algo_read_save(js['algofile'], algo[-1])
                #print("algo-1= ", algo[-1])
    

        for linenum, line in pat_occur_t2:              # GPU0
            line_h = remove_fan_hundert(line)
            line_asc = remove_non_number(line_h)       
            if (removestr0) in line_asc:
                del line_asc[4]
            id0.append(line_asc[2])
            gpu0.append(line_asc[3])
            temp0.append(int(line_asc[4]))
            fan0.append(int(line_asc[6]))
            speed0.append(float(line_asc[8])/1.0)
            share0.append(line_asc[10])
            core0.append(int(line_asc[11]))
            mem0.append(int(line_asc[12]))
            power0.append(int(line_asc[13]))
            eff0.append(float(line_asc[15])/1.0)
            
        
        for linenum, line in pat_occur_t3:              # GPU1
            line_h = remove_fan_hundert(line)
            line_asc = remove_non_number(line_h)
            if (removestr1) in line_asc:
                del line_asc[4]
            id1.append(line_asc[2])
            gpu1.append(line_asc[3])
            temp1.append(int(line_asc[4]))
            fan1.append(int(line_asc[6]))
            speed1.append(float(line_asc[8])/1.0)
            share1.append(line_asc[10])
            core1.append(int(line_asc[11]))
            mem1.append(int(line_asc[12]))
            power1.append(int(line_asc[13]))
            eff1.append(float(line_asc[15])/1.0)
        

        for linenum, line in pat_occur_t4:              # GPU2
            line_h = remove_fan_hundert(line)
            line_asc = remove_non_number(line_h)
            if (removestr2) in line_asc:
                del line_asc[4]
            id2.append(line_asc[2])
            gpu2.append(line_asc[3])
            temp2.append(int(line_asc[4]))
            fan2.append(int(line_asc[6]))
            speed2.append(float(line_asc[8])/1.0)
            share2.append(line_asc[10])
            core2.append(int(line_asc[11]))
            mem2.append(int(line_asc[12]))
            power2.append(int(line_asc[13]))
            eff2.append(float(line_asc[15])/1.0)
        
    
    alg = algo_read_save(js['algofile'],'')
    
    #print("alg=", alg)
    #print("logtime= ", logtime)
    #print("Uptime= ", uptime)
    #print("energy=", energy)
    
    #print("Temp0= ", temp0)
    #print("Temp1 = ", temp1)
    #print("Temp2 = ", temp2)
    
    #print("fan0= ", fan0)
    #print("fan1= ", fan1)
    #print("speed0= ", speed0)
    #print("speed1= ", speed1)
    #print("share0= ", share0)   
    #print("share1= ", share1)
    #print("core0= ", core0)
    #print("core1= ", core1)
    #print("mem0= ", mem0)
    #print("mem1= ", mem1)
    #print("power0= ", power0)
    #print("power1= ", power1)
    #print("effi0= ", eff0)
    #print("effi1= ", eff1)
        

    if (js["plot_graph"]):
        #Temp
        plt.plot(temp0)
        plt.plot(temp1)
        plt.plot(temp2)
        plt.xlabel("Time")
        plt.ylabel("GPU Temp")
        plt.ylim(60,90)
        plt.show()  
        #Fan
        plt.plot(fan0)
        plt.plot(fan1)
        plt.plot(fan2)
        plt.xlabel("Time")
        plt.ylabel("Fan %")
        plt.ylim(40,100)
        plt.show()
  
    if (js["insertDB"]):         
        if(gpu0_found):
            insert_varibles_into_table(user, alg, str(gpu0[-1]), str(temp0[-1]), str(fan0[-1]), str(speed0[-1]), str(share0[-1]), str(core0[-1]), str(mem0[-1]), str(power0[-1]), str(eff0[-1]), str(logtime[-1]), str(uptime[-1]), str(energy[-1]), str(id0[-1]))
            #print("gpu0_found=", gpu0_found)
        if(gpu1_found):
            insert_varibles_into_table(user, alg, str(gpu1[-1]), str(temp1[-1]), str(fan1[-1]), str(speed1[-1]), str(share1[-1]), str(core1[-1]), str(mem1[-1]), str(power1[-1]), str(eff1[-1]), str(logtime[-1]), str(uptime[-1]), str(energy[-1]), str(id1[-1]))
            #print("gpu1_found=", gpu1_found)
        if(gpu2_found):
            insert_varibles_into_table(user, alg, str(gpu2[-1]), str(temp2[-1]), str(fan2[-1]), str(speed2[-1]), str(share2[-1]), str(core2[-1]), str(mem2[-1]), str(power2[-1]), str(eff2[-1]), str(logtime[-1]), str(uptime[-1]), str(energy[-1]), str(id2[-1]))
            #print("gpu2_found=", gpu2_found)


except FileNotFoundError:                   # If log file not found,
    print("Log file not found.")                # print an error message. 		
    
finally:
    if in_file is not None:
       in_file.close()    
    
   
