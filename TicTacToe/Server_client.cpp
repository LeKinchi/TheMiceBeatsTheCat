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
}

Client::~Client() {
    #ifdef SERVER_DEBUG
        std::cout << "[SERVER] [DESTRUCTOR] Destroying Server...\n";
    #endif
    close(mastersocket_fd);
}

void Client::setup(int port, std::string hostname ) {
    mastersocket_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (mastersocket_fd < 0) {
        perror("Socket creation failed");
    }
#ifdef SERVER_DEBUG
    printf("[SERVER] [MISC] max fd = '%hu' \n", maxfd);
    printf( "[SERVER] [MISC] file descriptor for new socket: '%hu'\n", mastersocket_fd);
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
    #ifdef SERVER_DEBUG
        std::cout << "[SERVER] initializing socket\n";
    #endif
    int opt_value = 1;
    int ret_test = setsockopt(mastersocket_fd, SOL_SOCKET, SO_REUSEADDR, (char *) &opt_value, sizeof(int));
    #ifdef SERVER_DEBUG
        printf("[SERVER] setsockopt() ret %d\n", ret_test);
    #endif
    if (ret_test < 0) {
        perror("[SERVER] [ERROR] setsockopt() failed");
        shutdown();
    }
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
    printf("[SERVER] [DEBUG] [SHUTDOWN] closing master fd..  ret '%d'.\n",close_ret);
#endif
}

void Client::handleNewConnection() {
    #ifdef SERVER_DEBUG
        std::cout << "[SERVER] [CONNECTION] handling new connection\n";
    #endif

    socklen_t addrlen = sizeof(client_addr);
    tempsocket_fd = accept(mastersocket_fd, (struct sockaddr *) &client_addr, &addrlen);

    if (tempsocket_fd < 0) {
        perror("[SERVER] [ERROR] accept() failed");
    } else {

        FD_SET(tempsocket_fd, &masterfds);
//        std::cout <<  masterfds << std::endl;
        //increment the maximum known file descriptor (select() needs it)
        if (tempsocket_fd > maxfd) {
            maxfd = tempsocket_fd;
            #ifdef SERVER_DEBUG
                        std::cout << "[SERVER] incrementing maxfd to " << maxfd << std::endl;
            #endif
        }
        #ifdef SERVER_DEBUG
                printf("[SERVER] [CONNECTION] New connection on socket fd '%d'.\n",tempsocket_fd);
        #endif
    }
    handShake(tempsocket_fd);
    client_fd.insert(tempsocket_fd);
//    newConnectionCallback(tempsocket_fd); //call the callback
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
            perror("[SERVER] [ERROR] recv() failed");
        }
        close(fd); //close connection to client
        FD_CLR(fd, &masterfds); //clear the client fd from fd set
        return;
    }
    #ifdef SERVER_DEBUG
        printf("[SERVER] [RECV] Received '%s' from client!\n", input_buffer);
    #endif
    message_history.push_back(input_buffer);
//    receiveCallback(fd, input_buffer);
    // std::string recieved(input_buffer);
    //memset(&input_buffer, 0, INPUT_BUFFER_SIZE); //zero buffer //bzero
    bzero(&input_buffer, INPUT_BUFFER_SIZE); //clear input buffer
}

std::vector<std::string> Client::getHistory(){
    return message_history;
}


std::string Client::recvInputFromExistingStr(int fd) {
    int nbytesrecv = recv(fd, input_buffer, INPUT_BUFFER_SIZE, 0);
    if (nbytesrecv <= 0) {
        //problem
        if (0 == nbytesrecv) {
//            disconnectCallback((uint16_t) fd);
            close(fd); //well then, bye bye.
            FD_CLR(fd, &masterfds);
            return "";
        } else {
            perror("[SERVER] [ERROR] recv() failed");
        }
        close(fd); //close connection to client
        FD_CLR(fd, &masterfds); //clear the client fd from fd set
        return "";
    }
    #ifdef SERVER_DEBUG
        printf("[SERVER] [RECV] Received '%s' from client!\n", input_buffer);
    #endif
//    receiveCallback(fd, input_buffer);
    std::string recieved(input_buffer);
    //memset(&input_buffer, 0, INPUT_BUFFER_SIZE); //zero buffer //bzero
    bzero(&input_buffer, INPUT_BUFFER_SIZE); //clear input buffer
    return recieved;
}

void Client::loop() {
    tempfds = masterfds; //copy fd_set for select()
    #ifdef SERVER_DEBUG
        printf("[SERVER] [MISC] max fd = '%hu' \n", maxfd);
        std::cout << "[SERVER] [MISC] calling select()\n";
    #endif
    int sel = select(maxfd + 1, &tempfds, NULL, NULL, NULL); //blocks until activity
    #ifdef SERVER_DEBUG
    printf("[SERVER] [MISC] select() ret %d, processing...\n", sel);
    #endif
    if (sel < 0) {
        perror("[SERVER] [ERROR] select() failed");
        shutdown();
    }

    //no problems, we're all set

    //loop the fd_set and check which socket has interactions available
    for (int i = 0; i <= maxfd; i++) {
        if (FD_ISSET(i, &tempfds)) { //if the socket has activity pending
            if (mastersocket_fd == i) {
                //new connection on master socket
                handleNewConnection();
            } else {
                //exisiting connection has new data
                recvInputFromExisting(i);
            }
        } //loop on to see if there is more
    }
}

void Client::init() {
    // initializeSocket();
    connectSocket();
    // startListen();
}

void Client::onInput(void (*rc)(uint16_t fd, char *buffer)) {
    receiveCallback = rc;
}

void Client::onConnect( void(*ncc)(uint16_t) ) {
    newConnectionCallback = ncc;
}

void Client::onDisconnect(void(*dc)(uint16_t)) {
    disconnectCallback = dc;
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
    std::string recieved = recvInputFromExistingStr(fd);
    struct Packet pktRecieved = packetify(recieved);
   
    if (pktRecieved.packet_type == 1) { // Resonding to Syn
        
        actual_buffer_size = actual_buffer_size < pktRecieved.buffer_size ? actual_buffer_size : pktRecieved.buffer_size;
        
        //Send a syn-ack
        struct Packet response(2, sequence_number, pktRecieved.sequence_number + 1);
        response.buffer_size = actual_buffer_size;

        char resp[1024];
        write(fd, &transmitVersion(response)[0], transmitVersion(response).length());
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

void Client::SendSyn(){
  if (true)
        { // send a  Syn
            srand((unsigned)time(NULL));
            sequence_number = rand() % 1000;

            struct Packet response(1, sequence_number);
            response.buffer_size = 50;
            char resp[1024];
            strcpy(resp, transmitVersion(response).c_str());
            write(mastersocket_fd, resp, strlen(resp));


            // bzero(buffer, 256);
            // n = read(mastersocket_fd, buffer, 255);
            // if (n == 0)
            //     std::cout << "error reading incoming packet \n";
            // current_packet = packetify(buffer);
            // printf("Request recieved: \n\t Raw: %s \n\t Pro: %s", buffer, display(current_packet).c_str());
        }

}