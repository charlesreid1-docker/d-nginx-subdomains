import glob
import os
import subprocess

"""
Clean d-nginx-subdomains conf.d directory


This script cleans out the conf.d directory
in the d-nginx-subdomains repo.

This script should be run before you generate a new set
of config files from the nginx config file templates in
d-nginx-subdomains/conf.d_templates/

This script cleans out all the config files in the folder
d-nginx-subdomains/conf.d/

That way there are no old config files to clash with the
new ones.
"""

HERE = os.path.abspath(os.path.dirname(__file__))
CONF = os.path.abspath(os.path.join(HERE,'..','conf.d'))

for f in glob.glob(os.path.join(CONF,"*.conf")):
    if os.path.basename(f)!="_.conf":
        cmd = ['rm','-fr',f]
        subprocess.call(cmd)

