import subprocess
import locale

# set locale for a 24 hour timestamp
locale.setlocale(locale.LC_TIME, 'POSIX')

def __run(command):
    'Used to run a system command and return the results'
    
    # subprocess takes a list as command input
    if type(command) == str:
        command = command.split()
    
    # create a process using our command    
    process = subprocess.Popen(command, shell=False,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # get our status return code and results
    status = process.wait()
    output = process.communicate()
    if status == 0:
        return output[0]
    else:
        raise Exception(output[1])

def __getbin(sarbin, saroptions):
    'Creates a sar command to be ran'
    sarcommand = 'LC_TIME="POSIX" %s' % sarbin
    if saroptions:
        sarcommand = '%s %s' % (sarcommand, saroptions)
         
    results = __run(sarcommand)
    return __interrupt(results)
    
def __getfile(sarbin, saroptions, sarfile):
    'Uses input file to perform sar'
    sarcommand = 'LC_TIME="POSIX" %s -f %s' % (sarbin, sarfile)
    if saroptions:
        sarcommand = '%s %s' % (sarcommand, saroptions)
        
    results = __run(sarcommand)
    return __interrupt(results)
    
def __interrupt(saroutput):
    'interrupts the sar output and returns in a nice format'
    results = saroutput.split('\n')
    # remove our header and first blank line
    header = results.pop(0)
    results.pop(0)
    
    # sar report need at least 3 lines to parse data
    if len(results) > 3:
        keys = results.pop(0).split()
        keys[0] = 'timestamp' # rename actual timestamp with a key name
    else:
        raise Exception('''Sar Output does not appear to be over 5 lines,
                        this means not enough data to run report''')

    # create a list of dicts for our data
    output = []
    for line in results:
        if line != '': # skip blank lines
            if line.split()[1:] != keys[1:]: # skip header lines
                if line.split()[0] != 'Average:': # skip the end average
                    data = line.split()
                    
                    # be sure our key and data are the same length
                    if len(keys) != len(data):
                        raise Exception("Keys and data are not of the same length")
    
                    d = {}                    
                    for i in range(len(data)):
                        d[keys[i]] = data[i]
                    output.append(d)
    return output

def sar(sarbin=None, saroptions=None, sarfile=None):
    'Entry point for running sar, or reading sar log file'
    if sarfile and sarbin:
        __getfile(sarbin, saroptions, sarfile)
    elif sarbin:
        __getbin(sarbin, saroptions)
    else:
        raise Exception('Missing required inputs')