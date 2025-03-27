/** @odoo-module **/

import  * as formatters  from "@web/views/fields/formatters";
import { registry } from "@web/core/registry";

import { formatCurrency } from "@web/core/currency";

export function formatMonetary(value, options = {}) {
    if (!value) {
        return "";
    }

    let currencyId = options.currencyId;
    if (!currencyId && options.data) {
        const currencyField =
            options.currencyField ||
            (options.field && options.field.currency_field) ||
            "currency_id";
        const dataValue = options.data[currencyField];
        currencyId = Array.isArray(dataValue) ? dataValue[0] : dataValue;
    }
    return formatCurrency(value, currencyId, options)
}

registry
    .category("formatters")
    .remove("monetary")
registry
    .category("formatters")
    .add("monetary", formatMonetary)
