import os
import re
import pathlib

class module_generator:

    def __init__( self, repo_path, version ):
        '''
        repo_path: root of the epcc spack repo
        version: version of the module to install
        '''
        
        self.repo_path=repo_path
        self.version=version

    def _write_generic_module(self,template, module_file):
        ''' Generate modules for spack and write them to files.
        template: path of the template file used to generate the module
        module_file: File where to write the generated module
        '''

        with open(template) as f:
            lines=f.readlines()
            for i,line in enumerate(lines):
                lines[i]= re.sub(r"__EPCC__SPACK__REPO__ROOT__",self.repo_path,line)
                lines[i]= re.sub(r"__EPCC__VERSION__",str(self.version),lines[i])
        
        with open(module_file,"w+") as f:
            f.writelines(lines)




class spack_module_generator(module_generator):
    
    def write_module(self, output="."):
        pathlib.Path(output).mkdir(exist_ok=True,parents=True)
        template=os.path.join(self.repo_path, "scripts","tools","templates","spack.template.lua")
        module_file=os.path.join(output,"epcc-config-" + self.version + ".lua")
        self._write_generic_module(template,module_file)


class cse_env_module_generator(module_generator):

    def write_module(self,output="."):
        pathlib.Path(output).mkdir(exist_ok=True,parents=True)
        template=os.path.join(self.repo_path, "scripts","tools","templates","cse_modules.template.lua")
        module_file=os.path.join(output, self.version  + ".lua")
        self._write_generic_module(template,module_file)
    