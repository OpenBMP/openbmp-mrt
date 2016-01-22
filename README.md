OpenBMP MRT
===========
A lightweight OpenBMP consumer that dumps BMP messages on a time based interval to a file.
The MRT file can then be loaded in any compliant MRT parser.  Validation testing has been with
[libbgpdump](https://bitbucket.org/ripencc/bgpdump/wiki/Home).

**[RFC6396](https://tools.ietf.org/html/rfc6396)** - Multi-Threaded Routing Toolkit (MRT) Routing Information Export Format

* BGP4MP_STATE_CHANGE_AS4 - Peer up/down events
* BGP4MP_MESSAGE - BGP update messages
* TABLE_DUMP_V2 - Table dumps require the use of openbmp-mysql-consumer/db_rest

> #### NOTE
> Apparently libbgpdump does not support extended time mrt headers.  For this reason the dumps
> do not include microsecond precision, even though that data is available in BMP.  This can
> be easily updated to allow either non-ET or ET messages by configuration.

BGP4MP Support
--------------
State change messages as well as update messages are logged in MRT BGP4MP format.  Considering
the feed is from a message bus (kafka) which may have existed for a while, there is a chance that
BMP PEER UP/DOWN messages are not seen because those were sent a while back.  In this case UPDATE messages
are still received but since the UP/OPEN message has yet been seen, the BGP4MP_MESSAGE_AS4 header will
have **Local AS Number** set to zero and **Local IP Addresss** set to loopback (127.0.0.1 or ::1).
This has **no impact** on BGP parsing. Once the PEER UP/DOWN messages are seen, the local variables will be
populated.

> It should be noted that **Interface Index** is always **zero**.   We can populate this, but is it really
> needed?  If so, please submit an issue asking for it. You can also do a pull request to submit
> a change.


TABLE_DUMP Support
------------------
MRT TABLE_DUMP_V2 is a *SNAPSHOT* in time per **COLLECTOR** -->  **ROUTER** --> **PEER**.  This requires continual
state tracking in order to know which NLRI's (by address family) are current (not withdrawn) for the snapshot
period.  [DB_REST](https://github.com/openbmp/db_rest) via the MySQL/MariaDB consumer is used to handle the state
tracking.   TABLE_DUMP_V2 is enabled by configuration, specifically by defining the the DB_REST hostname and port.

Installation
------------
You can either run the code within the **git** directory or you can install it in your python path. 

> If you are going to run it within the **git** directory, see running instructions.  

### Install Dependencies:
    
    sudo apt-get install python-dev python-pip libsnappy-dev
    sudo pip install python-snappy
    sudo pip install kafka-python
    sudo pip install pyyaml


### Install:

    git clone https://github.com/OpenBMP/openbmp-mrt.git
    cd openbmp-mrt
    sudo python setup.py install

Configuration
-------------
Configuration is in YAML format.  See [src/etc/openbmp-mrt.yml](src/etc/openbmp-mrt.yml) for configuration example
and details.

Running
-------
If you install the python code, then you should be able to run from a terminal

    openbmp-mrt -c <configuration file>
    
If you are running from within the **git** directory, you can run it as follows:

    PYTHONPATH=./src/site-packages python src/bin/openbmp-mrt -c src/etc/openbmp-mrt.yml

    
#### Usage
```
Usage: src/bin/openbmp-mrt [OPTIONS]

OPTIONS:
  -h, --help                  Print this help menu
  -c, --config                Config filename (default is sys.prefix/etc/openbmp-mrt.yml)
```

#### Configuration
Configuration is in YAML format via the **openbmp-mrt.yml** file.  See the file for details.


