from src.scripts import script_compiler as s_compiler
from src.scripts import script_cmd as s_cmd
import tomllib
import sys

# - Load config
from src import config as cfg

# - Set print function
println = s_cmd.console('[b3-compiler]').print

# - Set key
from src import key as keyfile
key = keyfile.key

# - Set class to variable
comp = s_compiler.compiler(key)

def print_usage():
    println('Usage:')
    println('  b3-compiler [/c | /d] -f <file> (Optional: --b)')
    println('    *  de-/compiles the file')
    println('    *  --b: makes a backup of the original file')
    println('  b3-compiler -v')
    println('    *  prints the version of the program')

def compile_file(file_path: str, make_backup: bool = False):
    comp.compile(file_path, decomp_or_comp=0, make_original_file=make_backup)

def decompile_file(file_path: str, make_backup: bool = False):
    comp.compile(file_path, decomp_or_comp=1, make_original_file=make_backup)

def quit():
    sys.exit()

def index_check(argu_name: str):
    index = s_cmd._get_argument_index(sys.argv, argu_name)
    if index == None:
        print_usage()
        quit()
    return index

def print_version():
    println('Current version: v{}-cmd'.format(cfg.version))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print_usage()
        quit()

    if s_cmd._check_argument_exists(sys.argv, '-v'):
        print_version()
        quit()

    # - Set file
    file = sys.argv[index_check('-f')]

    # - Check if de-/compile argument exists
    if s_cmd._check_argument_exists(sys.argv, '/c'):
        c = 0
    elif s_cmd._check_argument_exists(sys.argv, '/d'):
        c = 1
    else:
        print_usage()
        quit()

    # (Optional) - Check if make backup argument exists
    if s_cmd._check_argument_exists(sys.argv, '--b'):
        make_backup = True
    else:
        make_backup = False

    try:
        if c == 0:
            compile_file(file, make_backup)
        elif c == 1:
            decompile_file(file, make_backup)
    except FileNotFoundError:
        println('File not found: {}!'.format(file))
        quit()
    
    println('Done!')
