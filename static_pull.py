import subprocess
import os
from static_domains import onepagers

if(os.geteuid()==0):
    print(" ")
    print(" ")
    print("ERROR: This script should not be run as root.")
    print(" ")
    print(" ")
    exit(1)


if( os.path.isdir('/www') is False ):
    print(" ")
    print(" ")
    print("ERROR: The /www directory does not exist.")
    print(" ")
    print(" ")
    exit(1)



for name in onepagers:
    url = onepagers[name]

    basedir = os.path.join("/www",name)
    pullcmd = ["git","-C",basedir,"--git-dir=git","--work-tree=htdocs","pull","origin","gh-pages"]

    if( os.path.isdir( os.path.join(basedir,"git") is False ) 
     or os.path.isdir( os.path.join(basedir,"htdocs")) is False ):
        print(" ")
        print(" ")
        print("ERROR: The directories /www/%s/git and /www/%s/htodcs"%(name,name))
        print(" do not exist. Use the static_clone.py script instead. ")
        print(" ")
        exit(1)

    print(" ")
    print("About to run the command:")
    print("    $ " + " ".join(pullcmd))
    print(" ")
    response = input('Okay to proceed? (y/n) ')
    if(response=='y' or response=='Y' or response=='yes'):
        subprocess.call(pullcmd)


