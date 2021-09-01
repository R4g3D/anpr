# anpr
A (mostly) automated setup for Automatic Number Plate Detection (ANPR).<br />
Original code and walkthrough by: <a href="https://www.youtube.com/c/nicholasrenotte">Nicholas Renotte</a><br />

## Steps
<b>Step 1.</b> Run the train.py script to setup the environment.<br />
<pre>
python train.py setup
</pre> 
<b>Step 2.</b> Run the train.py script to test the environment.<br />
<pre>
python train.py test
</pre>
<b>Step 2.</b> Run the train.py script to get the command needed to start training.<br />
<pre>
python train.py train
</pre>
<b>Step 3.</b> Run the ANPR on an image.
<pre>
python detector.py # Default image
python detector.py &lt;image.png&gt; # In current directory
python detector.py &lt;/path/to/image.png&gt; # In another directory
</pre>
