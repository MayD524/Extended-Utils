"""
    Author     : May Draskovics
    Date       : 12/22/2021
    Description:
        A basic find program that looks for a specific file in a given directory/range
"""
from sys import getrecursionlimit, setrecursionlimit
import argparse
import os

def lookForFile(path:str, lookfor:str, *, 
                recursive:bool=True, readContent:bool=False ,
                maxDepth:int=getrecursionlimit()-1, curDepth:int=0, 
                ignore_case:bool=False, ignoreDir:str=None) -> None:
    
    if curDepth == maxDepth:
        return
    
    if ignoreDir and path == ignoreDir:
        return
    
    for obj in os.listdir(path):
        pth = os.path.join(path, obj) if not ignore_case else os.path.join(path, obj).lower()
        pth = pth.replace("\\", '/')
        if os.path.isdir(pth) and recursive:
            lookForFile(pth, lookfor, recursive=recursive,  
                        readContent=readContent ,maxDepth=maxDepth, 
                        curDepth=curDepth+1, ignore_case=ignore_case,
                        ignoreDir=ignoreDir)
            
        elif readContent:
            
            with open(os.path.abspath(pth), "r") as f:
                if lookfor in f.read():
                    print(os.path.abspath(pth))
               
        elif lookfor in obj:
            print(os.path.abspath(pth)) ## just get the full path

#.txt
     
if __name__ == "__main__":
    ## just handle the arguments
    parser = argparse.ArgumentParser(description='Find a file... its in the name....')
    ## basic functions
    parser.add_argument('-l', '--look_for', help='Look for this file', required=True)
    parser.add_argument('-m', '--max_depth', type=int, help='Max depth to search', default=getrecursionlimit()-1, required=False)
    parser.add_argument('-d', '--dir', help='Directory to list', default=".", required=False)
    parser.add_argument('-i', '--ignore_case', help='Ignore case', action='store_true', required=False)
    parser.add_argument('-r', '--read_contents', help='Read contents of file', action='store_true', required=False)
    parser.add_argument('-id', '--ignore_dir', help='Ignore dirs', default=None, required=False) 
    
    ## You kinda need to know what you're doing here
    parser.add_argument('-ig', '--ignore_warnings', help='Ignore warnings', action='store_true', required=False)
    parser.add_argument('-sr', '--set_recursive_limit', type=int, help='Set the recursive limit', default=None, required=False)   
    
    args = parser.parse_args()
    
    
    args.dir = os.path.abspath(args.dir).replace("\\", '/')
    args.ignore_dir = os.path.abspath(args.ignore_dir).replace("\\",'/') if args.ignore_dir else None
    
    ## just so that we don't accidentally cause issues
    if args.set_recursive_limit is not None and not args.ignore_warnings:
        print("WARNING!! Setting the recursive limit to:", args.set_recursive_limit)
        print("This may cause problems if you are using a large directory.\nAre you sure you want to continue?")
        a = input("Enter Y to continue: ")
        if a.lower() == "y":
            setrecursionlimit(args.set_recursive_limit)
    
    if not os.path.isdir(args.dir):
        print(f"{args.dir} is not a directory")
        exit(1)
        
    if args.ignore_dir and not os.path.isdir(args.ignore_dir):
        print(f"{args.ignore_dir} is not a directory")
        exit(1)
    
    args.look_for = args.look_for.lower() if args.ignore_case else args.look_for
    lookForFile(args.dir, 
                args.look_for, 
                recursive=True, 
                readContent=args.read_contents,
                ignoreDir=args.ignore_dir, 
                maxDepth=args.max_depth)
    