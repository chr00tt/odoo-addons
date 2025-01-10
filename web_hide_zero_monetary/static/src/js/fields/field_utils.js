odoo.define('web_hide_zero_monetary.field_utils', function (require) {
"use strict";

var field_utils = require('web.field_utils');

var originalFormatMonetary = field_utils.format.monetary

function formatMonetary(value, field, options) {
    if (value) {
        return originalFormatMonetary(value, field, options)
    }
    
    return "";
}

field_utils.format.monetary = formatMonetary

});
