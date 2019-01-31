from __future__ import print_function

import numpy as np

from bokeh.util.browser import view
from bokeh.document import Document
from bokeh.embed import file_html
from bokeh.resources import INLINE

from bokeh.models import CustomJS, WidgetBox
from bokeh.models.widgets import (
    Button, Toggle, Dropdown, CheckboxGroup, RadioGroup, CheckboxButtonGroup, RadioButtonGroup,Slider, Div
)

#from bokeh.models import CustomJS, Slider, Div, Toggle

from bokeh.plotting import figure, output_file, show, ColumnDataSource, reset_output
from bokeh.plotting import output_notebook,output_file
from bokeh.transform import dodge, factor_cmap
from bokeh.layouts import column, row, widgetbox

def a_little_dashboard():
    x = np.linspace(0, 10, 500)
    y = np.sin(x)
    y1 = np.sin(2*x)
    y2 = np.sin(4*x)
    source = ColumnDataSource(data=dict(x=x, y=y, y1=y1, y2=y2))

    plot = figure(y_range=(-10, 10), plot_width=400, plot_height=400)

    plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)
    plot.line('x', 'y1', source=source, line_width=3, line_alpha=0.6, color="red")
    plot.line('x', 'y2', source=source, line_width=3, line_alpha=0.6, color = "pink")
    callback = CustomJS(args=dict(source=source), code="""
        var data = source.data;
        var A = amp.value;
        var k = freq.value;
        var phi = phase.value;
        var B = offset.value;
        var x = data['x']
        var y = data['y']
        if (toggle.value == "on"){
            A =10000;
        }
        var f = cb_obj.value
        if (toggle.active){
            div.text = "poo";
        } else{
            div.text = "foo"
        }

        for (var i = 0; i < x.length; i++) {
            y[i] = B + A*Math.sin(k*x[i]+phi);
        }
        source.change.emit();
    """)

    amp_slider = Slider(start=0.1, end=10, value=1, step=.1,
                        title="Amplitude", callback=callback)
    callback.args["amp"] = amp_slider

    freq_slider = Slider(start=0.1, end=10, value=1, step=.1,
                         title="Frequency", callback=callback)
    callback.args["freq"] = freq_slider

    phase_slider = Slider(start=0, end=6.4, value=0, step=.1,
                          title="Phase", callback=callback)
    callback.args["phase"] = phase_slider

    offset_slider = Slider(start=-5, end=5, value=0, step=.1,
                           title="Offset", callback=callback)
    callback.args["offset"] = offset_slider

    div = Div(text="""Your <a href="https://en.wikipedia.org/wiki/HTML">HTML</a>-supported text is initialized with the <b>text</b> argument.  The
    remaining div arguments are <b>width</b> and <b>height</b>. For this example, those values
    are <i>200</i> and <i>100</i> respectively.<br><br><p>yay</p>""",
    width=200, height=100)
    callback.args["div"]=div
    toggle = Toggle(label="Foo", button_type="success")
    #toggle.js_on_change('value', callback)
    callback.args["toggle"] = toggle
    layout = row(plot,widgetbox([amp_slider, freq_slider, phase_slider, offset_slider]),widgetbox([toggle, div]))
    return layout


def flip_flop_buttons():
    x = [x*0.05 for x in range(0, 200)]
    y = x
    x1 = np.linspace(0, 10, 500)
    y1 = np.sin(x1)
    x2 = np.linspace(0, 10, 500)
    y2 = np.sin(4*x2)

    plot = figure(plot_width=400, plot_height=400, title="xxx")
    source = ColumnDataSource(data=dict(x=x, y=y))
    source2 = ColumnDataSource(data=dict(x1=x1, y1=y1, 
                                        x2=x2, y2=y2))

    plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

    def callback(source=source,source2 = source2,  window=None):
        data = source.data
        data2 = source2.data;
        data['x'] = data2['x' + cb_obj.name];
        data['y'] = data2['y' + cb_obj.name];
        source.change.emit()

    #toggle1 = Button(label="Load data file 1", callback=callback, name="1")
    #toggle2 = Button(label="Load data file 2", callback=callback, name="2")

    toggle1 = Button(label="Load data file 1", callback=CustomJS.from_py_func(callback), name="1")
    toggle2 = Button(label="Load data file 2", callback=CustomJS.from_py_func(callback), name="2")
    return plot, toggle1, toggle2



