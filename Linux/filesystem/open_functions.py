# write 方法，返回传入字符串长度
with open("test_write.txt", "w", ) as f:
    f.write("123\n")
    res = f.write("456\n")
    print(res)

# read
with open("test_write.txt", "r", ) as f:
    content = f.read(1)
print(f"read one size charactor:{content}")

# writelines 写入一个list 返回None
with open("test_writelines.txt", "w", ) as f:
    res = f.writelines(['1\n', '2\n', '3\n'])

# readline
with open("test_writelines.txt", "r", ) as f:
    content = f.readline()
    print("judge write mode {}".format(f.writable()))
    print("judge read mode {}".format(f.readable()))
    print("judge current file is connected to terminal device {}".format(f.isatty()))
    print("current file pointer is {}".format(f.tell()))
    print("print file descriptor {}".format(f.fileno()))
print(f"read one line: {content}")

# readlines
with open("test_writelines.txt", "r", ) as f:
    content = f.readlines()
print(f"read content as list {content}")

with open("test_writelines.txt", "r", ) as f:
    content = f.read()
print(f"read content as list {content}")

# writelines 超长字符串测试
string = "1" * 1000000
with open("test_writelines_long_string.txt", "w", ) as f:
    f.writelines(string)
print("print file descriptor {}".format(f.fileno()))
