## Regulations and Assumptions 

### [Project Description](https://docs.google.com/document/d/12abTFE48Og_o3m5Oh16NBYvLzybPCEJQoeuerxMw03k/edit?tab=t.0)

### [Test Dataset](https://drive.google.com/file/d/1G_wWXdNKswV0gWflR0--64mfc2D8x2ZI/view?usp=sharing)
1. You can have any number of Python files, but the entry/main file must be named `project.py`.
2. The command to run the program will be:

```
python3 project.py <function name> [param1] [param2] ...
```

3. The list of function names and their parameters is in the function requirements section. 	
4. You can assume that the command-line input is always correct <u>IN FORMAT ONLY</u>. There won’t be a nonexistent function name as input, and the parameters will be given in the correct order and format. So you don’t need to handle unexpected input. However, input content can be faulty - e.g., given a duplicate netID for insertion. 
5. You can assume that the dataset files are always correct <u>IN FORMAT AND CONTENT</u>. So there won’t be errors when parsing the file, or when inserting the records to DB. 
6. Every date has the format YYYY-MM-DD, e.g. 2025-02-29, and every datetime has the format YYYY-MM-DD hh:mm:ss, e.g. 2025-02-29 14:10:34.
Strings that contain spaces will be wrapped in quotation marks when calling the command, (e.g. "The Matrix") whereas strings with no spaces will not have quotation marks (e.g. Wicked).
7. If the input is NULL, treat it as the None type in Python, not a string called “NULL”.
8. **If the output is boolean**, print “Success” or “Fail”.
9. **If the output is a result table**, print each record in one line and separate columns with ‘,’ - just like the format of the dataset file. 
10. You must use **Python 3**. The standard Python libraries and mysql-connector-python will be installed in the autograder — other third-party packages are not allowed.