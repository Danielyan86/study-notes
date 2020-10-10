# 如果没有换行符
with open("large_file.txt", "w+") as f:
    f.write('*' * 1000000)

with open("large_file.txt") as f:
    for line in f:
        print(line)


def readInChunks(fileObj, chunkSize=2048):
    """
    Lazy function to read a file piece by piece.
    Default chunk size: 2kB.

    """
    while True:
        data = fileObj.read(chunkSize)
        if not data:
            break
        yield data


f = open('large_file.txt')
for chunk in readInChunks(f):
    print(chunk)
    print("\n")
f.close()

# 按照换行符读取
with open("large_file.txt", "w+") as f:
    for num in range(10):
        f.write('- \n')

# f 是一个迭代器类型
with open("large_file.txt") as f:
    for line in f:
        print(line)
