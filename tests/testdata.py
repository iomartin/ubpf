import os

_test_data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")

def list_files():
    """
    Return a list of data files under tests/data

    These strings are suitable to be passed to read().
    """

    result = []
    for dirname, dirnames, filenames in os.walk(_test_data_dir):
        dirname = (os.path.relpath(dirname, _test_data_dir) + '/')[2:]
        for filename in filenames:
            if filename.endswith('.data') and not filename.startswith('.'):
                result.append(dirname + filename)
    return sorted(result)

def read(name):
    """
    Read, parse, and return a test data file

    @param name Filename relative to the tests/data directory
    @returns A hash from section to the string contents
    """

    section_lines = {}
    cur_section = None

    with open(os.path.join(_test_data_dir, name)) as f:
        for line in f:
            line = line.rstrip().partition('#')[0].rstrip()
            if line == '':
                continue
            elif line.startswith('--'):
                cur_section = line[2:].strip()
                if cur_section in section_lines:
                    raise Exception("section %s already exists in the test data file")
                section_lines[cur_section] = []
            elif cur_section:
                section_lines[cur_section].append(line)
    data = { section: '\n'.join(lines) for (section, lines) in section_lines.items() }

    # Special case: convert 'raw' section into binary
    # Each line is parsed as an integer representing an instruction.
    if 'raw' in data:
        insts = []
        for line in data['raw'].splitlines():
            num, _, _ = line.partition("#")
            insts.append(int(num, 0))
        data['raw'] = insts

    return data