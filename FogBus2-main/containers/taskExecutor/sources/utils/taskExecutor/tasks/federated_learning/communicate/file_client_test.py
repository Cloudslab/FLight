import ftplib
if __name__ == "__main__":
    print(2)

    server = ftplib.FTP()
    server.connect('127.0.0.1', 12345)
    server.login('123', 'kokchkhamyuxsyqpkvbxiimpncdvbxbd')
    server.abort()
    print(111)
    print(server.dir())
    server.quit()
    server.close()
    print(111)

    filename = "./sample_download.txt"
    #with open(filename, "wb") as file:
    #    server.retrbinary(f"RETR {remote_file_name}", file.write)
    #    server.close()