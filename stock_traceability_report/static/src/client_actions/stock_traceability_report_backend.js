/** @odoo-module **/

import { TraceabilityReport } from "@stock/client_actions/stock_traceability_report_backend";
import { patch } from "@web/core/utils/patch";

function processLine(line) {
    return { ...line, lines: [], isFolded: true };
}

patch(TraceabilityReport.prototype, {

    async onWillStart() {
        if (!this.state.lines.length) {
            const mainLines = await this.orm.call("stock.traceability.report", "get_main_lines", [
                this.context,
            ]);
            this.state.lines = mainLines.lines.map(processLine);
        }
    }

});
