import filecmp
import os
import pytest
import subprocess
import tempfile


@pytest.mark.parametrize("testcase", [("helloworld.cc", "helloworld_format.cc")])
def test_clang_format(testcase):
    # Get full paths to the test data
    test_input, test_output = testcase
    test_input = os.path.join(os.path.dirname(__file__), test_input)
    test_output = os.path.join(os.path.dirname(__file__), test_output)

    with tempfile.TemporaryDirectory() as tmp:
        outname = os.path.join(tmp, "formatted")
        with open(outname, "w") as out:
            subprocess.run(["clang-format", test_input], stdout=out)

        # Check that the content is equal
        assert filecmp.cmp(outname, test_output)
