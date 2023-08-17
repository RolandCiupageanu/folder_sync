# Project name: folder sync
## A program used to to synchronize two folders in unidirectional mode


### 1. Project description:

As automation becomes more and more used and needed, one may need to link two folders containing different files or folders.

The two folders are named intuitive:
- source folder : the folder with that the replica folder will be synced
- replica folder: the folder that is synced with the source folder

Other therms:
- source path : the path of the source folder
- replica path : the path of the replica folder
- log : a log.txt file in which all operations are tracked
- log path : the path of the log file
- scheduled time : the time interval at which the program is executed again

These two folders are synchronized only one way: the files and folders from the replica folder are synchronized with the files and folders from the source folder. 

### 2. Logic and usage:
The program comunicates with the user via command line arguments.
The user must must provide the following command line argumets format:

**Note! The paths are absolute paths, and they will be provided using the following slashes: \\ or // or /.**
**Note! Avoid providing paths using \ as it will be treated as an escape character.**

The name of the program:
sys.argv[0]: example: folder_sync.py

Path of the source folder:
sys.argv[1]: example: C:\\Users\\Roland\\Desktop\\folder0

Path of the replica folder:
sys.argv[2]: example: C:\\Users\\Roland\\Desktop\\folder1

Path of the log folder:
sys.argv[3]: example: C:\\Users\\Roland\\Desktop\\log

The time interval at which the program is executed again:
If this argument is 0, the program will execute once.
If the argument is a non zero integer, for example 3, it will be converted into minutes, so the program will run forever every 3 minutes.
If the argument couldn't be converted to an int, the program will exit with a message.
sys.argv[4]: example: 0

Example of the full path:
**python folder_sync.py C:\\Users\\Roland\\Desktop\\folder0 C:\\Users\\Roland\\Desktop\\folder1 C:\\Users\\Roland\\Desktop\\log 0**

where:

python : is the name of the interpreter
folder_sync.py : the name of the program to execute
C:\\Users\\Roland\\Desktop\\folder0 : path of the source folder
C:\\Users\\Roland\\Desktop\\folder1 : path of the replica folder
C:\\Users\\Roland\\Desktop\\log : path of the log.txt file

0 : the scheduled time (with 0 the program will only execute once)




### Program logic:
1. Arguments 1, 2, 3 and 4 are converted to paths.
If there are more then 5 arguments in total or the first three couldn't be converted to paths, the program will exit with a message.

2. The log file log.txt will be created at the log path (arg[3]), if the log file can not be accesed the program will continue whithout a log file, and the messages will be displayed only in the console, else each operation will be appended to the log file and also printed to the console.

3. A list of the files and folders in both source and replica files will be created. If the paths of these files can not be accesed, the program will exit with a message.

4. Next comes the file manipulation in the different situations.
Case 1: Both source and replica folders are empty, so there is nothing to do because both folders are in sync. The message will be appended to the log file(if the file can be created) and printed to the console.

5. Case 2: More files/ foders in the replica then in the source, so we need to delete the nonsync files from replica folder. The files will be deleted, and added to a list. The list will appear in the message and it will appended in the log file(if the file can be created) and printed in the console.

6. Case 3: More files/ foders in the source then in the replica  folder, so we need to copy files from source to replica folder. The files will be copied, and added to a list. The list will appear in the message and it will appended in the log file(if the file can be created) and printed in the console.

7. Case 4: Same file/ folder names in both source and replica folder, if modification dates in source/ replica differ, replace files/ folders from replica with the ones from source. The files will be replaced, and added to a list. The list will appear in the message and it will appended in the log file(if the file can be created) and printed in the console.

8. The final step, where the program will show if the two folders are in sync. The message will be appended in the log file(if the file can be created) and it will be printed in the console.

9. Scheduled time: using this time provided in sys.argv[4], the program will repeat periodically (see the above section: "logic and usage")

### 3. Testing
The unit tests are in the test_folder_sync.py an can be run using the pytest library using the command:
**pytest test_folder_sync.py**

### 4. Requirements
The only library that needs to be installed is pytest.
You can find it in the requirements.txt file and install it using the **pip install pytest** command.
