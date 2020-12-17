#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "Server.h"
#include "Server_client.h"


namespace py = pybind11;

PYBIND11_MODULE(gameServer, m) {
    py::class_<Server>(m, "Server")
        .def(py::init())
        .def(py::init<int>())
        .def("loop", &Server::loop)
        .def("sendMessageStr", &Server::sendMessageStr)
        .def("init", &Server::init);

    py::class_<Client>(m, "Client")
        .def(py::init())
        .def(py::init<int>())
        .def("loop", &Client::loop)
        // .def("init", &Client::init)
        .def("sendMessageStr", &Client::sendMessageStr); 
}


// PYBIND11_MODULE(gameServerClient, m) {
//    py::class_<Client>(m, "Client")
//         .def(py::init())
//         .def(py::init<int>())
//         .def("loop", &Client::loop)
//         .def("init", &Client::init)
//         .def("sendMessageStr", &Client::sendMessageStr); 
// }

// create module by running  
// g++ -O3 -Wall -shared -std=c++11 -fPIC `python3 -m pybind11 --includes` python_binding.cpp Server.cpp  -o gameServer`python3-config --extension-suffix`
