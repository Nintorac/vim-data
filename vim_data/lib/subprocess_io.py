from asyncio.subprocess import PIPE
from asyncio import subprocess
import asyncio
from collections import deque
import os
from tqdm import tqdm

async def run_subprocess_with_input(command, input_data):
    """
    Execute the given command as a subprocess, providing the input data to stdin.
    
    Parameters:
    - command: List of program arguments. The program to execute is the first item.
    - input_data: Data (str or bytes) to send to the subprocess's stdin.
    
    Returns:
    - output: The subprocess's stdout data
    """

    if isinstance(input_data, str):
        # If the input data is in string format, encode it to bytes
        input_data = input_data.encode()
    
    proc, *args = command
    # Execute the command, provide the input, capture the output
    process = await subprocess.create_subprocess_exec(proc, *args,
                            text=False, stdout=PIPE, stdin=PIPE,)
    
    
    output, _ = await process.communicate(input_data)
    
    return output

async def run_subprocesses_with_batch_input(command, data, max_queue_size=10, disable_tqdm=None):
    """
    Runs a batch of subprocesses with their respective input data asynchronously,
    using a deque with a configurable max size to limit the number of concurrent subprocesses.
    
    Maintains the ordering of the input data
    
    Parameters:
    - command: List of program arguments. The program to execute is the first item.
    - data: Iterable of input data
    - max_queue_size: Maximum size of the queue

    Returns:
    - outputs: A list of outputs from each subprocess
    """
    disable_tqdm = disable_tqdm or os.environ.get('DISABLE_TQDM') or True
    tasks = deque()  # Initialize the deque for storing tasks
    results = []  # List to store results as they are completed

    t = tqdm(total=len(data))

    for input_data in data:
        # If the deque reaches max size, remove and await the left-most (oldest) task to free space
        if len(tasks) >= max_queue_size:
            done_task = tasks.popleft()  # Remove the oldest task
            results.append(await done_task)  # Await its completion and store its result
            t.update(1)
            
        # Add a new task to the deque
        task = asyncio.create_task(run_subprocess_with_input(command, input_data))
        tasks.append(task)

    # After processing all input data, await completion of all remaining tasks in the deque
    results.extend(await asyncio.gather(*tasks))

    return results
