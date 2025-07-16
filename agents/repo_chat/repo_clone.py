#===============================================================================
#  File Name    : repo_clone.py
#  Project Name : 

#  Description  : 
#    Description of this file

#  Author       : Praveen Kumar
#  Created On   : 2025-07-13
#  Last Updated : 2025-07-13
#  Version      : v1.0.0

#  Language     : Python
#  File name    : repo_clone.py
#  Dependencies : 
#    - gitpython


#  Inputs       : Expected inputs
#  Outputs      : Expected outputs
#  Usage        : 
#    Example usage

#  Notes        : 
#    - clone repo from repo url
#===============================================================================
import sys 
sys.path.append('.')
from git import Repo
from src.infrastructure.llm.gemini_llm import GeminiLLM

def clone_repo( repo_url : str ):
    repo_dir = './tmp/onemoretech'
    repo = Repo.clone_from(repo_url,
                          repo_dir ,
                           branch='main')
    print(repo.branches)
    print( f"repo downloaded : {repo_dir}")
    
if __name__ == '__main__':
    llm = GeminiLLM()
    git_url = 'git@github.com:marlaman/self-healing-agent.git'
    clone_repo(git_url)
    print(llm.invoke("hi" ))