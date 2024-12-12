/** @odoo-module **/

import { formatFloat } from "@web/views/fields/formatters";

import { registry } from "@web/core/registry";
import { nbsp } from "@web/core/utils/strings";
import { session } from "@web/session";
import { humanNumber } from "@web/core/utils/numbers";

export function formatMonetary(value, options = {}) {
    // Monetary fields want to display nothing when the value is unset.
    // You wouldn't want a value of 0 euro if nothing has been provided.
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
    const currency = session.currencies[currencyId];
    const digits = options.digits || (currency && currency.digits);

    let formattedValue;
    if (options.humanReadable) {
        formattedValue = humanNumber(value, { decimals: digits ? digits[1] : 2 });
    } else {
        formattedValue = formatFloat(value, { digits });
    }

    if (!currency || options.noSymbol) {
        return formattedValue;
    }
    const formatted = [currency.symbol, formattedValue];
    if (currency.position === "after") {
        formatted.reverse();
    }
    return formatted.join(nbsp);
}

registry
    .category("formatters")
    .remove("monetary")
registry
    .category("formatters")
    .add("monetary", formatMonetary)
