# OS Project: Remote Command Execution System
This project is a simple **Client–Server application** built in Python that allows multiple clients to connect to a server and execute system commands remotely.  
It demonstrates the use of **socket programming** and **multithreading** in operating systems and networking.

## Features
- Supports **multiple clients** simultaneously using Python threads.  
- Clients can execute common system commands (`dir`, `cd`, `ls`, `pwd`, etc.).  
- The server executes the commands and sends the output back to each client.  
- Fully written in **Python**, using only built-in libraries (`socket`, `os`, `threading`, `subprocess`).  

## How to Run
- Run the Server first and then run the client.
