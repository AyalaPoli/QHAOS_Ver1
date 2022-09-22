
import struct


class Packet(object):
    base_packet_format = "< H B B B H "
    header = 0xAA55

    def __init__(self, params_format):
        self.params_format=self.base_packet_format+params_format

    def pack_data(self):
        self.s=struct.Struct(self.params_format)
        lst_to_pack=(self.header, self.packet_index, self.internal_num, self.op_code, self.size)+self.parameters_lst
        #lst_to_pack=(self.header, self.packet_index, self.internal_num, self.op_code, self.size)+self.parameters_lst
        self.packed_data = self.s.pack(*lst_to_pack)

    def unpack_data(self):
        self.s=struct.Struct(self.params_format)
        self.header, self.packet_index, self.internal_num, self.op_code, self.size, self.parameters_lst=self.s.unpack(self.packed_data)
        #self.header=hex(self.header)

    def get_index(self):
        return self.packet_index

    def is_start_experiment_packet(self):
        if self.op_code==0 and self.parameters_lst==0:
            return True
        return False

    def is_stop_experiment_packet(self):
        if self.op_code==0 and self.parameters_lst==1:
            return True
        return False


    def __repr__(self):
       return "Packet object: header: {}, index: {} op code: {} internal num: {} params_lst={} params_format: {} size: {}".\
           format(self.header, self.packet_index, self.op_code, self.internal_num, self.parameters_lst, self.params_format, self.size)

class Sent_Packet(Packet):

    def __init__(self, op_code, params_format, parameters_lst, packet_index):
        super().__init__(params_format)
        self.packet_index=packet_index
        self.op_code=op_code
        self.internal_num=1
        self.parameters_lst=parameters_lst
        self.size=struct.calcsize("="+params_format) #no alignment padding between members
        #print("self.size")
        #print(self.size)
        self.pack_data()

class Received_Packet(Packet):

    def __init__(self, packed_data, params_format):
        super().__init__(params_format)
        self.packed_data=packed_data
        self.unpack_data()
