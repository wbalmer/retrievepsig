First, I recommend you create a new python 3.9 environment using conda.
I have encountered issues installing species on python 3.10.

```
conda create -n retrievepsig python=3.9
conda activate retrievepsig
```

Then I install cython:

```
pip install cython
```

Then pymultinest, which is a nested sampler used by species to conduct fits

```
conda install -c conda-forge pymultinest
```

Just to be safe, after this step I like make sure to specify the numpy version that I'm sure is the most stable:

```
pip install numpy==1.21
```

and install seaborn for nice plots

```
pip install seaborn
```

Next, install species from the github repo

```
git clone https://github.com/tomasstolker/species.git
```

pip install this repo in developer mode

```
cd species
pip install -e .
```

and (subject to change!) checkout the "retrieval_tutorial" branch

```
git checkout "retrieval_tutorial"
```

It is pertinent to test that species installed correctly, I do this by

```
python
import species
species.\_\_version\_\_
```

Which should print an '0.4.0' then you can exit:

```
exit
cd ..
```

Now is the painful part. You need to install petitRADTRANS *thunderclap, spooky organ music*

This is fully described here: https://petitradtrans.readthedocs.io/en/latest/content/installation.html

You need to download the opacity data from https://keeper.mpdl.mpg.de/f/f5aba635d3a244adb3c0/?dl=1j

and extract it to a folder titled "input_data"

You then need to add this path to your .bashrc (I've included an example .bashrc in this repo) and

```
source .bashrc
```

Now you are okay to install pRT, but we will install it from Tomas Stolker (the developer of species)'s fork of the repo, e.g.

```
git clone https://gitlab.com/tomasstolker/petitRADTRANS.git
```

install

```
cd petitRADTRANS
python setup.py install
cd ..
```

Now, you are ready to test the script I've prepared. I've formulated a basic retrieval on 51 Eri b,
a unique and fascinating planet with some funky MIR photometry that we hope JWST will help clear up.

run

```
python retrieval_tutorial.py
```

and you should get output confirming that species compiled properly,
called down the 51 Eri photometry, read in the 51 Eri spectrum in this repo,
compiled petitRADTRANS successfully, and started a multinested retrieval.

By default, I set this test script to output temporary figures showing the cloud parameters,
PT profile, and spectrum it fits with each iteration, and so one you see those figures being generated in the directory,
that's the sign your retrieval is started successfully!

The output will look something like:

*****************************************************
MultiNest v3.10
Copyright Farhan Feroz & Mike Hobson
Release Jul 2015

no. of live points =   50
dimensionality =   17
running in constant efficiency mode
*****************************************************
Starting MultiNest
generating live points
Radiative transfer time: 1.15e+01 s

telling you the time the last radiative transfer calculation took.
