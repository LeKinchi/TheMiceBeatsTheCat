#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <string>
#include "TCP_Packet.h"
#include <stdlib.h>
#include <time.h>
#include <iostream>
#include <limits>
#define BUFFER_SIZE 500

using namespace std;

void error(const char *msg)
{
    perror(msg);
    exit(0);
}

bool sendPacket(struct Packet pkt, int sockID, char *buffer, int buffer_size)
{
    bzero(buffer, buffer_size);
    strcpy(buffer, transmitVersion(pkt).c_str());
    std::cout << "sending packet\n";
    for (int i = 0; i < strlen(buffer); i++)
        cout << buffer[i];
    std::cout << std::endl;

    write(sockID, buffer, buffer_size);
    int retry = 0, n = 0;
    do
    {
        n = read(sockID, buffer, 255);
        if (n < 0)
        {
            retry++;
            std::cout << "resendinging transmission\n";
            write(sockID, buffer, buffer_size);
        }
    } while (n < 0 && retry < 1);

    if (n < 0)
    {
        return false;
    }
    struct Packet current_packet = packetify(buffer);
    if (current_packet.packet_type == 3 && current_packet.ack_number == pkt.sequence_number)
        return true;
    else
    {
        struct Packet error(6);
        strcpy(buffer, transmitVersion(error).c_str());
        bzero(buffer, buffer_size);
        write(sockID, buffer, buffer_size);
    }
    return false;
}

int main(int argc, char *argv[])
{
    int sockfd, portno, n;
    struct sockaddr_in serv_addr;
    struct hostent *server;

    char buffer[256];
    if (argc < 3)
    {
        fprintf(stderr, "usage %s hostname port\n", argv[0]);
        exit(0);
    }

    portno = atoi(argv[2]);
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0)
        error("ERROR opening socket");

    server = gethostbyname(argv[1]);

    if (server == NULL)
    {
        fprintf(stderr, "ERROR, no such host\n");
        exit(0);
    }

    bzero((char *)&serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    bcopy((char *)server->h_addr,
          (char *)&serv_addr.sin_addr.s_addr,
          server->h_length);
    serv_addr.sin_port = htons(portno);

    if (connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
        error("ERROR connecting");

    // Starting sequence number
    int sequence_number = 500;
    std::vector<struct Packet> cache;

    struct Packet current_packet;
    bool did_syn = false;

    struct timeval tout;
    tout.tv_sec = 10;
    tout.tv_usec = 0;
    int iResult = setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, &tout, sizeof(tout));
    if (iResult == -1)
    {
        perror("setsockopt() failed with error code: ");
        return -1;
    }
    else
    {
        printf("setsockopt() timeout is set for: %ld\n", tout.tv_usec);
    }

    while (true)
    {
        int choice = 0;
        std::cout << "What to do? \n \t 1 to send a syn, 2 to send an ack, 4 to quit \n";
        std::cin >> choice;

        if (choice == 1)
        { // send a  Syn

            struct Packet response(1, sequence_number++);
            response.buffer_size = BUFFER_SIZE;

            char resp[1024];
            strcpy(resp, transmitVersion(response).c_str());
            write(sockfd, resp, strlen(resp));
            did_syn = true;

            bzero(buffer, 256);
            n = read(sockfd, buffer, 255);
            if (n == 0)
                std::cout << "error reading incoming packet \n";
            current_packet = packetify(buffer);
            printf("Request recieved: \n\t Raw: %s \n\t Pro: %s", buffer, display(current_packet).c_str());
        }

        if (choice == 2)
        { // Resonding an ack
            if (!did_syn)
            {
                std::cout << " Do SYN FIRST\n";
            }
            else
            {
                struct Packet response(3, current_packet.ack_number, current_packet.sequence_number + 1);
                char resp[1024];
                strcpy(resp, transmitVersion(response).c_str());
                write(sockfd, resp, strlen(resp));
                std::cout << "connection established \n";
                break;
            }
        }
        if (choice == 4)
            break;
    }

    while (true)
    {
        int choice = 0;
        std::cout << "What to do? \n \t 1 to send a message, 2 to end communication \n";
        std::cin >> choice;
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        if (choice == 1)
        {
            struct Packet response(5, sequence_number);
            sequence_number++;
            std::cout << "Enter message:\n";
            getline(cin, response.message);
            sendPacket(response, sockfd, buffer, 1024);
            char resp[1024];
            bzero(resp, 1024);
            strcpy(resp, transmitVersion(response).c_str());
            std::cout << "sending " << transmitVersion(response) << std::endl;
            // write(sockfd, resp, strlen(resp));
            // for (int i = 0; i < strlen(buffer); i++)
            // {
            //     cout << buffer[i];
            // }
            // cout << endl;
        }
        if (choice == 2)
            break;
    }

    close(sockfd);
    return 0;
}

// Make sure client and server exchange buffer size duing handshake and malloc the one they said
