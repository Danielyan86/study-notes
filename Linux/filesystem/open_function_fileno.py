with open("test_writelines.txt", "w+", ) as f:
    res = f.fileno()
    print(res)
