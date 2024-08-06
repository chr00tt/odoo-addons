/** @odoo-module */

import { _t, _lt } from "web.core";

import spreadsheet from "@spreadsheet/o_spreadsheet/o_spreadsheet_extended";

const { topbarMenuRegistry } = spreadsheet.registries;

topbarMenuRegistry.addChild("download", ["data"], {
    name: "下载 XLSX",
    sequence: 0,
    action: (env) => env.download(),
});