#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "Server.h"


namespace py = pybind11;

PYBIND11_MODULE(gameServer, m) {
    py::class_<Server>(m, "Server")
        .def(py::init())
        .def(py::init<int>())
        .def("loop", &Server::loop)
        .def("getHistory",&Server::getHistory)
        .def("sendMessageStr", &Server::sendMessageStr)
        .def("init", &Server::init);


}

// PYBIND11_MODULE(example, m) {
//    py::class_<Client>(m, "Client")
//         .def(py::init())
//         .def(py::init<int>())
//         .def("loop", &Client::loop)
//         .def("init", &Client::init)
//         .def("sendMessage", &Client::sendMessage); 
// }


// create module by running  
// g++ -O3 -Wall -shared -std=c++11 -fPIC `python3 -m pybind11 --includes` python_binding.cpp Server.cpp  -o gameServer`python3-config --extension-suffix`
