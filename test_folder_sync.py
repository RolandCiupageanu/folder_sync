# Roland Ciupageanu 2023
# Tests for project.py using pytest

import pytest
from project import create_log, get_time, current_time, get_file, get_path, copy_file, replace_same, delete_file, convert_path, check_slash

import os
import sys
import shutil
import time
import datetime

def test_create_log():
    # We create a folder, and we test if in it the log is created
    # We get the current directory
    current_path = os.getcwd()

    # Replacing \ with \\
    log_path = current_path + "\\log_folder"
    log_path = log_path.replace("\\","\\\\")

    # Creating a folder on the log path
    os.mkdir(log_path)
    # Creating the log file in the log folder
    create_log(log_path)

    assert os.listdir(log_path)[0] == "log.txt"
    assert create_log("some_random_path") == False

    # Removing the whole log folder
    shutil.rmtree(log_path)

def test_get_time():
    # We create a folder, and there two files with delay between them. After that we compare the modification date of the files.
    # We need to recive different modification dates
    current_path = os.getcwd()
    test_path = current_path + "\\test_path"
    test_path = test_path.replace("\\","\\\\")

    os.mkdir(test_path)

    with open(test_path + "\\" + "first_file.txt", "w") as first_file:
        first_file.write("Text in the FIRST file")
        first_time = get_time(test_path + "\\" + "first_file.txt")

    # Delay 1 second between the two folders
    time.sleep(1)

    with open(test_path + "\\" + "second_file.txt", "w") as second_file:
        second_file.write("Text in the SECOND file")
        second_time = get_time(test_path + "\\" + "second_file.txt")

    assert second_time>first_time
    assert second_time != first_time

    # Removing the whole test folder
    shutil.rmtree(test_path)

def test_get_time():
    # The tested return format: 2023-06-15 22:56:59.066165
    current_path = os.getcwd()
    test_path = current_path.replace("\\","\\\\")
    file_path1 = test_path + "\\" + "test_file1.txt"
    file_path2 = test_path + "\\" + "test_file2.txt"

    with open(file_path1, "w") as file1:
        file1.write("Text in the test file 1")
    
    # Delay 1 second between the two files, check if time1 < time2
    time.sleep(1)

    with open(file_path2, "w") as file2:
        file2.write("Text in the test file 2")
    
    assert type(get_time(file_path1)) is datetime.datetime
    assert type(get_time(file_path2)) is datetime.datetime
    assert get_time(file_path1) < get_time(file_path2)

    # Removing test folders
    os.remove(file_path1)
    os.remove(file_path2)

def test_current_time():
    # The tested return format: 15/06/2023 21:47:10
    assert type(current_time()) is str
    assert len(current_time().split(" ")) == 2
    
    day = int(current_time()[0:2])
    month = int(current_time()[3:5])
    assert day <=31
    assert month <= 12

def test_get_path():
    # Define a sys.argv, if we apply get_path() we get:
    sys.argv = ["program.py", "source_path", "replica_path", "log_path"]
    # get_path[0] will be [1] in the list, in the function source is sys.argv[1]
    assert get_path()[0] == "source_path"
    assert get_path()[1] == "replica_path"
    assert get_path()[2] == "log_path"
    
    # Anything with less then 4 elements will lead to sys.exit
    sys.argv = ["program.py", "source_path", "replica_path"]
    with pytest.raises(SystemExit):
        get_path()

    # sys.argv with to many args (>5), will also cause sys.exit
    sys.argv = ["program.py", "source_path", "replica_path", "log_path", "sync_time", "out_of_range"]
    with pytest.raises(SystemExit):
        get_path()

def test_get_file():
    # Test if path does not exists => return False
    assert get_file("some\\random\\file") == False
    
    # Test if the return is correct (files&folders list from path)
    # In current path we will make a folder where we will test get_file
    current_path = os.getcwd()
    test_folder_path = current_path + "\\test_folder"
    try:
        os.mkdir(test_folder_path)
    # Except only FileExistsError, FileNotFound is caught above with False
    except FileExistsError:
        pass

    # Creation of a file in the test folder
    try:
        with open(test_folder_path + "\\" + "test_file.txt", "w") as test_file:
            test_file.write("Just a file to test the get_file function :)")
    except FileExistsError:
        pass

    # Creation of a folder in the test folder
    folder_path = test_folder_path + "\\a_folder"
    try:
        os.mkdir(folder_path)
    except FileExistsError:
        pass 

    files = get_file(test_folder_path)
    assert files[0] == "a_folder"
    assert files[1] == "test_file.txt"
    assert len(files) == 2

    # Remove the test folder with all it's content
    shutil.rmtree(test_folder_path)

def test_convert_path():
    path0 = r"C:\Roland\Source"
    path1 = r"C:\\Roland\\Source" 
    path2 = r"C:/Roland/Source"
    path3 = r"C://Roland//Source"

    # Alltough here the paths with \ passes, it will not work in the program (see function deffinition)
    # Don't use \ when providing paths at the command line!
    assert convert_path(path0) == r"C:\\Roland\\Source"

    assert convert_path(path1) == r"C:\\Roland\\Source"
    assert convert_path(path2) == r"C:\\Roland\\Source"
    assert convert_path(path3) == r"C:\\Roland\\Source"

