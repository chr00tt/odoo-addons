odoo.define('web_hide_zero_monetary.ListView', function (require) {
"use strict";

var core = require('web.core');
var formats = require('web.formats');
var pyeval = require('web.pyeval');
var session = require('web.session');

var ListView = require('web.ListView');

var list_widget_registry = core.list_widget_registry;
var Column = ListView.Column

var ColumnMonetary = Column.extend({

    _format: function (row_data, options) {
        var options = pyeval.py_eval(this.options || '{}');
        //name of currency field is defined either by field attribute, in view options or we assume it is named currency_id
        var currency_field = (_.isEmpty(options) === false && options.currency_field) || this.currency_field || 'currency_id';
        var currency_id = row_data[currency_field] && row_data[currency_field].value[0];
        var currency = session.get_currency(currency_id);
        var digits_precision = this.digits || (currency && currency.digits);
        // 不显示 0.00
        if (!row_data[this.id].value) {
            return ''
        }
        var value = formats.format_value(row_data[this.id].value || 0, {type: this.type, digits: digits_precision}, options.value_if_empty);
        if (currency) {
            if (currency.position === "after") {
                value += '&nbsp;' + currency.symbol;
            } else {
                value = currency.symbol + '&nbsp;' + value;
            }
        }
        return value;
    },
});

list_widget_registry
    .add('field.monetary', ColumnMonetary);

});