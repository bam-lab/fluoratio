# fluoratio

## Purpose

This software is intended to analyze the nucleus to cytoplasm fluorescence ratio of a protein of interest over time. The software has been developed only for use with the TIFF image export from the Leica LAS X software, primarily because I have not used any other microscope software, so I don't know their filenaming conventions.

## Setup

This software must be run with Python 3.5.x or 3.6.x, which can be obtained at https://www.python.org/downloads/ . Test that you have installed it correctly by running `python --version` in your terminal, which should return a version number 3.x.x.

After you have installed Python 3, you must install the dependencies for fluoratio. Run `pip install --user -r req.txt` to install the dependencies listed in that file. Note that this command will only install the dependencies for that user account - to install them for all users, omit the `--user` flag.

## Running your analysis

After all the dependencies have been installed, you can run the software using `python Main.py` in your terminal.

## IF YOU ARE RUNNING ON macOS

If you are running this software on macOS, there will likely be a version of Python 2.7 already installed. This software will not work with Python 2.7. If you (masochistally) wish, you are welcome to modify this software to be compatible with Python 2.7, although I do not recommend it. By the time that this software ships, I anticipate that Python 2.7 will actually be completely deprecated, so you shouldn't be using it anyway.

With that preamble out of the way, here are some steps to get Python 3 on macOS. Download and install the Homebrew package manager, available at https://brew.sh/ . Then you will run `export PATH=/usr/local/bin:/usr/local/sbin:$PATH` in your terminal, followed by `brew install python`. This should install Python 3 in your computer. To verify this, run `python3 --version`, which should give you the Python version number beginning with 3. For all of the above `python` or `pip` commands, you must append `3` to the command, e.g. `python3` or `pip3` followed by the other arguments listed above.

## Results

This software will write out the nucleus to cytoplasm fluorescence ratios over time to a .csv file for each mark & find position. It will also generate individual plots for each position, with fluorescence ratio over time. A bulk plot of fluorescence ratio over time for all positions will also be generated, with a different colour for each position. You may want to tweak the colouring scheme for this, in case you have different experimental conditions for different positions.

## How to contribute

Create a virtual environment inside the fluoratio directory using the Python3 `virtualenv` command. Then, install all the dependencies using `pip` once you have started the virtualenv. Create a new git branch for any changes, and make a pull request once you have made your fix.

## Contact

If you run into any issue with this software, please submit an Issue ticket in Github, or contact me on [Twitter](https://twitter.com/jidiculous/). Include as much detail as possible in your submission.

Best of luck, and may your experiments be successful and your results reproducible!
