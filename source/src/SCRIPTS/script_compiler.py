import os
import sys
import shutil
from cryptography import fernet


class compiler:
    def __init__(self, keyfile) -> None:
        self.key = keyfile
        self.comp = fernet.Fernet(self.key)
    
    def compile(self, file, decomp_or_comp, make_original_file=False):
        file = _get_full_path(file)
        
        if make_original_file:
            dest_file = _replace_file_extension(file, '.backup')
            
            #print("FILENAME: " + file_without_ext)
            shutil.copyfile(file, dest_file)
        
        
        
        # Read file and compile it (encrypt)
        if decomp_or_comp == 0:
            FILE_CONTENT = open(file, 'rb').read()
            FILE_CONTENT_COMPILED = self.comp.encrypt(FILE_CONTENT)
            
        elif decomp_or_comp == 1:
            FILE_CONTENT = open(file, 'rb').read()
            FILE_CONTENT_COMPILED = self.comp.decrypt(FILE_CONTENT)
        

        # Write data to file
        open(file, 'wb').write(FILE_CONTENT_COMPILED)

        if decomp_or_comp == 0:
            os.rename(file, file + '.b3')
        else:
            filename_only = _get_file_without_path(file)
            print(filename_only)
            if not ".b3" in filename_only:
                pass
            else:
                os.rename(file, _replace_file_extension(file, ''))
        return

def _get_file_without_path(file):
    file_s = file.split('\\' if '\\' in file else '/')
    return file_s[len(file_s)-1]


def _get_file_without_ext(file):
    file_without_ext_s = file.split('.')
    if len(file_without_ext_s) == 1:
        return file
    file_without_ext = ""
    
    for i in range(len(file_without_ext_s)-1):
        if i != 0:
            file_without_ext += '.' + file_without_ext_s[i]
        else:
            file_without_ext += file_without_ext_s[i]
    return file_without_ext

def _replace_file_extension(file, extension):
    return _get_file_without_ext(file) + extension

def _get_full_path(file):
    return os.path.abspath(file)

def _generate_fernet_key():
    key = fernet.Fernet.generate_key()
    print('KEY:  ' + key.decode())



if __name__ == "__main__":
    if '-generatekey' in sys.argv:
        _generate_fernet_key()
        sys.exit()

    key = open('../KEY', 'rb').read()

    cmp = compiler(key)
    cmp.compile('testignore.txt', make_original_file=True)

