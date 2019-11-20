# PyDisplaceInput

Usage: 

Run the script from a command prompt, specifying at least
the scenario name, the name and the input directory if it is not the
current:

```
py_input --verbose --overwrite --name fake \
    --directory DISPLACE_input_minitest/ \
    baseline

```
For example:
```
.\py_input.py --overwrite --name fake --directory C:\Users\fbas\Documents\GitHub\DISPLACE_input_minitest baseline
```
or, for another scenario:
```
.\py_input.py --overwrite --name fake --directory C:\Users\fbas\Documents\GitHub\DISPLACE_input_minitest areaclosure
```

`--verbose` shows some info while running

`--overwrite` overwrites the output file if it is already present

`--directory` selects the input directory, where the model resides

`baseline` is the name of the scenario. 

Since the `--outfile` or `-o` option is not set, the output file will
reside in the `directory` path and will be named `baseline.db`.

You can specify an alternative output name: `-o outfile.db`.

Use the `--help` option to show the usage.