About
=====

Ionic Backup is a clone of the popular Dropbox program for personal server use. Ionic Backup is an improvement of the earlier version MatchBox which used the HTTP protocol. Ionic Backup uses a custom protocol I created specifically for this program.

Advantages Over Matchbox
========================

+Ionic Backup supports folders
+Quicker Uploads and Downloads
+Nicer Shell
+Easier to customize
+No dependencies (No Flask)

How To Setup Ionic Backup
=========================

1. Upload the server.py to your server, and run it using the following command: python server.py <port>
2. Create a folder that you would like to use as your Ionic Backup server.
3. Put client.py into your folder
4. Launch client.py and follow the on screen instructions.
5. type "help" into the shell to learn the commands. 


Files will automatically be uploaded when you insert them into your folder, in order to delete a file you mist do it via the shell. This is just to prevent accidental deletions.
