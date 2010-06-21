from opster import dispatch, command
from links_manager.links import find_links
from links_manager.dotfiles import read_dot_links, write_dot_links, read_dot_dirs

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
        

@command(usage="%name ROOT")
def links_reset(cmd, root=('r', '.', 'Root directory')):
    """Reset links data from .links file"""
    _dirs, links = read_dot_links(root)
    fs_pairs = find_links(root)
    fs_links = [k for k, _v in fs_pairs]
    for link, real_dir in links.iteritems():
        if not link in fs_links:
            print "Creating link %s to %s" % (link, real_dir)
        elif not (link, real_dir) in fs_pairs:
            print "Updating link %s to %s" % (link, real_dir)
    for link, real_dir in fs_pairs:
        if not link in links:
            print "Removing link %s (pointed to %s)" % (link, real_dir)
            

@command(usage="%name ROOT")
def links_commit(cmd, root=('r', '.', 'Root directory')):
    "Commit links data into .links file"
    write_dot_links(root, find_links(root))

@command(usage="%name ROOT")
def links_list(cmd, root=('r', '.', 'Root directory')):
    """Show dirs shortcuts allowed in .links files"""
    _dirs, links = read_dot_links(root)
    for link, real_dir in links:
        print "%-30s %s" % (link, real_dir)

@command(usage="%name ROOT")
def dirs_list(cmd, root=('r', '.', 'Root directory')):
    """Show all dirs in project filesystem"""
    for link, real_dir in read_dot_dirs(root).iteritems():
        print "%-30s %s" % (link, real_dir)

#@command(usage="%name ROOT")
#def dirs_suggest(cmd, root='.'):
#    """Suggest dirs in project filesystem"""
#    roots = []
#    for link, real_dir in find_links(root):

def main():
    dispatch(cmdtable={
       'dirs': (dirs_list, []),
       #'dirs-add': (dirs_show, []),
       #'dirs-remove': (dirs_show, []),
       #'dirs-suggest': (dirs_suggest, []),
       'links-show': (links_show, []),
       'links-list': (links_list, []),
       'links-reset': (links_reset, []),
       'links-commit': (links_commit, []),
    })

if __name__ == "__main__":
    main()
