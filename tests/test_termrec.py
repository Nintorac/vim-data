from pathlib import Path
import pytest
from vim_data.lib.term_rec import record_vim_terminal

tests_dir = Path('/'.join(__file__.split('/')[:-1]))
"""
Testing this module is kind of difficult, outputs are not consistent between runs
and would rely heavily on system load and other ephemeral phenomena.

It may be possible to render the recording to a gif and compare in image space but
its not clear if this would be a proper solution anyway.



For now we just make sure it runs without failing
"""

@pytest.mark.asyncio
async def test_successful_execution_with_basic_input():
    """
    Test successful execution with basic input to record a Vim session.
    """
    input_data = "iHello, Vim!\033"

    recording = await record_vim_terminal(input_data)

@pytest.mark.asyncio
async def test_handling_of_complex_input_data():
    """
    Test recording of a Vim session with complex inputs like editing and saving.
    """
    # Sequence explaining the inputs:
    # i - enter insert mode; Hello, Vim! - insert text; 
    # \033 - ESC key to go back to normal mode; 
    # :w - save the file; :q! - quit without saving (if needed);
    input_data = "iHello, Vim!\0332ddOThis is a new line.\033"
    recording = await record_vim_terminal(input_data)

if __name__ == "__main__":
    pytest.main()