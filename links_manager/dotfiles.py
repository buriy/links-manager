import os.path
DOT_DIRS = '.dirs'
DOT_LINKS = '.links'

def split_line(l):
    l = l.split('#', 1)[0] # split comments
    return [x.strip() for x in l.split('=', 1) if '=' in l]

def read_dot_dirs(path):
    dirs = {}
    for source in [path, os.getenv('HOME')]:
        filename = os.path.join(source, DOT_DIRS)
        if not os.path.exists(filename):
            continue
        for l in open(filename, 'rt').readlines():
            short, real = split_line(l)
            dir = real.replace(os.sep, '/')
            if not dir.endswith('/'):
                dir += '/'
            dirs[short] = dir
    return dirs

def read_dot_links(path):
    filename = os.path.join(path, DOT_LINKS)

    dirs = read_dot_dirs(path)

    links = {}
    for l in open(filename, 'rt').readlines():
        symlink, real = [x.replace(os.sep, '/') for x in split_line(l)]
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

def write_dot_file(path, name, values):
    filename = os.path.join(path, name)
    w = open(filename, 'wt')
    if isinstance(values, dict) or hasattr(values, 'iteritems'):
        values = sorted(values.iteritems())
    for k, v in values:
        line = u"%s = %s\n" % (k, v)
        w.write(line.encode('utf-8'))
    w.close()
