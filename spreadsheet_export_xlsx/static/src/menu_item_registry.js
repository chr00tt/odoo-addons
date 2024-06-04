/** @odoo-module */

import { _t, _lt } from "web.core";

import spreadsheet from "@spreadsheet/o_spreadsheet/o_spreadsheet_extended";

const { topbarMenuRegistry } = spreadsheet.registries;

topbarMenuRegistry.addChild("download", ["data"], {
    name: "下载 XLSX",
    sequence: 0,
    // action: (env) => {
    //     env.services.action.doAction({
    //         type: "ir.actions.client",
    //         tag: "action_download_spreadsheet",
    //         params: {
    //             orm: this.orm,
    //             name: this.props.name,
    //             data: this.model.exportData(),
    //             stateUpdateMessages: [],
    //         },
    //     })
    // },
    action: (env) => env.download(),
});