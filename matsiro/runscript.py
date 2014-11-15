import os, sys, re, yaml
from   datetime         import datetime,timedelta

class Runscript(object):
    def __init__(self, yamlPath, Mkinc):

        self.mkinc      = Mkinc
        self.prjDir     = self.mkinc.prjDir
        self.prjName    = self.prjDir.split('/')[-1]

        self.dictConf   = yaml.load( open(yamlPath).read().format(**self.mkinc.dictVar) )


    def gen_runscr(self, prjName):

        Keys        = self.dictConf[prjName]

        fmtFunc     = lambda item,Dict:  "item='%s', "%item \
                                       + ', '.join([ "%s=%s"%(k,v) for k,v in Dict.items() ])

        '''
        isdigit     = lambda value: str(value).replace('E','',1)       \
                                              .replace('e','',1)       \
                                              .replace('D','',1)       \
                                              .replace('d','',1)       \
                                              .replace('-','',2)       \
                                              .replace('.','')       \
                                              .replace(',','').isdigit()

        fmtFunc     = lambda k,v: '%s=%s'%(k,v if isdigit(v) else '"%s"'%v)
        '''

        SYSIN       = []

        for key in Keys:

            if not key in  ['data', 'hist']:
                SYSIN.append(   ' &nm%s '%key
                              + ', '.join( ['%s=%s'%(k,v) for k,v in self.dictConf[key].items()] )
                              + ' &end')

            else:
                SYSIN.extend( [  ' &nm%s '%key
                               + fmtFunc(item,V)
                               + ' &end' for item,V in self.dictConf[key].items() ])


        return SYSIN


    def save(self, setName, sDTime, eDTime=None, delT='y', outDir=None):
        template    = '''
#!/bin/sh
#PBS -q ???
#PBS -l select=?:ncpus=?

MRUN=mpiexec_mpt
GCM={GCM}
TSTAMP='{TSTAMP}'


for tstamp in $TSTAMP
  do
  echo $tstamp
  SYSIN=\
"{SYSIN}"
done
        '''

        getTStamp   = lambda dtime, delT: {'y': dtime.strftime('%Y'),
                                           'm': dtime.strftime('%Y%m'),
                                           'd': dtime.strftime('%Y%m%d')}[delT]

        eDTime      = nxtDTime( sDTime, delT )  if eDTime == None   else    \
                      eDTime

        TSTAMP      = []
        while sDTime < eDTime:

            TSTAMP.append( getTStamp( sDTime, delT ) )
            sDTime      += timedelta( days=self.nDays(TSTAMP[-1]) )

        sTSTAMP     = ' '.join(TSTAMP)
        sGCM        = self.mkinc.replace( self.mkinc['root']['GCM'] )
        sSYSIN      = '\n'.join(self.gen_runscr('default'))

        print template.format(**{'GCM':sGCM,
                                 'TSTAMP':sTSTAMP,
                                 'SYSIN':sSYSIN,
                                 })
        sys.exit()


        if outDir == None: outDir = self.mkinc.dictVar['runscrDir']
        if not os.path.exists( outDir ):    os.makedirs(outDir)

        outFName    = '%s.%s'%( self.prjName,setName )
        outPath     = os.path.join( outDir, outFName )

        outFile     = open( outPath, 'w' )

        outStr      = '\n'.join( self.gen_runscr( setName ) )

#        print outStr
#        print 'need to implement writing routine'


    def nDays(self,YYYYMM):
        if len(YYYYMM) == 6:
            year    = int(YYYYMM[:4]);  mon   = int(YYYYMM[4:6])
            year1   = year+1 if mon == 12 else year
            mon1    = 1      if mon == 12 else mon+1

            return (datetime(year1,mon1,1)-datetime(year,mon,1)).days

        elif len(YYYYMM) == 4: return (datetime(int(YYYYMM)+1,1,1)-datetime(int(YYYYMM),1,1)).days
        else                 : return 1     # for yyyymmdd; delT='d'


def main():
    rs=Runscript('agcm5.6GW')

    scr     ='\n'.join( rs.gen_runscr(rs.default) )

    print rs.save(datetime(2000,1,1))
    print rs.save(datetime(2000,2,1),delT='m')
    sys.exit()


    runName     = 'TESTRUN'
    Year        = 2000
    eYear       = 2001
    outDir      = '/data1/hjkim/MODEL/bin/%s.%i'%(runName,Year)

    dictVar = {'forcingDir' : '/data1/hjkim/ELSE/GSWP3/in/BETA0711/',
               'fixparaDir' : '/data1/hjkim/ELSE/agcm5.6GW/expara/' ,
               'initPath'   : os.path.join(outDir,'Initial'),
               'rstPath'    : os.path.join(outDir,'Restart'),
               'runName'    : runName,
               'sDTime'     : '%i,1,1,0,0,0'%Year,
               'eDTime'     : '%i,1,1,0,0,0'%eYear,
               'Year'       : Year,
               }
    print scr.format(**dictVar)

if __name__ == '__main__':
    main()
