/** @odoo-module */

import {SpreadsheetRenderer} from "@spreadsheet_oca/spreadsheet/bundle/spreadsheet_renderer.esm";
import { patch } from "@web/core/utils/patch";

import { useService } from "@web/core/utils/hooks";

const {useSubEnv, useState, onWillStart} = owl;

patch(SpreadsheetRenderer.prototype, "spreadsheet_export_xlsx.SpreadsheetRenderer", {
    setup() {
        this._super();

        this.ui = useService("ui");
        this.action = useService("action");

        useSubEnv({
            download: this._download.bind(this),
        });
    },

    /**
     * Downloads the spreadsheet in xlsx format
     */
    async _download() {
        this.ui.block();
        try {
            await this.action.doAction({
                type: "ir.actions.client",
                tag: "action_download_spreadsheet",
                params: {
                    orm: this.orm,
                    name: this.props.name,
                    data: this.spreadsheet_model.exportData(),
                    stateUpdateMessages: [],
                },
            });
        } finally {
            this.ui.unblock();
        }
    }
});
