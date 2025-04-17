# -*- coding: utf-8 -*-

from odoo import _, api, models

from odoo.addons.queue_job.exception import FailedJobError

class BaseImportImport(models.TransientModel):
    _inherit = "base_import.import"

    def _import_one_chunk(self, model_name, attachment, options):
        model = self.env[self.res_model].with_context(options.get('context', {}))

        name_create_enabled_fields = options.pop('name_create_enabled_fields', {})
        import_limit = options.pop('limit', None)
        model = model.with_context(
            import_file=True,
            name_create_enabled_fields=name_create_enabled_fields,
            import_set_empty_fields=options.get('import_set_empty_fields', []),
            import_skip_records=options.get('import_skip_records', []),
            _import_limit=import_limit)
        fields, data = self._read_csv_attachment(attachment, options)
        result = model.load(fields, data)
        error_message = [
            message["message"]
            for message in result["messages"]
            if message["type"] == "error"
        ]
        if error_message:
            raise FailedJobError("\n".join(error_message))
        return result
