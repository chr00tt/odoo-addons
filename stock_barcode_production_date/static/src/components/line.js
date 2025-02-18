/** @odoo-module **/

import LineComponent from '@stock_barcode/components/line';
import { patch } from 'web.utils';

patch(LineComponent.prototype, 'stock_barcode_production_date', {
    get productionDate() {
        const dateTimeStrUTC = (this.line.lot_id && this.line.lot_id.production_date) || this.line.production_date;
        if (!dateTimeStrUTC) {
            return '';
        }
        return moment.utc(dateTimeStrUTC).toDate().toLocaleDateString();
    },
});
