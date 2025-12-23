---
layout: default
title: The previous NIC Data server
author: Stuurman, Nico
---

## Accessing the previous NIC Server 

\

Note: this server will soon be de-commissioned.   Use the newer server
(with much more space and faster access) instead.

\

The NIC maintains an 8 TB file server for temporary storage of data
acquired in the NIC to allow for easy transport of data between
microscopes, our offline analysis systems, and any other computer at
UCSF. It is not accessible from outside the UCSF network.

To access the server from Windows:

1.  Open a windows explorer window and go to Tools → Map Network Drive

2.  Pick an unused drive letter and type [\\\\nicdata\\data]{.windows
    rel="nofollow"}

3.  Login using the same nicuser account you use to login to the
    microscopes.

From Mac:

1.  In the Finder go to Go → Connect to Sever

2.  Enter
    [smb://nicdata.ucsf.edu/data](smb://nicdata.ucsf.edu/data){rel="nofollow"}

3.  Enter CAMPUS in the Workgroup/Domain field and the nicuser username
    and password.

Once you\'ve logged on to the server, create a folder to store your
files in. Then save data to your heart's content.