/** @odoo-module **/

import LineComponent from '@stock_barcode/components/line';
import { patch } from "@web/core/utils/patch";
import { parseDateTime } from "@web/core/l10n/dates";

patch(LineComponent.prototype, {
    get productionDate() {
        const dateTimeStrUTC = (this.line.lot_id && this.line.lot_id.production_date) || this.line.production_date;
        if (!dateTimeStrUTC) {
            return '';
        }
        const dateTimeLocal = parseDateTime(dateTimeStrUTC).toJSDate();
        return dateTimeLocal.toLocaleDateString();
    },
});
