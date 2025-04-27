/** @odoo-module **/

import BarcodePickingModel from '@stock_barcode/models/barcode_picking_model';
import { patch } from "@web/core/utils/patch";

patch(BarcodePickingModel.prototype, {

    async updateLine(line, args) {
        super.updateLine(...arguments);
        if (args.production_date) {
            line.production_date = args.production_date;
        }
    },

    async _processGs1Data(data) {
        const result = {};
        const { rule, value } = data;
        if (rule.type === 'production_date') {
            // convert to noon to avoid most timezone issues
            value.setHours(12, 0, 0);
            result.productionDate = moment.utc(value).format('YYYY-MM-DD HH:mm:ss');
            result.match = true;
        } else {
            return await super._processGs1Data(...arguments);
        }
        return result;
    },

    _convertDataToFieldsParams(args) {
        const params = super._convertDataToFieldsParams(...arguments);
        if (args.productionDate) {
            params.production_date = args.productionDate;
        }
        return params;
    },

    _getFieldToWrite() {
        const fields = super._getFieldToWrite(...arguments);
        fields.push('production_date');
        return fields;
    },

    _createCommandVals(line) {
        const values = super._createCommandVals(...arguments);
        values.production_date = line.production_date;
        return values;
    },
});
