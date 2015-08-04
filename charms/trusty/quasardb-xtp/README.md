# Overview

[quasardb](https://www.quasardb.net/) is a distributed key-value store. It scales horizontally and vertically for virtually unlimited capabilities. 
 
You can store raw data of any form and size into quasardb, but should you need to, you can also do atomic operations on integers, manipulate queues and sets. 
 
quasardb is write-safe by default and offers features to sync absolutely everything you do for maximum safety. 
 
Thanks to its master-less design, quasardb is able to face the loss of nodes transparently. 

# Usage

    juju deploy quasardb-xtp

## Scale up

    Scale up is automatic. Increase the number of cores in your VM and restart the node instance.

## Scale out

Please follow these two steps:

 1. juju add-unit quasardb-xtp
 2. There is no second step

# Configuration

## Networking configuration

The default listening ports for quasardb is 2836 and the administration console and REST APIs are on 8080. This can be configured.

It also also possible to change the timeouts values although we advise to leave them intact.

## Eviction configuration

You can configure the maximum number of items and the total maximum size you want to have in memory. This parameter is identical on *all nodes* and will be replicated accross nodes.

If you specify 0 for the maximum size, it will be automatically computed depending on the amount of RAM available on the machine.

# Contact information

 - Web site: [https://www.quasardb.net/](https://www.quasardb.net/)
 - Documentation: [https://doc.quasardb.net/](https://doc.quasardb.net/)
 - Bug tracking: [https://quasardb.zendesk.com/](https://quasardb.zendesk.com/)
