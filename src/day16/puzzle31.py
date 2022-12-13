from src.data_parser import parser


class Packet:
    def __init__(self, version, type_id):
        self.version = version
        self.type_id = type_id


class LiteralPacket(Packet):
    def __init__(self, version, type_id, groups):
        super().__init__(version, type_id)
        self.groups = groups
        self.literal_value = self.count_literal_value()

    def count_literal_value(self):
        return int(''.join(group[1:] for group in self.groups), 2)


class OperatorPacket(Packet):
    def __init__(self, version, type_id, sub_pockets):
        super().__init__(version, type_id)
        self.sub_packets = sub_pockets

    def sum_up_version_numbers(self):
        version_sum = 0

        for packet in self.sub_packets:
            version_sum += packet.version

            if isinstance(packet, OperatorPacket):
                version_sum += packet.sum_up_version_numbers()

        return version_sum


class Decoder:
    def __init__(self, message):
        self.message = message
        self.binary = self.convert_into_binary()
        self.packet = self.decode_packet()[0]

    def convert_into_binary(self):
        def align_number(n):
            length = len(n)
            return '0' * (4 - length) + n

        binary = ''
        for num in self.message:
            num = align_number(bin(int(num, 16))[2:])
            binary += num

        return binary

    def get_version_and_type_id(self, idx):
        version = int(self.binary[idx:idx + 3], 2)
        idx += 3
        type_id = int(self.binary[idx:idx + 3], 2)
        return version, type_id

    def decode_literal(self, version, idx):
        groups = []
        first_bit = self.binary[idx]

        while first_bit == '1':
            groups.append(self.binary[idx:idx + 5])
            idx += 5
            first_bit = self.binary[idx]

        groups.append(self.binary[idx: idx + 5])
        idx += 5

        packet = LiteralPacket(version, 4, groups)
        return packet, idx

    def decode_operator(self, version, type_id, idx):
        length_type_id = self.binary[idx]
        idx += 1

        if length_type_id == '0':
            total_length_in_bits = int(self.binary[idx:idx + 15], 2)
            idx += 15
            sub_packets, idx = self.decode_packets(idx, idx + total_length_in_bits)
        else:
            number_of_sub_packets = int(self.binary[idx:idx + 11], 2)
            idx += 11
            sub_packets, idx = self.decode_packets(idx, bits=False, sub_packets=number_of_sub_packets)

        packet = OperatorPacket(version, type_id, sub_packets)
        return packet, idx

    def decode_packet(self, idx=0):
        version, type_id = self.get_version_and_type_id(idx)
        idx += 6

        if type_id == 4:
            packet, idx = self.decode_literal(version, idx)
        else:
            packet, idx = self.decode_operator(version, type_id, idx)

        return packet, idx

    def decode_packets(self, idx, end=None, bits=True, sub_packets=0):
        packets = []

        if bits:
            end = end if end else len(self.binary)
            while end != idx:
                packet, idx = self.decode_packet(idx)
                packets.append(packet)
        else:
            while len(packets) != sub_packets:
                packet, idx = self.decode_packet(idx)
                packets.append(packet)

        return packets, idx

    def sum_up_version_numbers(self):
        version_sum = self.packet.version
        if isinstance(self.packet, OperatorPacket):
            version_sum += self.packet.sum_up_version_numbers()
        return version_sum


def process_data(data):
    data = data[0][:-1]
    dc = Decoder(data)
    return dc


def sum_versions(data):
    dc = process_data(data)
    return dc.sum_up_version_numbers()


if __name__ == '__main__':
    test_data = parser("input/day16_test1")
    actual_data = parser("input/day16")

    for d in test_data:
        print(sum_versions([d]))
    print(sum_versions(actual_data))
