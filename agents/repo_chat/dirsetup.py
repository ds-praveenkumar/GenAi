#===============================================================================
#  File Name    : init.py
#  Project Name : Project Name
#  Description  : 
#    Description of this file

#  Author       : Praveen Kumar
#  Created On   : 2025-07-10
#  Last Updated : 2025-07-10
#  Version      : v1.0.0

#  Language     : Python
#  File name    : init.py
#  Dependencies : 
#    - Dependency 1
#    - Dependency 2

#  Inputs       : Expected inputs
#  Outputs      : Expected outputs
#  Usage        : 
#    Example usage

#  Notes        : 
#    - Notes or TODOs
#===============================================================================
import os
from pathlib import Path 

class ProjectDirSetup:
    def __init__( self):
        self.l1dir = ['.github','static', 'data','k8s', 'experiments', 'src', 'tools','tests' ,'agents', ]
        self.l2dir = {
            'src': ['application', 'core', 'infrastructure']       
                      }
        
    def run( self):
        for item in self.l1dir:
            os.makedirs( item, exist_ok=True)
            print(f"Path created: {item}")
            if item in self.l2dir.keys():
                for sub_dir in self.l2dir[item]:
                    dir_path = Path(item) / sub_dir
                    os.makedirs(dir_path.as_posix(), exist_ok=True )
                    print( f"Path created : {dir_path}")
                    
                    
if __name__ == "__main__":
    ps = ProjectDirSetup()
    ps.run()