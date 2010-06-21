import os.path

kdll = None

def get_kernel():
    global kdll
    if kdll is None:
        import ctypes
        kdll = ctypes.windll.LoadLibrary("kernel32.dll")
    return kdll


def _get_linked_path(h, bufsize=200):
    kdll = get_kernel()
    buf = ' '*bufsize
    readsize = kdll.GetFinalPathNameByHandleA(h, buf, bufsize, 0)
    if readsize >= bufsize: # not read
        return _get_linked_path(h, readsize+1)
    buf = buf[:readsize] # strip out
    return buf

FILE_ATTRIBUTE_REPARSE_POINT = 0x400
FILE_ATTRIBUTE_DIRECTORY = 0x10

def is_symlink(x):
    if os.name != 'nt':
        return os.path.islink(x)
    kdll = get_kernel()
    attrs = kdll.GetFileAttributesA(x)
    total = FILE_ATTRIBUTE_DIRECTORY | FILE_ATTRIBUTE_REPARSE_POINT
    return attrs & total == total

def get_real_path(x):
    if os.name != 'nt':
        return os.path.realpath(x)
    kdll = get_kernel()
    h=kdll.CreateFileA(x, 0, 0, None, 3, 0x02000000, None)
    path = _get_linked_path(h)
    kdll.CloseHandle(h)
    if path.startswith('\\\\?\\'):
        path = path[4:]
    return os.path.abspath(path)
    
def find_links(root):
    links = []
    for path, dirs, _files in os.walk(root):
        for d in dirs: 
            x = os.path.join(path, d)
            t = os.path.relpath(x, root)
            if is_symlink(x):
                link_path = '/%s/' % t.replace(os.sep,'/')
                real_path = get_real_path(x).replace(os.sep, '/')
                links.append((link_path, real_path))

    return links
