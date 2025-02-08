# CyberBivash001

A network scanner to scan open ports , services in the local network .

unittest >>>

(.venv) C:\Users\Administrator\Documents\Test\nw_scanner> python network_scanner.py -n 192.168.1.1/32 -p 80,443,8080,22

Starting host discovery...
    Active Hosts in
     192.168.1.1/32
┏━━━━━━━━━━━━━┳━━━━━━━━┓
┃ IP Address  ┃ Status ┃
┡━━━━━━━━━━━━━╇━━━━━━━━┩
│ 192.168.1.1 │ Active │
└─────────────┴────────┘

Scanning ports for 192.168.1.1...
 Open Ports for
   192.168.1.1
┏━━━━━━┳━━━━━━━━┓
┃ Port ┃ Status ┃
┡━━━━━━╇━━━━━━━━┩
│ 80   │ Open   │
│ 443  │ Open   │
└──────┴────────┘

(.venv) C:\Users\Administrator\Documents\Test\nw_scanner>
