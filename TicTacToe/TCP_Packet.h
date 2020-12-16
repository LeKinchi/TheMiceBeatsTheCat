//
// Created by kinchi on 11/8/20.
//

#ifndef GAME_SERVER_TCP_PACKET_H
#define GAME_SERVER_TCP_PACKET_H


#include <string>
#include <vector>
#include <iostream>

struct Packet
{
    // @packet_type: 1 for syn, 2 for syn-ack, 3 for ack, 4 for retransmission, 5 for data, 6 for error
    int packet_type;
    int sequence_number;
    int ack_number;
    int buffer_size;
    std::string message;

    Packet(): packet_type(0), sequence_number(0), ack_number(0), buffer_size(0){}

    Packet(int Type, int Seq = 0, int Ack = 0): packet_type(Type), sequence_number(Seq), ack_number(Ack), buffer_size(0)
    {}
};

std::string transmitVersion(struct Packet pkt)
{
        return std::to_string(pkt.packet_type) + ';' + std::to_string(pkt.sequence_number) + ';' + std::to_string(pkt.ack_number) + ';'
               + std::to_string(pkt.buffer_size) + ';' + pkt.message +';';
}

struct Packet packetify(std::string raw_pkt) {
    if(raw_pkt.empty())
        return Packet();
    int index = 0;
    std::vector<std::string> parsed_packet;
    parsed_packet.resize(5);


    for (char const &c : raw_pkt) {
        if (c != ';')
            parsed_packet[index] += std::string(1, c);
        else
            index++;
    }

    struct Packet temp;
    temp.packet_type = std::stoi(parsed_packet[0]);
    temp.sequence_number = std::stoi(parsed_packet[1]);
    temp.ack_number = std::stoi(parsed_packet[2]);
    temp.buffer_size = std::stoi(parsed_packet[3]);
    temp.message = parsed_packet[4];

    return temp;
}

std::string display(struct Packet pkt)
{
    std::string type;
    if (pkt.packet_type == 1)
        type = " Syn";
    else if (pkt.packet_type == 2)
        type = " Syn-Ack";
    else if (pkt.packet_type == 3)
        type = " ACK";
    else if (pkt.packet_type == 4)
        type = " RETRANS";
    else if (pkt.packet_type == 5)
        type = " DATA";
    if (pkt.packet_type == 6)
        type = " ERROR";

    std::string temp;
    temp += "Packet Type: " + type + "; ";
    temp += "Sequ Number: " + std::to_string(pkt.sequence_number) + "; ";
    temp += "ACK Number: " + std::to_string(pkt.ack_number) + "; ";
    temp += "Buffer Size: " + std::to_string(pkt.buffer_size) + "; ";
    temp += "Message: " + pkt.message + ";\n";

    return temp;
}


#endif //GAME_SERVER_TCP_PACKET_H
