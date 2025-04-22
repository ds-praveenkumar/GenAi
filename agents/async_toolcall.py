from langchain_core.tools.structured import StructuredTool
from pydantic import  BaseModel
import asyncio

class ToolArgs(BaseModel):
    a : int
    b : int
    
async def multiply(a: int, b: int):
    # await asyncio.sleep(1)
    return  a * b

def dummy():
    return "Test function"

async_tool = StructuredTool.from_function(
    name='multiplyer',
    description="multiplies two numbers",
    func=dummy,
    coroutine=multiply,
    args_schema=ToolArgs
)

async def main():
    result = await async_tool.ainvoke({"a": 2, "b": 4})
    print(result)

asyncio.run(main())