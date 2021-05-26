# YAML Parser
This script parses the `!include` directive in YAML files. Included file doesn't have to be in the same directory, relative paths also work.

## Requirements
- Python 3.8 and above
- pyyaml

## Usage
```bash
python3 -m pip install pyyaml
./yaml_parser <input_file>
```

### Example
```bash
$ cat main.yaml
numbers: !include numbers.yml

$ cat numbers.yaml
- 1
- 2
- 3

$ ./yaml_parser.py main.yaml
numbers:
  - 1
  - 2
  - 3
```