import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from rich.console import Console
from rich.markdown import Markdown

console = Console()

def show(content, color="bold magenta"):
    
    if len(content) >= 2:
        md = Markdown( content) 
        console.print(md, style=color)
        
def print_console(text, color="bold magenta"):
    if len(text) >= 2:
        console.print(text, style=color)
    
    