from asyncio import subprocess
import asyncio
import fcntl
import logging
from pathlib import Path
import pty
import os
from tempfile import TemporaryDirectory

logger = logging.getLogger(__name__)

RECORDING_FILE = 'term_recording'
VIM_FILE = 'vim_file'

def get_docker_command(shared_dir, vim_image_name='vim'):
    cmd = ["docker", "run",'--rm', '--workdir', '/data', '-v',f'{shared_dir}:/data', "-it", "--entrypoint", "ash", vim_image_name]
    return cmd

async def record_vim_terminal(input_data, self_terminate=True):
    """
    Execute the given command as a subprocess, providing the input data to stdin.

    The vim input should leave the input in normal mode.
    
    Parameters:
    - input_data: The VIM key command sequence to record
    - self_terminate: wether a wq should be injected after running the input
    
    Returns:
    - output: The asciicast formatted temrinal recording
    """

    pty_master, pty_slave = pty.openpty()
    shared_directory = TemporaryDirectory()
    command = get_docker_command(shared_directory.name)

    logger.info(f"Running docker commmand: {' '.join(command)}")
    
    # Execute the command, provide the input, capture the output
    process = await subprocess.create_subprocess_exec(
        *command,
        text=False, stdout=pty_slave, stdin=pty_slave)
    
    os.write(pty_master, f"""termrec -f asciicast -e 'vim -n {VIM_FILE}' {RECORDING_FILE}\n""".encode())
    fcntl.fcntl(pty_master, fcntl.F_SETFL, os.O_NONBLOCK)

    f = os.fdopen(pty_master, "w")

    for c in input_data:
        print(c)
        await asyncio.sleep(0.5)
        if process.returncode is not None: raise ValueError()
        # os.write(pty_master, c.encode())
        print(c, flush=True, file=f, end='')
    # f.close()    

    if self_terminate:
        # TODO: maybe just kill the vim process? then no extra chars are recorded
        # and there would be no final state requirements for the vim process.
        # Not clear how to do that.
        os.write(pty_master, ':wq\n'.encode())

    await asyncio.sleep(0.2)
    os.write(pty_master, b'exit\n')

    while True:
        try:
            data = os.read(pty_master, 1024)
        except OSError:
            break
        if not data:
            break

    await asyncio.sleep(0.2)
    process.terminate()

    await process.wait()
    output = (Path(shared_directory.name) / RECORDING_FILE).read_text()

    return output