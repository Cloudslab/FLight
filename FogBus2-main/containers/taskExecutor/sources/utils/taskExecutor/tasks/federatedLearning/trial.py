from communicate.router import router
if __name__ == "__main__":
    r = router("127.0.0.1", 12347)
    r.send(("127.0.0.1",12345) ,"register", b"hello")
