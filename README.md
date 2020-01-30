# filternet
Tool to filter a list of network blocks and IP addresses using a network and address blacklist

Both the input file and blacklist file should be of the same format

## Example Input List File

```
1.2.3.4
3.4.5.0/24
23.1.1.1/16
23.66.1.4/16  # Some comment
23.64.4.4
```

## Example Blacklist File

```
23.0.0.0/12
96.6.0.0/15
104.64.0.0/10
104.64.0.0/10
184.24.0.0/13
184.84.0.0/14
23.192.0.0/11
23.32.0.0/11
23.64.0.0/14
23.72.0.0/13
72.246.0.0/15
96.16.0.0/15
96.6.0.0/15
```

## Usage

Without an input file specified, stdin will be used

```
$ cat input.lst | ./filternet.py -b lists/akamai-nets.lst
```

Optionally, provide the input file via `-i`:

```
$ ./filternet.py -b lists/akamai-nets.lst -i input.lst
```