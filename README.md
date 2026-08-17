<h1>AirMouse</h1>  

<h2>Installation:</h2>
Inside __init__.py change CURRENT_MODE based if you use XDOTOOL or YDOTOOL

Run __init__.py

Download Actions from the app store https://apps.apple.com/us/app/actions/id1586435171  
Download the shortcut from https://www.icloud.com/shortcuts/8e444376531b4ba898eb691983159114

Modify variables based on your system, and run it

<h2>Controls:</h2>
Point your phone to move the x axis

Increase and decrease volume to move the y axis  
Turn your phone landscape left to left click

<h2>How it works:</h2>
-Server

Creates a local server, which listens for  query parameters, and based on that goes to that coordinate  
Example: http://localhost:8000/?x=100&y=100  

-Iphone  
Runs a loop that gets the compass direction, and the volume of the phone, based on that its calculates the x, y
Then it gets the contents of link with the correct xy query parameters