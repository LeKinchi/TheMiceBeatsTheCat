//
// Created by Kinchi on 11/11/20.
//

#ifndef GAME_SERVER_SERVER_H
#define GAME_SERVER_SERVER_H

#include <cstdio>
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



#define SERVER_DEBUG 0

#define INPUT_BUFFER_SIZE 100 //test: 100 bytes of buffer
#define DEFAULT_PORT 9034

class Server {
public:

    // calls setup with DEFAULT_PORT
    Server();

    // Calls setup with the arg passed
    Server(int port);

    // closes the socket(mastersocket)
    ~Server();

    // closes the socket(mastersocket)
    void shutdown();

    // It initializes the socket  by calling
    //       initializeSocket(), bindSocket(),startListen()
    void init();

    // Checks for new connection or new message
    void loop();

    //callback setters
    void onConnect( void (*ncc)(uint16_t fd) );
    void onInput(void (*rc)(uint16_t fd, char *buffer));
    void onDisconnect(void (*dc)(uint16_t fd));

    uint16_t sendMessage(uint16_t source_fd, const char *messageBuffer);
    uint16_t sendMessage(uint16_t source_fd, char *messageBuffer);
    uint16_t sendMessageStr( std::string messageBuffer);
    std::vector<std::string> getHistory();

private:
    
    std::vector<std::string> message_history;

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
    struct sockaddr_in servaddr;

    //input buffer
    char input_buffer[INPUT_BUFFER_SIZE];

    void (*newConnectionCallback) (uint16_t fd);
    void (*receiveCallback) (uint16_t fd, char *buffer);
    void (*disconnectCallback) (uint16_t fd);


    //function prototypes

    // initializes socket address
    void setup(int port);

    //set option on socket to reuse-address
    void initializeSocket();

    // binds associates socket with  local addr
    void bindSocket();

    // make socket as ready to accept connections with backlog size of 3
    void startListen();

    // Adds the new socket to masterfds and increment maxfd if needed
    void handleNewConnection();

    // receives input from socket if not handles error and disconnect and remove from masterfds
    void recvInputFromExisting(int fd);
    std::string recvInputFromExistingStr(int fd);

    void handShake(int fd);
};


#endif //GAME_SERVER_SERVER_H
