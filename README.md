# anpr
A (mostly) automated setup for Automatic Number Plate Detection (ANPR).<br />
Original code and walkthrough by: <a href="https://www.youtube.com/c/nicholasrenotte">Nicholas Renotte</a><br />

## Steps
<b>Step 1.</b> Run the train.py script to install dependencies and test the environment.<br />
This will need to be run a couple times, follow the outputted instructions.
<pre>
python train.py test
</pre> 
<b>Step 2.</b> Run the train.py script to get the command needed to start training.
<pre>
python train.py train
</pre>
<b>Step 3.</b> Run the ANPR on an image.
<pre>
python detector.py
</pre>
