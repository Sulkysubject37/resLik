#include <iostream>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "reslik/reslik_unit.hpp"
#include "reslik/diagnostics.hpp"

namespace py = pybind11;

PYBIND11_MODULE(_core, m) {
    m.doc() = "ResLik C++ Core";

    // Bind DiagnosticReport struct
    py::class_<reslik::diagnostics::DiagnosticReport>(m, "DiagnosticReport")
        .def_readonly("mean_gate_value", &reslik::diagnostics::DiagnosticReport::mean_gate_value)
        .def_readonly("max_discrepancy", &reslik::diagnostics::DiagnosticReport::max_discrepancy)
        .def_readonly("collapsed_features", &reslik::diagnostics::DiagnosticReport::collapsed_features);

    py::class_<reslik::ResLikUnit>(m, "ResLikUnit")
        .def(py::init([](int input_dim, int latent_dim) {
            std::cout << "DEBUG: ResLikUnit ctor input_dim=" << input_dim << " latent_dim=" << latent_dim << std::endl;
            return new reslik::ResLikUnit(input_dim, latent_dim);
        }), py::arg("input_dim"), py::arg("latent_dim"))
        .def("forward", [](reslik::ResLikUnit& self, const std::vector<float>& input) {
            // std::cout << "DEBUG: Binding forward input size=" << input.size() << std::endl;
            auto out = self.forward(input);
            if (out.empty()) {
                std::cerr << "DEBUG: Binding forward returned EMPTY vector!" << std::endl;
            } else {
                // std::cout << "DEBUG: Binding forward output size=" << out.size() << std::endl;
            }
            return out;
        }, py::arg("input"), "Apply ResLik gating to a single input vector.")
        .def("set_reference_stats", &reslik::ResLikUnit::set_reference_stats, 
             py::arg("mu_ref"), py::arg("sigma_ref"), 
             "Set reference statistics for discrepancy calculation.")
        .def("set_lambda", &reslik::ResLikUnit::set_lambda, py::arg("lambda"), 
             "Set the gating sensitivity parameter.")
        .def("set_tau", &reslik::ResLikUnit::set_tau, py::arg("tau"), 
             "Set the discrepancy dead-zone threshold.")
        .def("get_diagnostics", &reslik::ResLikUnit::get_diagnostics, 
             "Get the diagnostics from the last forward pass.")
        .def("update_stats", &reslik::ResLikUnit::update_stats, 
             "Update internal running statistics (not yet implemented).");
}