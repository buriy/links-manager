import os.path
DOT_DIRS = '.dirs'
DOT_LINKS = '.links'
USER_DIR = os.getenv('HOME')

def split_line(l):
    l = l.split('#', 1)[0] # split comments
    return [x.strip() for x in l.split('=', 1) if '=' in l]

def read_dot_dirs(root):
    path_list = [USER_DIR, root]
    dirs = {}
    for source in path_list:
        dirs.update(read_dot_dirs_file(source))
    return dirs

def norm_path(path):
    path = path.strip().replace(os.sep, '/')
    if not path.endswith('/'):
        return path + '/'
    return path

def read_dot_dirs_file(path):
    dirs = {}
    filename = os.path.join(path, DOT_DIRS)
    if not os.path.exists(filename):
        return dirs
    for l in open(filename, 'rt').readlines():
        short, real = split_line(l)
        dirs[short] = norm_path(real)
    return dirs

def read_dot_links(path):
    filename = os.path.join(path, DOT_LINKS)

    dirs = read_dot_dirs(path)

    links = {}

    if not os.path.exists(filename):
        return dirs, links

    for l in open(filename, 'rt').readlines():
        symlink, real = [x.replace(os.sep, '/') for x in split_line(l)]
        if symlink.startswith('/'): 
            symlink = symlink[1:]
        is_rel = not os.path.isabs(real)
        if is_rel and ('/' in real):
            head, tail = real.split('/', 1)
            if head in dirs:
                real = os.path.join(dirs[head], tail)
        links[symlink] = real
    return dirs, links

def find_shortener(path, dirs):
    key = ""
    value = ""
    for k, v in dirs.iteritems():
        if path.startswith(v):
            if len(v) > len(value):
                key, value = k, v
    if k and v:
        return path.replace(value, key + '/', 1)
    return path

def write_dot_links(root, links):
    reals = []
    dirs = read_dot_dirs(root)
    for symlink, realpath in links:
        path = find_shortener(realpath, dirs)
        reals.append((symlink, path))
    
    write_dot_file(root, DOT_LINKS, reals)

def write_dot_dirs(path, dirs):
    write_dot_file(path, DOT_DIRS, dirs)

def write_dot_file(path, name, values):
    filename = os.path.join(path, name)
    w = open(filename, 'wt')
    if isinstance(values, dict) or hasattr(values, 'iteritems'):
        values = sorted(values.iteritems())
    for k, v in values:
        line = u"%s = %s\n" % (k, v)
        w.write(line.encode('utf-8'))
    w.close()

