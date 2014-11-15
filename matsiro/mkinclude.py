import os, re
import yaml


class Mkinclude(object):
    def __init__(self, yamlPath, prjDir='./'):

        self.prjDir     = prjDir

        self.dictVar    = {'prjDir':self.prjDir}
        self.dictConf   = yaml.load( open(yamlPath).read().format(**self.dictVar) )


    def __getitem__(self,k):
        return self.dictConf[k]

    def check(self):
        ##
        # chenk NMPE and nLat (can be devided?)
        # check min NMPE and HRESOLUTION (one > 4?, hlf >= 10)
        return


    def gen_mkinc(self, prjName):

        dictConf    = dict((k, "" if v == None else v) for k,v in self.dictConf[prjName].items())
        Keys        = dictConf.pop('__order__')#,0)


        fmtFunc     = {'include': lambda k,V: '\n'.join( ['%s %s'%(k,v) for v in V] )
                        }

        MKINC       = [ '%s = %s'  %(key,dictConf[key]) if not key in fmtFunc else
                        fmtFunc[key](key,dictConf[key])
                                    for key in Keys]

        return MKINC

    '''
    #DUNNO WHY DOES NOT WALK DOWN TO ALL THE ELEMENTS
    def search(self, Dict, Key):
        if Key in Dict: return Dict[Key]
        for key,value in Dict.items():
            print Key, key
            if isinstance(value,dict):
                return self.search(value, Key)

        return False
    '''

    def search(self, Dict, Key):
        # only search for depth 1
        for key, value in Dict.items():
            if Key in value:    return value[Key]

        return False


    def replace(self, sItem):
        while '$(' in sItem:
            keyword = re.findall('\$\(.+?\)',sItem)[0][2:-1]

            replace = self.search( self.dictConf, keyword )

            sItem   = sItem.replace( '$(%s)'%keyword, replace)

        return sItem


    def save(self, prjName, outPath=None):
        outDir      = self[prjName]['__locate__']

        outPath     = os.path.join( outDir, 'Mkinclude' ) if outPath == None else   \
                      outPath

        outFile     = open( outPath, 'w' )

        outStr      = '\n'.join( self.gen_mkinc(prjName) )

        outFile.writelines(outStr)


if __name__=='__main__':

    mkinc   = Mkinclude('/data1/hjkim/MODEL/conf/agcm5.6GW.mkinc', '/data1/hjkim/MODEL/MAT_1deg/')

    print mkinc.gen_mkinc('root')
