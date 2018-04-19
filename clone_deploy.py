import subprocess
import os

onepagers = {
    'pages.charlesreid1.com' : 'https://git.charlesreid1.com/charlesreid1/pages.charlesreid1.com',
    'hooks.charlesreid1.com' : 'https://git.charlesreid1.com/charlesreid1/hooks.charlesreid1.com',
    'bots.charlesreid1.com' :  'https://git.charlesreid1.com/charlesreid1/bots.charlesreid1.com'
}

for name in onepagers:
    url = onepagers[name]
    work_dir = os.path.join("/www",name,"htdocs")
    git_dir =  os.path.join("/www",name,"git")
    clonecmd = ["git","--separate-git-dir=%s"%(git_dir),"clone",url,work_dir]


