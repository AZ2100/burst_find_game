# Burst Detect Game Tool

This tool use used to find bursts in signals 

## Getting Started

Please download the zip file for this directory and unpack it.

### Prerequisites

You must have `python2`. python3 might work but has not been tested.

To check which version of python you are running simply type `python --version` in your terminal.
Output should look like:
```
Python 2.X.X 
```

If you do not have `python2` (any version of 2) then download `python2` and `pip` for your operating system.

Make sure the project interpreter and all of the code is Python 2.

You must have Pygame. If you do not, follow th instructions here:
http://kidscancode.org/blog/2015/09/pygame_install/

### Installing

Make sure the command is searching in the right location. Type `cd`
followed by the location where requirements.txt is stored. For example, if it's stored in your user, A, in your desktop:
```
cd /Users/A/Desktop/
```

In your terminal/bash-window `cd` into this folder run:
```
pip install -r requirements.txt
```


## Running the Tool

Now you should be able to call:
```
python src/main.py
```

## This will bring up a matplotlib window 

![](https://media.giphy.com/media/9SIMHyfhYAyTHCDLgh/giphy.gif)

# Things to know about the tool

There are two stages to each image evaluation:
*   Stage 1) - "Playing" (Annotating)
      * While playing you can click and drag to highlight bursts 
      * Hold `x` and click on a highlighted burst to remove it! (I think this should be very helpful)
      * You can click `next` to move to the next Stage 
      * You can click `previous` to go back to the previous signal
      * And you can hit `quit` to exit the game
      * You can jump to a certain signal if you know its global id <this is useful if you want to keep your progress when you leave and come back>
      
*   Stage 2) - "Seeing" (Validating)
      * In this stage you can see the predicted bursts overlayed ontop of your highlighted bursts
      * You can hit `previous` to go to Stage 1 for this signal and make some changes
      * You can hit `next` to go to Stage 1 for the next signal (when this is done your highlights will be saved to the out_files)
      * And you can hit `quit` to exit the game
      * You can jump to a certain signal if you know its global id <this is useful if you want to keep your progress when you leave and come back>
       
      
      
### Note that all data is always saved as `(time)_file.csv`) so we know which is the most recent one

Once you are done please send me the `out_files` folder when you are done, this contains the burst regions you generated.












