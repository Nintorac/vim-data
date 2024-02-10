#%%
from asyncio.subprocess import PIPE
from asyncio import subprocess
import asyncio
from collections import deque
from tqdm import tqdm

from vim_data.lib.subprocess_io import run_subprocesses_with_batch_input
# Example usage
if __name__ == "__main__":
    cmd = ["docker", "run", "-i", "vim"]
    input_str = "ihello world{i}\033:wq\n"
    
    output = await run_subprocesses_with_batch_input(cmd, [input_str.format(i=i) for i in range(100)])
    for o in output:
        print(o)