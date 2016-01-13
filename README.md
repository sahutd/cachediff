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

##Example output
![Sample Cachediff output](http://i.imgur.com/BmHT8sV.png)

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

##Instruction Manual
1. Download the github-repo of [Cachediff](https://github.com/sahutd/cachediff.git) and extract the tar file.

2. Download the [Intel Pin](https://software.intel.com/en-us/articles/pin-a-binary-instrumentation-tool-downloads) and extract the tar file and rename the folder to "pin".

3. Download the [DineroIV](http://pages.cs.wisc.edu/~markhill/DineroIV/) and extract the tar file and rename the folder to dinero.

4. Now replace the the MyPinTool folder from 
```
your_present_directory/pin/source/tools/MyPinTool to your_present_directory/cachediff/pin/source/tools/MyPinTool
```
This can be done by 
```
your_present_directory$: rm -r pin/source/tools/MyPinTool
your_present_directory$: cp your_present_directory/cachediff/pin/source/tools/MyPinTool    pin/source/tools/
```
 
5. Make the [Intel Pin](https://software.intel.com/en-us/articles/pin-a-binary-instrumentation-tool-downloads) examples.
```
your_present_directory$: cd pin/source/tools/
your_present_directory$: make
your_present_directory$: cd ../../..
```

6. Make the [DineroIV](http://pages.cs.wisc.edu/~markhill/DineroIV/)
```
your_present_directory$: cd dinero
your_present_directory$: make
your_present_directory$: cd ..
```

7. Set environmental variables :
```
your_present_directory$: echo "export PIN=/path/to/pin/folder" >> ~/.bashrc
your_present_directory$: echo "export PIN=/path/to/dinero/folder" >> ~/.bashrc
your_present_directory$: source ~/.bashrc
```

8. [Disable ASLR](http://askubuntu.com/questions/318315/how-can-i-temporarily-disable-aslr-address-space-layout-randomization)
```
your_present_directory$: setarch $(uname -m) -RL bash
```
(Dont forget to revert once done, this is a **SECURITY HAZARD**)

9. Now you are ready to run the script,
```
python3 cachediff.py program1.c program2.c input_stream1.txt input_stream2.txt
```
where,
- program1.c - the original program
- program2.c - the modified version of the original program
- input_stream1 - input to program1
- input_stream2 - input to program2

