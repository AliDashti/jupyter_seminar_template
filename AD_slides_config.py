c = get_config()

#c.NbConvertApp.notebooks = ["notebook1.ipynb", "notebook2.ipynb"]

c.TagRemovePreprocessor.remove_input_tags.add("to_remove")

exporter_settings = {
    'exclude_input_prompt' : True,
    'exclude_output_prompt' : True,
}
c.TemplateExporter.update(exporter_settings)


app_settings = {
    "export_format": "slides"
}
c.NbConvertApp.update(app_settings)

c.ServePostProcessor.reveal_prefix = "reveal.js" 

c.Exporter.template_file = './reveal_child_template'


