#Cachediff     [![Build Status](https://travis-ci.org/sahutd/cachediff.svg?branch=master)](https://travis-ci.org/sahutd/cachediff)

Cachediff is a tool to study the effect of cache performance between two versions (differing from each other by a small diff/delta) of the same C/C++ program.
This is useful to students, educationist and professionals. Cachediff presents to the user a localized and global view of the cache and its statistics. It uses cache simulation based on instruction/memory tracing during execution. It can be extended to support n-versions of the same program.

##Usage
```
python cachediff.py program1.c program2.c input1.c input2.c
```
To run the test-suite

```
nosetests
```

##Requirements
* [Intel Pin](https://software.intel.com/en-us/articles/pin-a-binary-instrumentation-tool-downloads)
```
export PIN=/path/to/pin/folder
```
* [DineroIV](http://pages.cs.wisc.edu/~markhill/DineroIV/)
```
export DINERO=/path/to/dinero/folder
```
* [Disable ASLR](http://askubuntu.com/questions/318315/how-can-i-temporarily-disable-aslr-address-space-layout-randomization)(Dont forget to revert once done, this is a **SECURITY HAZARD**)