def test_check_slash():
    path0 = r"C:\Roland\Source"
    path1 = r"C:\\Roland\\Source" 
    path2 = "C:/Roland/Source"
    path3 = "C://Roland//Source"
    path4 = "C:RolandSource"

    assert check_slash(path0) == True
    assert check_slash(path1) == True
    assert check_slash(path2) == True
    assert check_slash(path3) == True
    assert check_slash(path4) == False

def create_structure():
    """Creates the folder structure needed to test different functions.
    Returns paths for further use"""
    current_path = os.getcwd()
    test_folder_path = current_path + "\\test_folder"
    try:
        os.mkdir(test_folder_path)
    # Except only FileExistsError, FileNotFoundError is caught by the other tests, it won't get to copy
    except FileExistsError:
        pass

    # Source folder in test_folder_path
    path_source = test_folder_path + "\\source_folder"
    try:
        os.mkdir(path_source)
    except FileExistsError:
        pass

    # Replica folder in test_folder_path
    path_replica = test_folder_path + "\\replica_folder"
    try:
        os.mkdir(path_replica)
    except FileExistsError:
        pass
    
    return current_path, test_folder_path, path_source, path_replica

def test_copy_file():
    create_structure()
    paths = create_structure()
    path_source = paths[2]
    path_replica = paths[3]
    test_folder_path = paths[1]

    # We create a test folder in the source folder
    folder_source = path_source + "\\a_folder"
    try:
        os.mkdir(folder_source)
    except FileExistsError:
        pass

    # We create a test folder in the replica folder with the same name as in the source folder
    folder_replica = path_replica + "\\a_folder"
    try:
        os.mkdir(folder_replica)
    except FileExistsError:
        pass
    
    # in the source folder, we also a test file
    try:
        with open(path_source + "\\" + "test_file.txt", "w") as test_file:
            test_file.write("Just a file to test the copy_file function :)")
    except FileExistsError:
        pass

    # Getting the list of files from the source and replica folders
    files_source = get_file(path_source)
    files_replica = get_file(path_replica)

    # Tests if the files to copy are only the ones that are not present (test_file.txt)
    assert copy_file(files_source, files_replica, path_source, path_replica ) == ["test_file.txt"]

    # Remove the whole folder with it's content after testing
    shutil.rmtree(test_folder_path)

def test_replace_same():
    create_structure()
    paths = create_structure()
    path_source = paths[2]
    path_replica = paths[3]
    test_folder_path = paths[1]

    # In the source folder we create a test file
    try:
        with open(path_source + "\\" + "test_file.txt", "w") as test_file:
            test_file.write("Content of the source file")
    except FileExistsError:
        pass

    # We create the 2 files (source file / replica file) with 1 second delay
    time.sleep(1)
    # In the replica folder we create a test file with the same name, but other content
    try:
        with open(path_replica + "\\" + "test_file.txt", "w") as test_file:
            test_file.write("Content of the replica file")
    except FileExistsError:
        pass
    
    # Getting the list of files from the source and replica folders
    files_source = get_file(path_source)
    files_replica = get_file(path_replica)

    # Tests if the replaced file is test_file.txt
    assert replace_same(files_source, files_replica, path_source,path_replica) == ["test_file.txt"]

    # Tests if the file is overwritten with the last modification like the source file
    with open(path_replica + "\\" + "test_file.txt", "r") as test_file:
        # Reading the first line of the replica file and check if it's the line from the source file
        first_line = test_file.readline()
        assert first_line == "Content of the source file"

    # Remove the whole folder with it's content after testing
    shutil.rmtree(test_folder_path)

def test_delete_file():
    create_structure()
    paths = create_structure()
    path_source = paths[2]
    path_replica = paths[3]
    test_folder_path = paths[1]

    # In the wource folder we create a test folder
    folder_source = path_source + "\\a_folder"
    try:
        os.mkdir(folder_source)
    except FileExistsError:
        pass

    # In the source folder we create a test file
    try:
        with open(path_source + "\\" + "test_file.txt", "w") as test_file:
            test_file.write("Just a file to test the delete_file function :)")
    except FileExistsError:
        pass

    # In the replica folder we create another test folder, with a different name
    folder_replica = path_replica + "\\b_folder"
    try:
        os.mkdir(folder_replica)
    except FileExistsError:
        pass

    # In the replica folder we create a test file
    try:
        with open(path_replica + "\\" + "another_file.txt", "w") as another_file:
            another_file.write("Just ANOTHER to test the delete_file function :)")
    except FileExistsError:
        pass

    # Getting the list of files from the source and replica folders
    files_source = get_file(path_source)
    files_replica = get_file(path_replica)

    # We test if the files in the replica (the ones not present in source) are found in the list to delete
    assert delete_file(files_source, files_replica,path_replica) == ["another_file.txt", "b_folder"]

    # Remove the whole folder with it's content after testing
    shutil.rmtree(test_folder_path)
