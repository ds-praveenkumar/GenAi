import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from rich.console import Console
from rich.markdown import Markdown

console = Console()

def show(content):
    
    if len(content) > 2:
        md = Markdown( content) 
        console.print(md)
        
