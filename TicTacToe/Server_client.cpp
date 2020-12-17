//
// Created by kinchi on 11/11/20.
//

#include "Server_client.h"
#include "TCP_Packet.h"


/*
 * Server.cpp
 *
 * EventServer is a simple C++ TCP socket server implementation,
 * built to simplify socket programming (and to serve as an example to anyone who wants to learn it!)
 * It can interface with the rest of your program using three callback functions.
 * - onConnect, which fires when a new client connects. the client's fd is passed.
 * - onDisconnect, which fires when a client disconnects. passes fd.
 * - onInput, fires when input is received from a client. passes fd and char*
 *
 * define SERVER_DEBUG to spew out some juicy debug data!
 */


Client::Client() {
    setup(DEFAULT_PORT);
}

Client::Client(int port) {
    setup(port);
    connectSocket();
}

Client::~Client() {
    #ifdef SERVER_DEBUG
        std::cout << "[CLIENT] [DESTRUCTOR] Destroying Server...\n";
    #endif
    close(mastersocket_fd);
}

void Client::setup(int port, std::string hostname ) {
    mastersocket_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (mastersocket_fd < 0) {
        perror("Socket creation failed");
    }
#ifdef SERVER_DEBUG
    printf( "[CLIENT] [MISC] file descriptor for socket: '%hu'\n", mastersocket_fd);
#endif
    FD_ZERO(&masterfds);
    FD_ZERO(&tempfds);

    server = gethostbyname(&hostname[0]);

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
    serv_addr.sin_port = htons(port);


    bzero(input_buffer,
          INPUT_BUFFER_SIZE); //zero the input buffer before use to avoid random data appearing in first receives
}

void Client::initializeSocket() {
    // #ifdef SERVER_DEBUG
    //     std::cout << "[CLIENT] initializing socket\n";
    // #endif
    // int opt_value = 1;
    // int ret_test = setsockopt(mastersocket_fd, SOL_SOCKET, SO_REUSEADDR, (char *) &opt_value, sizeof(int));
    // #ifdef SERVER_DEBUG
    //     printf("[CLIENT] setsockopt() ret %d\n", ret_test);
    // #endif
    // if (ret_test < 0) {
    //     perror("[CLIENT] [ERROR] setsockopt() failed");
    //     shutdown();
    // }
}

void Client::connectSocket() {
    #ifdef SERVER_DEBUG
        std::cout << "[CLIENT] connecting...\n";
    #endif
    int connect_ret = connect(mastersocket_fd, (struct sockaddr *)&serv_addr, sizeof(serv_addr));
    #ifdef SERVER_DEBUG
        printf("[CLIENT] connect() ret %d\n", connect_ret);
    #endif
    if (connect_ret < 0) {
        perror("[CLIENT] [ERROR] bind() failed");
    }
    FD_SET(mastersocket_fd, &masterfds); //insert the master socket file-descriptor into the master fd-set
    maxfd = mastersocket_fd; //set the current known maximum file descriptor count
}

void Client::shutdown() {
    int close_ret = close(mastersocket_fd);
#ifdef SERVER_DEBUG
    printf("[CLIENT] [DEBUG] [SHUTDOWN] closing master fd..  ret '%d'.\n",close_ret);
#endif
}


void Client::recvInputFromExisting(int fd) {
    int nbytesrecv = recv(fd, input_buffer, INPUT_BUFFER_SIZE, 0);
    if (nbytesrecv <= 0) {
        //problem
        if (0 == nbytesrecv) {
//            disconnectCallback((uint16_t) fd);
            close(fd); //well then, bye bye.
            FD_CLR(fd, &masterfds);
            return;
        } else {
            perror("[CLIENT] [ERROR] recv() failed");
        }
        close(fd); //close connection to client
        FD_CLR(fd, &masterfds); //clear the client fd from fd set
        return;
    }
    #ifdef SERVER_DEBUG
        printf("[CLIENT] [RECV] Received '%s' from client!\n", input_buffer);
    #endif
    // message_history.push_back(input_buffer);
//    receiveCallback(fd, input_buffer);
    // std::string recieved(input_buffer);
    //memset(&input_buffer, 0, INPUT_BUFFER_SIZE); //zero buffer //bzero
    bzero(&input_buffer, INPUT_BUFFER_SIZE); //clear input buffer
}

std::vector<std::string> Client::getHistory(){
    return std::vector<std::string>();
    // message_history;
}

void Client::loop() {
    tempfds = masterfds; //copy fd_set for select()
    #ifdef SERVER_DEBUG
        printf("[CLIENT] [MISC] max fd = '%hu' \n", maxfd);
        std::cout << "[SERVER] [MISC] calling select()\n";
    #endif
    int sel = select(maxfd + 1, &tempfds, NULL, NULL, NULL); //blocks until activity
    #ifdef SERVER_DEBUG
    printf("[CLIENT] [MISC] select() ret %d, processing...\n", sel);
    #endif
    if (sel < 0) {
        perror("[CLIENT] [ERROR] select() failed");
        shutdown();
    }

    //no problems, we're all set
    //loop the fd_set and check which socket has interactions available
    for (int i = 0; i <= maxfd; i++) {
        if (FD_ISSET(i, &tempfds)) { //if the socket has activity pending
            if (mastersocket_fd == i) {
            } else {
                //exisiting connection has new data
                recvInputFromExisting(i);
            }
        } //loop on to see if there is more
    }
}


uint16_t Client::sendMessage( char *messageBuffer) {
    return send(mastersocket_fd, messageBuffer, strlen(messageBuffer), 0);
}

uint16_t Client::sendMessage( const char *messageBuffer) {
    return send(mastersocket_fd, messageBuffer, strlen(messageBuffer), 0);
}

uint16_t Client::sendMessageStr( std::string messageBuffer) {
    return send(mastersocket_fd, &messageBuffer[0], messageBuffer.length(), 0);
}


void Client::handShake(int fd) {

    struct Packet pktRecieved;
    pktRecieved = pktRecieved.packetify("recieved");
    if (pktRecieved.packet_type == 1) { // Resonding to Syn
        
        actual_buffer_size = actual_buffer_size < pktRecieved.buffer_size ? actual_buffer_size : pktRecieved.buffer_size;
        
        //Send a syn-ack
        struct Packet response(2, sequence_number, pktRecieved.sequence_number + 1);
        response.buffer_size = actual_buffer_size;

        write(fd, &(response.transmitVersion(response)[0]), response.transmitVersion(response).length());
    }

    // if (pkt.packet_type == 4)
    // {
    //     if (!true)
    //     {
    //         struct Packet response = cache.back();
    //         char resp[1024];
    //         strcpy(resp, transmitVersion(response).c_str());
    //         write(sockID, resp, strlen(resp));
    //     }
    // }
}