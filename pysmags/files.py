def toFile(filename, content, lines=False):
    if lines:
        f = open(filename, 'w')
        for line in content:
            f.write(f"{line}\n")
        f.close()
        return
    f = open(filename, 'w')
    f.write(content)
    f.close()

def toFileB(filename, content):
    f = open(filename, 'wb')
    f.write(content)
    f.close()