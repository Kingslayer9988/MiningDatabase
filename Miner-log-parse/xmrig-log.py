# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 15:37:47 2018

@author: mzell & kingslayer
"""
import matplotlib.pyplot as plt
import re
import mysql.connector
import json
import subprocess

def remove_non_number(text):
   a = re.sub(r'\x1b(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])',' ', text)
   b = re.sub(' +',' ',a)
   c = b.split(" ")
   #print(c)
   #print("len=",len(c))
   return (c)
    
def remove_fan_hundert(text):
   return re.sub(r'm100 %','m 99 %', text)

def insert_varibles_into_table(user, algo, cpu, temp, speed_t, speed10s, speed60s, speed15m, logtime, speedmax, diff):
    try:
        connection = mysql.connector.connect(host='DATABASE-IP OR DYNDNS',
                                             database='DATABASE-NAME',
                                             user='USER',
                                             password='PASSW0RD',
					     ssl_cert='ca-cert.pem',
                                             ssl_key='ca-key.pem')
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO xmrig_cpu (user, algo, cpu, temp, speed_t, speed10s, speed60s, speed15m, logtime, speedmax, diff) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """

        record = (user, algo, cpu, temp, speed_t, speed10s, speed60s, speed15m, logtime, speedmax, diff)
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
               print("cpu_parse.json file not found.")                # print an error message. 		
                    
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
   

def read_cpu_temp(file):
    try:                              # Try to:
        with open(file, 'rt') as f:
            # Read the results, and converted to an integer
            temp = int(f.read()) / 1000
            return(temp)
                                
    except FileNotFoundError:                   # If log file not found,
        print("cpu temp file not found.")                # print an error message. 		
                    
    finally:
        if f is not None:
            f.close()    


patt = []
pat_occur_t0 = []
pat_occur_t1 = []
#pat_occur_t2 = []
#pat_occur_t3 = []


logtime =[]
speed_t = []
speed10s = []
speed60s = []
speed15m = []
speedmax =[]

diff = []
algo = []


try:                              # Try to:

    js = read_json_config("PATH/TO/xmrig_log.json")


    #User Kennung
    user = js['username']
       
    #build pattern lines
    for i in range(len(js['pattern'])):
        patt.append(re.compile(r'%s' % js['pattern'][i], re.IGNORECASE))
    
   
    
    with open (js['logfilename'], 'r+') as in_file:        # open file for reading text.
            
        for linenum, line in enumerate(in_file):        # Keep track of line numbers. 
            if patt[0].search(line) != None:          # If substring search finds a match,
                pat_occur_t0.append((linenum, line.rstrip('\n'))) # strip linebreaks, store line and line number in list as tuple.
            if patt[1].search(line) != None:          # If substring search finds a match,
                pat_occur_t1.append((linenum, line.rstrip('\n'))) # strip linebreaks, store line and line numb
            '''
            if patt[2].search(line) != None:          # If substring search finds a match,
                pat_occur_t2.append((linenum, line.rstrip('\n'))) # strip linebreaks, store line and line numb
            if patt[3].search(line) != None:          # If substring search finds a match,
                pat_occur_t3.append((linenum, line.rstrip('\n'))) # strip linebreaks, store line and line numb
            '''

        if (js["clearlog"]):
            in_file.truncate(0)                             # clear file

        for linenum, line in pat_occur_t0:              # CPU miner ...speed
            line_asc = remove_non_number(line)       
            #print("line0_asc= ",line_asc)
            logtime.append(line_asc[0] + ', ' + line_asc[1])
            speed_t.append(line_asc[4])
            speed10s.append(line_asc[5])
            speed60s.append(line_asc[6])
            speed15m.append(line_asc[7])
            speedmax.append(line_asc[10])
            #energy.append(line_asc[7].rstrip("kWh"))
            
           
        for linenum, line in pat_occur_t1:              # CPU net ...algo
            line_asc = remove_non_number(line)
            #print("line1_asc= ",line_asc)
            diff.append(int(line_asc[8]))
            algo.append(line_asc[10])
            
    if(js['freebsd']):
        bsdtemp = subprocess.check_output("sysctl -a |grep temperature", shell=True, universal_newlines=True)
        #bsdtemp = "dev.cpu.15.temperature: 70.1C\ndev.cpu.14.temperature: 70.1C\ndev.cpu.13.temperature: 70.1C\ndev.cpu.12.temperature: 70.1C\ndev.cpu.11.temperature: 70.1C\ndev.cpu.10.temperature: 70.1C\ndev.cpu.9.temperature: 70.1C\ndev.cpu.8.temperature: 70.1C\ndev.cpu.7.temperature: 70.1C\ndev.cpu.6.temperature: 70.1C\ndev.cpu.5.temperature: 70.1C\ndev.cpu.4.temperature: 70.1C\ndev.cpu.3.temperature: 70.1C\ndev.cpu.2.temperature: 70.1C\ndev.cpu.1.temperature: 70.1C\ndev.cpu.0.temperature: 70.1C"
        find = bsdtemp.find("dev.cpu.2.temperature:")
        temp= (bsdtemp[find-7:find-2]).lstrip()
    else:
        temp = read_cpu_temp(js['cputempfile'])

     #temp = 33
    
    cpu = js['cputype']

    print("temp= ",temp)
    #print("cpu= ", cpu)
    
    #print("logtime= ", logtime[-1])
    #print("algo=", algo[-1])
    #print("diff=", diff[-1])
    #print("speed_t= ", speed_t[-1])
    #print("speed10s= ", speed10s[-1])
    #print("speed60s= ", speed60s[-1])
    #print("speed15m= ", speed15m[-1])
    #print("speedmax= ", speedmax[-1])
            

    if (js["plot_graph"]):
        #speed10s
        plt.plot(speed10s)
        plt.xlabel("Time")
        plt.ylabel("Speed10s")
        plt.show()  
        
  
    if (js["insertDB"]):         
        insert_varibles_into_table(user, str(algo[-1]), str(cpu), str(temp), str(speed_t[-1]), str(speed10s[-1]), str(speed60s[-1]), str(speed15m[-1]), str(logtime[-1]), str(speedmax[-1]), str(diff[-1]))
                                #(user, algo, cpu, temp, speed_t, speed10s, speed60s, speed15m, logtime, speedmax, diff)

except FileNotFoundError:                   # If log file not found,
    print("Log file not found.")                # print an error message. 		
    
finally:
    if in_file is not None:
       in_file.close()    
    
   
