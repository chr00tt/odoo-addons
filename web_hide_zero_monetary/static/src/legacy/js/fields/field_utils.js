odoo.define('web_hide_zero_monetary.field_utils', function (require) {
"use strict";

var field_utils = require('web.field_utils');
var session = require('web.session');
var utils = require('web.utils');

const NBSP = "\u00a0";

function formatMonetary(value, field, options) {
    if (!value) {
        return "";
    }
    options = Object.assign({ forceString: false }, options);

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
    const val = currency.position === 'after'
        ? [formatted_value, currency.symbol]
        : [currency.symbol, formatted_value];
    if (options.forceString) {
        return val.join(' ');
    }
    return utils.Markup(val.map((v) => _.escape(v)).join(NBSP));
}

field_utils.format.monetary = formatMonetary

});
