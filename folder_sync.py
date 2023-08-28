# Roland Ciupageanu 2023
# A unidirectional folder syncronisation

import os
import sys
import shutil
import datetime
import time

# ==========================Helper functions===================================
def create_log(path):
    """This function will create the log.txt file in the specified path
    and write to it the first line of info, returns False if the log.txt couldn't be created"""
    # Time in dd/mm/YY H:M:S format, string
    time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    try:
        with open(path + "\\" + "log.txt", "w") as logfile:
            logfile.write(f"{time} Created log.txt in path: {path}\n")
    except:
        # If False = the user will be infromed only in the console 
        return False

def get_time(path):
    """This function will return the time of the last modification of a file
    in the format ex: 2023-03-20 22:03:52.461867 """
    time = os.path.getmtime(path)
    formated_time = datetime.datetime.fromtimestamp(time)
    return formated_time

def current_time():
    """Returns current time in dd/mm/YY H:M:S format as a string"""
    current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return current_time

def get_path():
    """This function will return the source path,replica path and log file path
    provided from the command line arguments"""
    # Paths in cmd can be provided with \\, / or ///
    # Don't use \ to provide paths!
    try:
        source = sys.argv[1]
        replica = sys.argv[2]
        log = sys.argv[3]

    except IndexError:
        sys.exit("To few command line arguments!")

    if len(sys.argv) > 5:
        sys.exit("To many command line arguments!")
    return source, replica, log

def convert_path(path):
    """Allows the user to type paths using '\\', '/' or '//'. All will be converted to '//'.
    !!!Using '\' will work in the function but FAIL in the program because as a command line argument will be considered
    an escape character."""
    converted_path = ""
    for char in path:
        if char == "/":
            converted_path += "\\\\"
        elif char == "\\":
            converted_path += "\\\\"
        else:
            converted_path += char

    if "\\\\\\\\" not in converted_path:
        return converted_path
    
    else:
        converted_path1 = ""
        li = converted_path.split("\\\\\\\\")
        for element in range(len(li)):
            if element == len(li)-1:
                converted_path1 += li[element]
            else:
                converted_path1 += li[element]+"\\\\"
        return converted_path1
    
def check_slash(path):
    """Signals the absence of slashes in the path"""
    for character in path:
        if character in ["\\","/"]:
            return True
    return False

def get_file(path):
    """This function will return a list containg the files/folders of the path.
    False if exception is raised and the path could not be accesed"""
    try:
        list_file = sorted (os.listdir(path))
    except FileNotFoundError:
        return False
    return list_file

def copy_file(files_source, files_replica, path_source,path_replica):
    """This function will copy any files or folders from source to replica 
    if they are present in the source folder and not in the replica folder.
    Returns a list of the copied files"""
    copied_files = []
    for file in files_source:
        if file not in files_replica:
            # If the target is a file with extension
            if "." in file:
                shutil.copy(path_source + "\\" + file, path_replica + "\\" + file)
                copied_files.append(file)
            # If the target is a folder
            else:
                shutil.copytree(path_source + "\\" + file, path_replica + "\\" + file)
                copied_files.append(file)
    return copied_files
   
def replace_same(files_source, files_replica, path_source,path_replica):
    """This function will replace files/folders from replica with the ones from the source if:
        the files have the same names and they have different modification dates.
        Returns a list of replaced files in the replica folder"""
    replaced_files = []
    for n in range(len(files_source)):
            source_file_path = path_source + "\\" + files_source[n]
            replica_file_path = path_replica + "\\" + files_replica[n]
            
            # If the files/ folders from source/replica have different modification dates
            if get_time(source_file_path) != get_time(replica_file_path):
                # If the target is a file
                if os.path.isfile(replica_file_path):
                    os.remove(replica_file_path)
                    shutil.copy(source_file_path,replica_file_path)
                    replaced_files.append(files_source[n])

                # If the target is a folder
                elif os.path.isdir(replica_file_path): 
                    shutil.rmtree(replica_file_path)
                    shutil.copytree(source_file_path,replica_file_path)
                    replaced_files.append(files_source[n])
    return replaced_files
                    
