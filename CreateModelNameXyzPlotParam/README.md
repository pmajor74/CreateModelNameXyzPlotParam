Requirements: Python 3.9+ installed, and have it installed to PATH

#What the tool does

This is an extremely simple tool. It is designed to help take a group of LoRA files that you are training and saving out every "X" steps. It will then output text to be used in the Automatic1111 interface in the XYZ plot, in the Config SR section.

For example, you may have the following files:

JohnAppleseed-step00000100.safetensors
JohnAppleseed-step00000200.safetensors
JohnAppleseed-step00000300.safetensors
JohnAppleseed-step00000400.safetensors
JohnAppleseed-step00000500.safetensors
JohnAppleseed-step00000600.safetensors
JohnAppleseed-step00000700.safetensors

You want to plot all of these in A111 easily and don't feel like adding commas or typing a lot?

1) Run the tool
2) Drag the files onto the tool
3) The text you need is immediately copied into the following format: step00000100,step00000200,step00000300,step00000400,step00000500,step00000600,step00000700
4) Open your Automatic 1111 SD interface
5) In Scripts choose XYZ Plot
6) Past the values in the "X Type" field and change the X Type down to "Config S/R"  (search and replace)
7) In your main prompt, add the following line:  <lora:JohnAppleseed-step00000100:1> a photo of a man JohnAppleseed
8) Run. Enjoy your grid. 
9) If you want to do runs where you can experiment with the strength of the LoRA, just change the strength and it will be changed for all.

#How to Run

Run as follows (non-windows env can just run "python CreateModelNameXyzPlotParam_steps.py"):

	1) CreateModelNameXyzPlotParam.cmd

At first run, it will install python dependencies: tkinterdnd2 and pyperclip


