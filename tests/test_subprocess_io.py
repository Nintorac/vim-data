import asyncio
import pytest
from vim_data.lib.subprocess_io import run_subprocess_with_input, run_subprocesses_with_batch_input


@pytest.mark.asyncio
async def test_run_subprocess_with_vim_input():
    cmd = ["docker", "run", "-i", "vim"]
    input_str = "ihello world{i}\033:wq\n"
    
    output = await run_subprocess_with_input(cmd, input_str.format(i=0))
    assert output.decode() == 'hello world0\n'

@pytest.mark.asyncio
async def test_run_subprocessses_with_vim_inputs():
    cmd = ["docker", "run", "-i", "vim"]
    input_str = "ihello world{i}\033:wq\n"
    input_strs = [input_str.format(i=i) for i in range(10)]
    outputs = await run_subprocesses_with_batch_input(cmd, input_strs, 2)
    decoded_outputs = [output.decode() for output in outputs]
    assert decoded_outputs == [f'hello world{i}\n' for i in range(10)]


@pytest.mark.asyncio
async def test_run_subprocess_with_input():
    command = ['cat']
    input_data = "Hello World"
    output = await run_subprocess_with_input(command, input_data)
    
    # Since 'echo' returns the input and subprocess returns bytes, decode it
    assert output.decode().strip() == input_data

@pytest.mark.asyncio
async def test_run_subprocesses_with_batch_input():
    command = ['cat']
    input_data_list = ["Hello\n", "World\n", "Testing\n", "123\n"] * 10
    outputs = await run_subprocesses_with_batch_input(command, input_data_list, 2)
    
    # Decode each output and strip to remove any trailing new line characters
    decoded_outputs = [output.decode() for output in outputs]
    
    assert decoded_outputs == input_data_list

if __name__ == "__main__":
    asyncio.run(pytest.main())