def delete_file(files_source, files_replica,path_replica):
    """This function will delete files/ folders from replica if they are not present
    in the source. Returns a list of the deleted files"""
    deleted_files = []
    for file in files_replica:
        if file not in files_source:
            replica_file_path = path_replica + "\\" + file
            # If the target is a file
            if os.path.isfile(replica_file_path):
                os.remove(replica_file_path)
                deleted_files.append(file)
                
            # If the target is a folder
            elif os.path.isdir(replica_file_path): 
                shutil.rmtree(replica_file_path)
                deleted_files.append(file)
    return deleted_files

# ============================Main function==============================================
def main():
    # Getting the pats of the source, replica and log folder
    path = get_path()

    # Defining source,replica and log file folder paths
    source_path = convert_path(path[0])

    replica_path = convert_path(path[1])

    log_file_status = 0

    log_path = convert_path(path[2])

    # If there are no slashes in the path, notofy the user that maybe this is the problem.
    if not check_slash(source_path) or not check_slash(replica_path) or not check_slash(log_path):
        hint_msg = r" !Possible cause: missing slashes or \ in provided path!"

    if get_file(log_path) == False:
        # Signals that the log file couldn't be created.
        # The program will continue but without any log file, 
        # messages will be printed only in the console

        time = current_time()
        log_file_status = 1
        if check_slash(log_path):
            print(f"{time} The log.txt file could'n be created at path: {log_path}")
        else:
            print(f"{time} The log.txt file could'n be created at path: {log_path}" + hint_msg)

    if log_file_status == 0:
        # Log file creation
        # If the log file does not already at the log_path, create the log.txt file
        if "log.txt" not in get_file(log_path):
            time = current_time()
            
            create_log(log_path)
            if create_log(log_path) != False:
                # Variable to signal the creation of the log_file_status (0=ok, 1=NOK)
                log_file_status = 0
                print(f"{time} Created log.txt in path: {log_path}")
                
            else:
                # Signals that the log file couldn't be created.
                # The program will continue but without any log file, 
                # messages will be printed only in the console
                log_file_status = 1
                if check_slash(log_path):
                    print(f"{time} The log.txt file could'n be created at path: {log_path}")
                else:
                    print(f"{time} The log.txt file could'n be created at path: {log_path}" + hint_msg)
        else:
            log_file_status = 0

    # Getting a list of files in both source and replica folder
    if get_file(source_path) == False:
        if check_slash(source_path):
            sys.exit(f"The source path {source_path} is not a valid path!")
        else:
            sys.exit(f"The source path {source_path} is not a valid path!" + hint_msg)

    list_source = get_file(source_path)

    if get_file(replica_path) == False:
        if check_slash(replica_path):
            sys.exit(f"The replica path {replica_path} is not a valid path!")
        else:
            sys.exit(f"The replica path {replica_path} is not a valid path!" + hint_msg)

    list_replica = get_file(replica_path)

    # What the program does in the different situations:

    # Case 1
    # Both source and replica folders are empty ==> there is nothing to do
    if len(list_source) == len(list_replica) == 0:
        time = current_time()
        
        # Log file and message handling
        # If the log.txt is present in the log_path(no error and the file was created)
        if log_file_status == 0:
            with open(log_path + "\\" + "log.txt", "a") as logfile:
                logfile.write(f"{time} Source and replica folders are empty, folders are in sync!\n")
            print(f"{time} Source and replica folders are empty, folders are in sync!")
        else:
            # No log file created, messages display only in the console
            print(f"{time} Source and replica folders are empty, folders are in sync!NO log file created!")

    # Case2
    # More files/ foders in the replica then in the source ==> delete the nonsync files from replica folder
    elif len(list_source) < len(list_replica):
        time = current_time()
        deleted_list = delete_file(list_source,list_replica,replica_path)
        delete_file(list_source,list_replica,replica_path)

        # Log file and message handling
        # If the log.txt is present in the log_path(no error and the file was created)
        if log_file_status == 0:
            with open(log_path + "\\" + "log.txt", "a") as logfile:
                logfile.write(f"{time} The files {deleted_list} were deleted from the replica folder\n")
            print(f"{time} The files {deleted_list} were deleted from the replica folder")
        else:
            # No log file created, messages display only in the console
            print(f"{time} The files {deleted_list} were deleted from the replica folder! NO log file created!")


    # Case 3
    # More files/ foders in the source then in the replica ==> copy files from source to replica folder
    elif len(list_source) > len(list_replica):
        # ============================================================================================
        # Even if list_source > list_replica, first delete nonsync files from replica, then copy files
        time = current_time()
        deleted_list = delete_file(list_source,list_replica,replica_path)
        delete_file(list_source,list_replica,replica_path)

        # Log file and message handling
        # If the log.txt is present in the log_path(no error and the file was created)
        if log_file_status == 0:
            with open(log_path + "\\" + "log.txt", "a") as logfile:
                logfile.write(f"{time} The files {deleted_list} were deleted from the replica folder\n")
            print(f"{time} The files {deleted_list} were deleted from the replica folder")
        else:
            # No log file created, messages display only in the console
            print(f"{time} The files {deleted_list} were deleted from the replica folder! NO log file created!")
        # ============================================================================================

        # Time in dd/mm/YY H:M:S format, string
        time = current_time()

        copy_list = copy_file(list_source,list_replica,source_path,replica_path)

        # Copy the files/ folders from source folder to replica folder if they are not present
        copy_file(list_source,list_replica,source_path,replica_path)

        # Log file and message handling
        # If the log.txt is present in the log_path(no error and the file was created)
        if log_file_status == 0:
            with open(log_path + "\\" + "log.txt", "a") as logfile:
                logfile.write(f"{time} The files {copy_list} were copied from source to replica folder\n")
            print(f"{time} The files {copy_list} were copied from source to replica folder")
        else:
            # No log file created, messages display only in the console
            print(f"{time} The files {copy_list} were copied from source to replica folder! NO log file created!")

    # Case 4
    # Same file/ folder names in both source and replica ==> if modification dates in source/ replica differ
    # Replace files/ folders from replica with the ones from source
    elif list_source == list_replica:
        time = current_time()

        replace_list = replace_same(list_source,list_replica,source_path,replica_path)

        replace_same(list_source,list_replica,source_path,replica_path)
        
        # Log file and message handling
        # If the log.txt is present in the log_path(no error and the file was created)
        if log_file_status == 0:
            with open(log_path + "\\" + "log.txt", "a") as logfile:
                logfile.write(f"{time} The files {replace_list} were replaced in the replica folder\n")
            print(f"{time} The files {replace_list} were replaced in the replica folder")
        else:
            # No log file created, messages display only in the console
            print(f"{time} The files {replace_list} were replaced in the replica folder! NO log file created!")

    # The final part that shows that the two folders are in sync
    time = current_time()

    # Log file and message handling
    # If the log.txt is present in the log_path(no error and the file was created)
    if log_file_status == 0:
        with open(log_path + "\\" + "log.txt", "a") as logfile:
            logfile.write(f"{time} The source and replica folders are in sync!\n")
        print(f"{time} The source and replica folders are in sync!")
    else:
        # No log file created, messages display only in the console
        print(f"{time} The source and replica folders are in sync!! NO log file created!")

    print("=====EXECUTION COMPLETED=====")

if __name__ == "__main__":
    # If until here not enough command line arguments were supplied (>5 needed)
    if len(sys.argv) > 5:
        sys.exit("To many command linde arguments!")
    try:
        # Converting the scheduled_time argument to int, and then to minutes
        # Accepts even a float scheduled_time, it will be rounded to the nearest int
        scheduled_time = int(sys.argv[4])*60
        
    # If until here not enough command line arguments were supplied (<5 needed)
    except IndexError:
        sys.exit("To few command linde arguments!")
        
    # If ValueError program exits with the following message
    except ValueError:
        sys.exit("Not a valid time argument, please supply int or float argument!")
        
    # If scheduled_time is set to 0, the program will execute only one time
    if scheduled_time == 0:
        main()
        
    else:
        # Program executes every (scheduled_time*60) + execution time (seconds)
        while True:
            main()
            time.sleep(scheduled_time)

