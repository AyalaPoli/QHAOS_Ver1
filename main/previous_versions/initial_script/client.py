from main.previous_versions.initial_script.client_functions import *
import time

print("Start client")


s=socket.socket(address_family, socket_type)
s.connect((host, port))
current_time = time.ctime(time.time())
print("host: {}\nport: {}".format(host,port))
print("{}\tGot connected to the server".format(current_time))
connection_ok=show_connection_message(host,port,current_time)


timestr = time.strftime("%Y%m%d-%H%M%S")
client_file_valid=False
while not client_file_valid:
    client_file, received_from_server_file=get_client_files_from_GUI(host, timestr)
    mgs=is_valid_experiment_file(client_file)
    if (mgs==valid_message):
        client_file_valid=True
        show_file_validation_message(client_file)

print("client_file")
print(client_file)
print("received_from_server_file")
print(received_from_server_file)
s.send(client_file.encode(FORMAT))
s.send(received_from_server_file.encode(FORMAT))

curr_device=device_choose_flow()

loop_experiment_num=get_expeiment_num_from_GUI()

start_experiment_ok=show_experiment_start_message(client_file, curr_device, loop_experiment_num)

current_time = time.ctime(time.time())
experiment_sent=show_experiment_sent_message(client_file, curr_device, loop_experiment_num, current_time)


f=open(client_file, "rb")
print("{}\tStart sending file: {} to the server  ".format(current_time, client_file))

l=f.read(BUFFER_SIZE)
while(l):
    s.send(l)
    l=f.read(BUFFER_SIZE)
f.close()

print("{}\tDone sending file {} to the server".format(current_time, client_file, ))

print("{}\tStart receiving data to file {} from the server".format(current_time, received_from_server_file))

with open(received_from_server_file, 'wb') as f:
    print ("\t\topen file for writing: {}".format(received_from_server_file))
    #receive data from server
    while True:
        data=s.recv(BUFFER_SIZE)
        print ("\t\tGot data from server {}".format(data))
        f.write(data)
        if not data:
            break
f.close()

print("{}\tDone receiving file {} from the server:".format(current_time, received_from_server_file))
s.close()
current_time = time.ctime(time.time())
print("{}\tEnd of connection".format(current_time))

