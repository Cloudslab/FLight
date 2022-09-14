import ftplib
if __name__ == "__main__":
    print(2)

    server = ftplib.FTP()
    server.connect('127.0.0.1', 2121)
    server.login('myuser', 'change_this_password')
    print(111)
    print(server.dir())
    print(111)
    filename = "./sample_download.txt"
    remote_file_name = "./sample.txt"
    with open(filename, "wb") as file:
        server.retrbinary(f"RETR {remote_file_name}", file.write)
        server.close()