import git

g = git.cmd.Git(".")
g.pull()

print("pulled")
