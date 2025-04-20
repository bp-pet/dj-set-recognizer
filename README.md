# DJ set recognizer
Download a DJ set from Soundcloud, split it into segments, and try to recognize each using Shazam.

### How to use
Make a url.txt file and put the url there. There can be multiple lines in the file, but only the first one that does not start with # will be used.

Run all steps in main.py. All files from previous runs are deleted during this. Results are saved to the output folder.

Shazam API seems to have some limit/cooldown per IP address so using a VPN can be useful.

### Folders
- audio/raw - File is downloaded to here; should contain exactly one file.
- audio/cut - The cut segments are put here.
- audio/archive - Not used by the script but is a place to store any other files if needed.
- output - Saving result or JSON output of Shazam if required.