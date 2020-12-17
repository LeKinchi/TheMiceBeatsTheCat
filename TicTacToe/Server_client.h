//
// Created by Kinchi on 11/11/20.
//

#ifndef GAME_SERVER_CLIENT_H
#define GAME_SERVER_CLIENT_H


#pragma once

#include <cstdlib>
#include <cstring>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h> //sockaddr, socklen_t
#include <arpa/inet.h>
#include <netdb.h>
#include <iostream>
#include <set>
#include <vector>
#include <string>

#define SERVER_DEBUG 0

#define INPUT_BUFFER_SIZE 100 //test: 100 bytes of buffer
#define DEFAULT_PORT 9034

class Client {
public:

    // calls setup with DEFAULT_PORT
    Client();

    // Calls setup with the arg passed
    Client(int port);

    // closes the socket(mastersocket)
    ~Client();

    // closes the socket(mastersocket)
    void shutdown();

    // It initializes the socket  by calling
    //       initializeSocket(), bindSocket(),startListen()
    void init();

    // Checks for new connection or new message
    void loop();

    uint16_t sendMessage(const char *messageBuffer);
    uint16_t sendMessage(char *messageBuffer);
    uint16_t sendMessageStr( std::string messageBuffer);

    std::vector<std::string> getHistory();
private:

    std::string last_message;


    struct hostent *server;

    // pseudo tcp connection sequence number
    int sequence_number;

    int actual_buffer_size = INPUT_BUFFER_SIZE;

    //Holds the fd of all active socket connections
    std::set<int> client_fd;

    //fd_set file descriptor sets for use with FD_ macros
    fd_set masterfds;
    fd_set tempfds;

    //unsigned integer to keep track of maximum fd value, required for select()
    uint16_t maxfd;

    //socket file descriptors
    int mastersocket_fd; //master socket which receives new connections
    int tempsocket_fd; //temporary socket file descriptor which holds new clients

    //client connection data
    struct sockaddr_storage client_addr;

    //server socket details
    struct sockaddr_in serv_addr, cli_addr;

    //input buffer
    char input_buffer[INPUT_BUFFER_SIZE];

    //function prototypes

    // initializes socket address
    void setup(int port, std::string hostname="localhost" );

    //set option on socket to reuse-address
    void initializeSocket();

    // connect to outside host
    void connectSocket();


    // receives input from socket if not handles error and disconnect and remove from masterfds
    void recvInputFromExisting(int fd);
    std::string recvInputFromExistingStr(int fd);

    void handShake(int fd);


    void SendSyn();
};


#endif //GAME_SERVER_SERVER_H
