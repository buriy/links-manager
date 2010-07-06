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

def relpath(path, start):
    """Return a relative version of a path"""

    if not path:
        raise ValueError("no path specified")

    start_list = os.path.abspath(start).split(os.sep)
    path_list = os.path.abspath(path).split(os.sep)

    if os.name == 'nt':
        if start_list[0].lower() != path_list[0].lower():
            unc_path, rest = os.path.splitunc(path)
            unc_start, rest = os.path.splitunc(start)
            if bool(unc_path) ^ bool(unc_start):
                raise ValueError("Cannot mix UNC and non-UNC paths (%s and %s)"
                                                                % (path, start))
            else:
                raise ValueError("path is on drive %s, start on drive %s"
                                                % (path_list[0], start_list[0]))
        for i in range(min(len(start_list), len(path_list))):
            if start_list[i].lower() != path_list[i].lower():
                break
        else:
            i += 1

    else:
        # Work out how much of the filepath is shared by start and path.
        i = len(os.path.commonprefix([start_list, path_list]))

    rel_list = [os.pardir] * (len(start_list)-i) + path_list[i:]
    if not rel_list:
        return curdir
    return os.path.join(*rel_list)

def find_links(root):
    links = []
    for path, dirs, _files in os.walk(root):
        for d in dirs: 
            x = os.path.join(path, d)
            t = relpath(x, root)
            if is_symlink(x):
                link_path = '%s/' % t.replace(os.sep,'/')
                real_path = get_real_path(x).replace(os.sep, '/')
                links.append((link_path, real_path))

    return links

def create_link(root, link, real):
    if link.startswith('/'):
        link = link[1:]
    if link.endswith('/'):
        link = link[:-1]
    x = os.path.join(root, link)
    if os.name != 'nt':
      return os.symlink(real, x)
    print "Not implemented yet. Please create manually: ", x, '->', real

def remove_link(root, link):
    if link.startswith('/'):
        link = link[1:]
    if link.endswith('/'):
        link = link[:-1]
    x = os.path.join(root, link)
    return os.unlink(x)

