/** @odoo-module **/

import LineComponent from '@stock_barcode/components/line';
import { patch } from "@web/core/utils/patch";

patch(LineComponent.prototype, {
    get productionDate() {
        const dateTimeStrUTC = (this.line.lot_id && this.line.lot_id.production_date) || this.line.production_date;
        if (!dateTimeStrUTC) {
            return '';
        }
        return moment.utc(dateTimeStrUTC).toDate().toLocaleDateString();
    },
});
