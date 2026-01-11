#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "reslik/reslik_unit.hpp"

namespace py = pybind11;

PYBIND11_MODULE(_core, m) {
    m.doc() = "ResLik C++ Core";

    py::class_<reslik::ResLikUnit>(m, "ResLikUnit")
        .def(py::init<int, int>())
        .def("forward", &reslik::ResLikUnit::forward)
        .def("set_reference_stats", &reslik::ResLikUnit::set_reference_stats)
        .def("set_lambda", &reslik::ResLikUnit::set_lambda)
        .def("update_stats", &reslik::ResLikUnit::update_stats);
}
