# !/usr/bin/python
# -*- coding: utf-8 -*-

import re
import time
from os import popen
from sys import argv
from optparse import OptionParser, OptionGroup

def checkPlatform(vendor):
    for i in log_dict[vendor]["type"]:
        if i is not None:
            for j in log_dict[vendor][str(i)]:
                check_command(i, j, ip_addr, user, pwd)

    print 'Configuration Valid(byte1):'
    print "-" * 65
    a = [len(log_dict[vendor][str(i)]) for i in range(7)]
    b = 0
    c = 0
    for j in a:
        b = c
        c += j
        print first_data[b:c]

    print 'Configuration Value(byte3):'
    print "-" * 65 
    a = [len(log_dict[vendor][str(i)]) for i in range(7)]
    d = 0
    e = 0
    for i in a:
        d = e
        e += i
        print third_data[d:e]

    print "Configuration Valid(byte1='01')"
    print "-" * 65
    for i in ls:
        print i

    print "Check Romote Modify Status"
    if first_data.count("01") in range(2,40,2):
        print "Remote modify config success!"
    else:
        print "Remote modify config failed."

def set_command(type1,offset,data):
    set_cmd = "ipmitool -H {2} -U {3} -P {4} raw 0x38 0x12 {0} {1} {5} 1 2>/dev/null". \
        format(type1, offset, ip_addr, user, pwd, data)
    popen(set_cmd)
    time.sleep(5)

    cmd = "ipmitool -H {2} -U {3} -P {4} raw 0x38 0x11 {0} {1} 2>/dev/null". \
        format(type1, offset, ip_addr, user, pwd)
    num = popen(cmd[:60]).read().split()[int(offset) + 2]
    print "byte3 result:%s" % num
    data1 = '0' + str(data) 
    
    if num != 'ff' and num == data1:
        print "byte3 modify success"
    else:
        print "byte3 modify failed."        

def set_info():
    n = int(input("enter the set times:"))
    for i in range(n):
        type1 = raw_input("the first number(type)：")
        offset = raw_input("the second number(offset)：")
        data = raw_input("the third number(data)：")
        set_command(type1,offset,data)

def check_command(i, j, ip_addr, user, pwd):
         
    cmd = "ipmitool -H {2} -U {3} -P {4} raw 0x38 0x11 {0} {1}    2>/dev/null". \
        format(i, j, ip_addr, user, pwd)

    result = popen(cmd).read().strip()
    data = re.sub("\n", '', result)
    log = data[:2]
    if j != "0xff":
        log1 =data[6:]
    else:
        log1 = data[6:]
    first_data.append(log)
    third_data.append(log1) 
    
    if log == '01':
        ls.append(cmd[:63])

if __name__ == '__main__':

    # define global variables
    ls = []
    first_data = []
    third_data = []
    script = __file__

    # parse arguments
    usage = 'Usage: %prog [Option] host'
    parser = OptionParser(usage=usage)
    parser.add_option('-H', '--host',default='192.168.2.11',
                      dest='ip', action='store',
                      help='set remote IP ')
    parser.add_option('-U', '--user',
                      dest='ur', action='store', default='ADMIN',
                      help='set remote USER (default=ADMIN)')
    parser.add_option('-P', '--password',
                      dest='pw', action='store', default='ADMIN',
                      help='set remote PASSWORD (default=ADMIN)')
    parser.add_option('-V', '--vendor',
                      dest='vd', action='store', default='intel',
                      help='set remote vendor (default=intel) ')
    group1 = OptionGroup(parser,
                         "Case1", 
                         "python {0} -H 192.168.2.11 ".format(script))

    parser.add_option_group(group1)
    options, args = parser.parse_args()
    opt_dict = eval(str(options))
    user = options.ur
    pwd = options.pw
    vendor = options.vd

    # check ip address
    ip_addr = options.ip
    if not ip_addr:
        print "Invalid host IP, Try '-h/--help' for more information."
        raise SystemExit(-1)

    with open('data/parameter.json') as jrf:
        log_dict = eval(jrf.read())

    set_info()
    checkPlatform(vendor)

    print """
        Choose List:
        1 - Enter BIOS Setup
        2 - Test done
        """
    num = raw_input("enter the bios (1:yes 2:no)：")

    # enter the bios or quit script
    if num == "1":
        bios_cmd = "ipmitool  –I lanplus  –H {0}  –U {1}  –P {2}  chassis  bootdev  bios"
        popen(bios_cmd.format(ip_addr, user, pwd))
        reset_cmd = "ipmitool  –I lanplus  –H {0}  –U {1}  –P {2}  chassis  power  reset"
        popen(reset_cmd.format(ip_addr, user, pwd))
    else:
        print 'Test done'


