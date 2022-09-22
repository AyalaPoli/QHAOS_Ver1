from main.previous_versions.client_server_params import *
from main.previous_versions.initial_script.server_functions import *
import time

print("Start server")
s=socket.socket(address_family, socket_type)
current_time = time.ctime(time.time())

s.bind((host, port))
print("host: {}\nport: {}".format(host,port))
s.listen(listen_param)
current_time = time.ctime(time.time())
print("{}\tServer start listening".format(current_time))

# change print to conn.send("message".encode(FORMAT))
# and in the client side msg = client.recv(SIZE).decode(FORMAT)

while True:
    conn, addr = s.accept()
    current_time = time.ctime(time.time())
    print("{}\tConnected with client: {} ".format(current_time,addr))

    #get input and output filename
    experiment_filename=conn.recv(BUFFER_SIZE).decode(FORMAT)
    basename=os.path.basename(experiment_filename)
    recieved_from_client_file=add_to_path(received_from_client_dir,basename)
    print("received Experiment file in {}".format(recieved_from_client_file))

    output_filename=conn.recv(BUFFER_SIZE).decode(FORMAT)
    basename=os.path.basename(output_filename)
    send_to_client_file=add_to_path(sent_from_server_dir, basename)
    print("sent to output in {}".format(send_to_client_file))

    #get file from client
    infile=open(recieved_from_client_file, "wb")
    data = conn.recv(BUFFER_SIZE)
    current_time = time.ctime(time.time())
    print("{}\tServer received data: {}".format(current_time,data))
    if not data:
        break
    infile.write(data)
    infile.close()

    #process input file
    current_time = time.ctime(time.time())
    msg=process_experiment_file(recieved_from_client_file, send_to_client_file)
    print("{}\tDone processing file in server. Output message: {}".format(current_time, msg))

    #Send file in buffer sizes
    f=open(send_to_client_file, 'rb')
    l=f.read(BUFFER_SIZE)
    while (l):
        conn.send(l)
        print("Server sent {}".format(l))
        l=f.read(BUFFER_SIZE)
    current_time = time.ctime(time.time())
    print("{}\tDone sending output file, ending connection\n".format(current_time))
    conn.close()
    f.close()

s.close()
print("{}\tServer abort".format(current_time))
