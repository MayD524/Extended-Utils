"""
    Author     : May Draskovics
    Date       : 12/22/2021
    Description:
        a basic ls command but extended to make it better to use :>
"""
from datetime import datetime
import argparse
import math
import os

MAX_TREE_DEPTH  = 50
lines:list[str] = []



def list_files(path:str, tree_loc:int, max_depth:int, 
               *, writeFile:bool=False, fileWrite:str=None, 
               recursive_search:bool=True) -> None:
    if tree_loc > max_depth:
        return ## don't bother recursing further
    treeLocStr = "-"*tree_loc
    for obj in os.listdir(path):
        pth = os.path.join(path, obj)
        lsLine = f"└{treeLocStr}> {pth}".replace("\\", "/")
        
        ## check if we are outputting to a file
        if writeFile:
            lines.append(lsLine.replace("└", "|"))
        ## print whatever we have to console
        print(lsLine)
        if os.path.isdir(pth) and recursive_search:
            list_files(pth, tree_loc + 1, max_depth, recursive_search=recursive_search, writeFile=writeFile)
            
    if tree_loc == 0 and writeFile:
        with open(fileWrite, "w+") as f:
            f.write("\n".join(lines))

def convert_size(size:int) -> str:
    if size == 0:
        return "0B"
    
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size, 1024)))
    p = math.pow(1024, i)
    s = round(size / p, 2)
    return "%s %s" % (s, size_name[i])

def octal_to_string(octal:int) -> str:
    result = ""
    valueLetters = [(4, "r"), (2, "w"), (1, "x")]
    
    for digit in [int(n) for n in str(octal)]:
        for value, letter in valueLetters:
            if digit >= value:
                result += letter
                digit -= value
            else:
                result += "-"
    return result


def get_file_info(path:str) -> list[str]:
    
    fData:list[str] = [
        convert_size(os.path.getsize(path)),            # file size
        datetime.fromtimestamp(os.path.getmtime(path))
            .strftime("%Y-%m-%d %H:%M:%S"),             # last modified
        octal_to_string(os.stat(path).st_mode),         # permissions
    ]
    
    return fData

def long_listing(path:str, tree_loc:int, max_depth:int, 
                 *, writeFile:bool=False, fileWrite:str=None, 
                 recursive_search:bool=True) -> None:
    
    if tree_loc > max_depth:
        return
    
    for obj in os.listdir(path):
        pth = os.path.join(path, obj).replace("\\", "/")
        if os.path.isdir(pth) and recursive_search:
            long_listing(pth, tree_loc + 1, max_depth, recursive_search=recursive_search, writeFile=writeFile)
        else:
            fData = get_file_info(pth)
            ## print format
            ## mode last_modified size name
            ## spaced out to make it easier to read
            lsLine = f"{fData[1]:>24}     {fData[0]:>10} {pth:}".replace("\\", "/")
            print(lsLine)
            if writeFile:
                lines.append(lsLine.strip())
        ## get data on the file
    if tree_loc == 0 and writeFile:
        with open(fileWrite, "w+") as f:
            f.write("\n".join(lines))
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='List Directory Extended')
    parser.add_argument('-d', '--dir', help='Directory to list', default=".", required=False)
    parser.add_argument('-t', '--tree', type=int ,help='Tree depth', default=MAX_TREE_DEPTH, required=False)
    parser.add_argument('-f', '--file', help='File to write to', default=None, required=False)
    parser.add_argument('-nr', '--no_recurse', help='Disable Recursive Listing', action='store_false', required=False)
    parser.add_argument('-ll', '--long_listing', help='Enable Long Listing', action='store_true', required=False)
    args = parser.parse_args()
    args.tree = args.tree - 1
    
    if not os.path.isdir(args.dir):
        print(f"{args.dir} is not a directory")
        exit(1)
        
    if args.long_listing:
        print("        Last Modified            Size    Name")
        print("-"*55)
        long_listing(args.dir, 0, args.tree, writeFile=args.file is not None, fileWrite=args.file, recursive_search=args.no_recurse)
    else:
        list_files(args.dir, 0, args.tree, writeFile=args.file is not None, fileWrite=args.file, recursive_search=args.no_recurse)
