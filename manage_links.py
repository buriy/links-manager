import os
from opster import dispatch, command
from links_manager.links import find_links, create_link, remove_link
from links_manager.dotfiles import read_dot_links, write_dot_links
from links_manager.dotfiles import read_dot_dirs, write_dot_dirs, norm_path
from links_manager.dotfiles import read_dot_dirs_file, USER_DIR

@command(usage="%name ROOT")
def links_show(cmd, root=('r', '.', 'Root directory')):
    """Show all links in project filesystem"""
    links = find_links(root)
    _dirs, saved = read_dot_links(root)
    for symlink, real_dir in links:
        if symlink in saved:
            if real_dir in saved[symlink]:
                status = ' '
            else:
                status = '*'
        else:
            status = '+'
        print "%s %-30s %s" % (status, symlink, real_dir)
    for symlink, real_dir in sorted(saved.iteritems()):
        if not (symlink, real_dir) in links:
            status = '-'
            print "%s %-30s %s" % (status, symlink, real_dir)

def links_reset(root, verbose, force):
    """Reset links data from .links file"""
    _dirs, links = read_dot_links(root)
    fs_pairs = find_links(root)
    fs_links = [k for k, _v in fs_pairs]
    for link, real_dir in links.iteritems():
        if not link in fs_links:
            if verbose:
                print "Creating link %s to %s" % (link, real_dir)
            if not os.path.exists(real_dir):
                print "Warning: Target path %s does not exist" % real_dir
                if not force: break
            create_link(root, link, real_dir)
        elif not (link, real_dir) in fs_pairs:
            if verbose:
                print "Updating link %s to %s" % (link, real_dir)
            if not os.path.exists(real_dir):
                print "Warning: Target path %s does not exist" % real_dir
                if not force: break
            remove_link(root, link)
            create_link(root, link, real_dir)
    for link, real_dir in fs_pairs:
        if not link in links:
            if verbose:
                print "Removing link %s (pointed to %s)" % (link, real_dir)
            remove_link(root, link)


@command(usage="%name ROOT")
def links_commit(cmd, root=('r', '.', 'Root directory')):
    "Commit links data into .links file"
    write_dot_links(root, find_links(root))

@command(usage="%name ROOT")
def links_list(cmd, root=('r', '.', 'Root directory')):
    """Show dirs shortcuts allowed in .links files"""
    _dirs, links = read_dot_links(root)
    for link, real_dir in links.iteritems():
        print "%-30s %s" % (link, real_dir)

@command(usage="%name")
def dirs_list(cmd, root=('r', '.', 'Root directory')):
    """Show all dirs in project filesystem"""
    for link, real_dir in read_dot_dirs(root).iteritems():
        print "%-30s %s" % (link, real_dir)


def dirs_add(src, dest, user_home, root):
    """Add entry into .dirs file (in project root or global)"""
    if user_home:
        path = USER_DIR
    else:
        path = root
    dirs = read_dot_dirs_file(path)
    dirs[src] = norm_path(dest)
    write_dot_dirs(path, dirs)

#@command(usage="%name ROOT")
#def dirs_suggest(cmd, root='.'):
#    """Suggest dirs in project filesystem"""
#    roots = []
#    for link, real_dir in find_links(root):

def main():
    #import sys; print sys.argv
    dispatch(cmdtable={
       'dirs': (dirs_list, [], ''),
       'dirs-add': (dirs_add, [('u', 'user_home', False, 'Write into user home directory'),
                               ('r', 'root', '.', 'Root directory')],
                                "%name SOURCE DESTINATION"),
       #'dirs-remove': (dirs_show, []),
       #'dirs-suggest': (dirs_suggest, []),
       'show': (links_show, [], ''),
       'list': (links_list, [], ''),
       'reset': (links_reset, [('r', 'root', '.', 'Root directory'), 
                               ('v', 'verbose', False, 'Verboseness'),
                               ('f', 'force', False, 'Ignore warnings')], ''),
       'commit': (links_commit, [], ''),
    })

if __name__ == "__main__":
    main()