def periodic_table():
    from bokeh.sampledata.periodic_table import elements
    periods = ["I", "II", "III", "IV", "V", "VI", "VII"]
    groups = [str(x) for x in range(1, 19)]

    df = elements.copy()
    df["atomic mass"] = df["atomic mass"].astype(str)
    df["group"] = df["group"].astype(str)
    df["period"] = [periods[x-1] for x in df.period]
    df = df[df.group != "-"]
    df = df[df.symbol != "Lr"]
    df = df[df.symbol != "Lu"]

    cmap = {
        "alkali metal"         : "#a6cee3",
        "alkaline earth metal" : "#1f78b4",
        "metal"                : "#d93b43",
        "halogen"              : "#999d9a",
        "metalloid"            : "#e08d49",
        "noble gas"            : "#eaeaea",
        "nonmetal"             : "#f1d4Af",
        "transition metal"     : "#599d7A",
    }

    TOOLTIPS = [
        ("Name", "@name"),
        ("Atomic number", "@{atomic number}"),
        ("Atomic mass", "@{atomic mass}"),
        ("Type", "@metal"),
        ("CPK color", "$color[hex, swatch]:CPK"),
        ("Electronic configuration", "@{electronic configuration}"),
    ]

    p = figure(title="Periodic Table (omitting LA and AC Series)", plot_width=1000, plot_height=450,
               x_range=groups, y_range=list(reversed(periods)),
               tools="hover", toolbar_location=None, tooltips=TOOLTIPS)

    r = p.rect("group", "period", 0.95, 0.95, source=df, fill_alpha=0.6, legend="metal",
               color=factor_cmap('metal', palette=list(cmap.values()), factors=list(cmap.keys())))

    text_props = {"source": df, "text_align": "left", "text_baseline": "middle"}

    x = dodge("group", -0.4, range=p.x_range)

    p.text(x=x, y="period", text="symbol", text_font_style="bold", **text_props)

    p.text(x=x, y=dodge("period", 0.3, range=p.y_range), text="atomic number",
           text_font_size="8pt", **text_props)

    p.text(x=x, y=dodge("period", -0.35, range=p.y_range), text="name",
           text_font_size="5pt", **text_props)

    p.text(x=x, y=dodge("period", -0.2, range=p.y_range), text="atomic mass",
           text_font_size="5pt", **text_props)

    p.text(x=["3", "3"], y=["VI", "VII"], text=["LA", "AC"], text_align="center", text_baseline="middle")

    p.outline_line_color = None
    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_standoff = 0
    p.legend.orientation = "horizontal"
    p.legend.location ="top_center"
    p.hover.renderers = [r] # only hover element boxes
    return p

    
    
    
    






def buttons():
    button = Button(label="Button (enabled) - has click event", button_type="primary")
    button.js_on_click(CustomJS(code="console.log('button: click', this.toString())"))

    button_disabled = Button(label="Button (disabled) - no click event", button_type="primary", disabled=True)
    button_disabled.js_on_click(CustomJS(code="console.log('button_disabled: click', this.toString())"))

    toggle_inactive = Toggle(label="Toggle button (initially inactive)", button_type="success")
    toggle_inactive.js_on_click(CustomJS(code="console.log('toggle_inactive: ' + this.active, this.toString())"))

    toggle_active = Toggle(label="Toggle button (initially active)", button_type="success", active=True)
    toggle_active.js_on_click(CustomJS(code="console.log('toggle_active: ' + this.active, this.toString())"))

    menu = [("Item 1", "item_1_value"), ("Item 2", "item_2_value"), None, ("Item 3", "item_3_value")]

    dropdown = Dropdown(label="Dropdown button", button_type="warning", menu=menu)
    dropdown.js_on_click(CustomJS(code="console.log('dropdown: ' + this.value, this.toString())"))

    dropdown_disabled = Dropdown(label="Dropdown button (disabled)", button_type="warning", disabled=True, menu=menu)
    dropdown_disabled.js_on_click(CustomJS(code="console.log('dropdown_disabled: ' + this.value, this.toString())"))

    #dropdown_split = Dropdown(label="Split button", button_type="danger", menu=menu, default_value="default")
    #dropdown_split.js_on_click(CustomJS(code="console.log('dropdown_split: ' + this.value, this.toString())"))

    checkbox_group = CheckboxGroup(labels=["Option 1", "Option 2", "Option 3"], active=[0, 1])
    checkbox_group.js_on_click(CustomJS(code="console.log('checkbox_group: ' + this.active, this.toString())"))

    radio_group = RadioGroup(labels=["Option 1", "Option 2", "Option 3"], active=0)
    radio_group.js_on_click(CustomJS(code="console.log('radio_group: ' + this.active, this.toString())"))

    checkbox_button_group = CheckboxButtonGroup(labels=["Option 1", "Option 2", "Option 3"], active=[0, 1])
    checkbox_button_group.js_on_click(CustomJS(code="console.log('checkbox_button_group: ' + this.active, this.toString())"))

    radio_button_group = RadioButtonGroup(labels=["Option 1", "Option 2", "Option 3"], active=0)
    radio_button_group.js_on_click(CustomJS(code="console.log('radio_button_group: ' + this.active, this.toString())"))

    widget_box = WidgetBox(children=[
        button, button_disabled,
        toggle_inactive, toggle_active,
        dropdown, dropdown_disabled, #dropdown_split,
        checkbox_group, radio_group,
        checkbox_button_group, radio_button_group,
    ])
    return widget_box



if __name__ == "__main__":
    doc = Document()
    doc.add_root(buttons())
    doc.validate()
    filename = "buttons.html"
    with open(filename, "w") as f:
        f.write(file_html(doc, INLINE, "Button widgets"))
    print("Wrote %s" % filename)
#view(filename)