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

from runscript          import Runscript
from mkinclude          import Mkinclude

class CL:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


class MATSIRO(object):
    def __init__(self, modVer, mode, prjDir):
        self.baseDir= '/data1/hjkim/MODEL'
        self.confDir= os.path.join( self.baseDir, 'conf' )

        self.stdDir = os.path.join( self.baseDir, modVer)

        self.prjDir = os.path.abspath( prjDir )
        self.srcDir = os.path.join(self.prjDir,'src')

        self.prjName= self.prjDir.split('/')[-1]

        os.environ['AGCMDIR']   = self.prjDir       # necessary but can be removed

        mkincPath   = os.path.join( self.confDir, '%s.mkinc'%modVer )
        runscrPath  = os.path.join( self.confDir, '%s.runscr'%modVer )

        self.mkinc  = Mkinclude( mkincPath,  self.prjDir )

        self.mkinc.dictVar      = {'prjDir'    : self.prjDir,
                                   'runscrDir' : os.path.join(self.prjDir,'runscr'),
                                   'forcingDir': os.path.join(self.prjDir,'forcing'),
                                   'fixparaDir': os.path.join(self.prjDir,'fixpara'),
                                   'initPath'  : os.path.join(self.prjDir,'{initPath}'),
                                   'rstPath'   : os.path.join(self.prjDir,'{rstPath}'),
                                   'runName'   :'{runName}',
                                   'sDTime'    :'{sDTime}',
                                   'eDTime'    :'{eDTime}',
                                   'Year'      :'{DTime}',
                                   }

        if mode == 'w':
            print '>>> Copying [%s] model source files from %s'%(modVer, self.stdDir)
            shutil.copytree( self.stdDir, self.prjDir )

            print '>>> Configuring model setup ... [%s]'%os.path.join(self.prjDir,'Mkinclude')
            self.mkinc.save('root')#, self.prjDir)

            print '>>> Configuring model setup ... [%s]'%os.path.join(self.prjDir,'src/proj/offmat','Mkinclude')
            self.mkinc.save('offmat')#, os.path.join(self.prjDir,'src/proj/offmat/'))

#        self.runscr = Runscript( runscrPath, self.mkinc  )

#        self.compile('dirs')
#        self.compile('lib')
#        self.compile('gcm')

#        self.runscr.save( 'default', datetime(2001,1,1), datetime(2010,1,1), delT='y');sys.exit()


    def run(self):
#        self.runscr.qsub(datetime(2000,1,1), qName='C10', nNode=1, nCPU=10, delT='y')
        return


    def build(self):
        self.compile('dirs')
        self.compile('lib')
        self.compile('gcm')


    def compile(self, target):
        os.chdir( self.srcDir )

        print '>>> Compiling [%s] ...'%target,
        Make    = Popen( ['make', target] , stdout=PIPE, stderr=PIPE)

        sTime   = time.time()
        while Make.poll() is None:
            time.sleep(1)
            sys.stdout.write('.')
            sys.stdout.flush()

        out,err=Make.communicate()

        if Make.returncode == 0:    print ' OK! [%5.1fs]'%(time.time()-sTime)
        else                   :    print ' ERROR! [%5.1fs]'%(time.time()-sTime)

        if err:
            print CL.WARNING+'<stderr>'
            print err+CL.ENDC

        if Make.returncode != 0:    raise

        Popen(['ifort','--version'])



