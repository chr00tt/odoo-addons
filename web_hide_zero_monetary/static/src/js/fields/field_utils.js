odoo.define('web_hide_zero_monetary.field_utils', function (require) {
"use strict";

var field_utils = require('web.field_utils');
var session = require('web.session');

const NBSP = "\u00a0";

function formatMonetary(value, field, options) {
    if (!value) {
        return "";
    }
    options = options || {};

    var currency = options.currency;
    if (!currency) {
        var currency_id = options.currency_id;
        if (!currency_id && options.data) {
            var currency_field = options.currency_field || field.currency_field || 'currency_id';
            currency_id = options.data[currency_field] && options.data[currency_field].res_id;
        }
        currency = session.get_currency(currency_id);
    }

    var digits = (currency && currency.digits) || options.digits;
    if (options.field_digits === true) {
        digits = field.digits || digits;
    }
    var formatted_value = field_utils.format.float(value, field,
        _.extend({}, options , {digits: digits})
    );

    if (!currency || options.noSymbol) {
        return formatted_value;
    }
    if (currency.position === "after") {
        return formatted_value += NBSP + currency.symbol;
    } else {
        return currency.symbol + NBSP + formatted_value;
    }
}

field_utils.format.monetary = formatMonetary

});