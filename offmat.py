#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : offmat.py
# CREATED BY : hjkim @IIS.2014-11-01 16:53:10.586993
# MODIFED BY :
#
# USAGE      : $ ./offmat.py modelName command outDir
#
# DESCRIPTION:
#------------------------------------------------------cf0.2@20120401


import  os,sys,time,shutil
from    datetime        import datetime, timedelta
import  yaml
from    optparse        import OptionParser
#from    cf.util.LOGGER  import *
#from    cf              import settings
from    subprocess      import Popen,PIPE

#from runscript          import Runscript
#from mkinclude          import Mkinclude

from matsiro            import MATSIRO

class CL:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


#@ETA
def main(args,opts):

    print args
    print opts

    prjDir  = args[0]


    if opts.new_prj:
        Matsiro     = MATSIRO(opts.new_prj, 'w', prjDir)

    elif opts.old_prj:
        Matsiro     = MATSIRO(opts.old_prj, 'm', prjDir)

#    Matsiro.compile('dirs')
#    Matsiro.compile('dirs')
#    Matsiro.compile('lib')
    Matsiro.build()

    return


if __name__=='__main__':
    usage   = 'usage: %prog [options] arg'
    version = '%prog 1.0'

    parser  = OptionParser(usage=usage,version=version)

    parser.add_option('-c','--create',action='store',dest='new_prj',
                      help='create a new simulation project')

    parser.add_option('-m','--modify',action='store',dest='old_prj',
                      help='modify an existing simulation project')


    (options,args)  = parser.parse_args()

#    if len(args) == 0:
#        parser.print_help()
#    else:
#        main(args,options)

#    LOG     = LOGGER()
    main(args,options)


