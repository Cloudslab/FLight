"""
Sending message to message receiver on other nodes, the reason that use TPC instead of UDP is:
1. The framework is not that performance aware (few sec delay between message is fine)
2. Ref: https://stackoverflow.com/questions/47903/udp-vs-tcp-how-much-faster-is-it Through put control
3. Model communication which is the most communication consuming tasks does not pass through this module
(FTP of warehouse instead)
4. Reliability
"""