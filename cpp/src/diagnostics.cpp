#include "reslik/diagnostics.hpp"

namespace reslik {
namespace diagnostics {

DiagnosticReport get_last_report() {
    return DiagnosticReport{1.0f, 0.0f, {}};
}

} // namespace diagnostics
} // namespace reslik
