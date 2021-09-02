# anpr
A (mostly) automated setup for Automatic Number Plate Detection (ANPR).<br />
Original code and walkthrough by: <a href="https://www.youtube.com/c/nicholasrenotte">Nicholas Renotte</a><br />
This code only works on Linux systems. (AWS t2.large ubuntu-focal-20.04-amd64-server 16 GB storage)

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
<b>Step 4.</b> Run the ANPR on a webcam/video/stream.
<pre>
python watcher.py # Default image
python watcher.py &lt;video.mp4&gt; # Video file in current directory
python watcher.py &lt;/path/to/video.mp4&gt; # Video file in another directory
python watcher.py &lt;rtsp://user:pass@ipaddress:port/resource&gt; # RTSP stream
</pre>
Note: watcher.py is not currently operational.