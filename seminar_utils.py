
def stats_table_observed_yield():
    th_props = [
      ('font-size', '11pt'),
      ('text-align', 'center'),
      ('font-weight', 'bold'),
      ('color', 'black'),
      ('background-color', 'lightblue')
      ]
    td_props = [
      ('text-align', 'center'),
      ('padding', "0.1em 0.1em"),
         ('font-size', '3pt')
      ]
    return [dict(selector="table",
                props= [("max-height","220px"),('max-width', '120px'), ('font-size','10pt')]),
            dict(selector="th",
                 props=th_props),
            dict(selector="td",
                 props= td_props),
            dict(selector ='td:hover',
                props = [('color', 'red'),("font-size", "20pt")] ),
            dict(selector ='tr:hover > td',
                props = [('background-color', 'yellow'), ("font-size", "11pt")] ),
            dict(
            props=[
                ('border-collapse', 'separate'), 
                ('border-spacing',  '0px 0px')
                    ])
           ]




def magnify():
    return [dict(selector="th",
                 props=[("font-size", "4pt")]),
            dict(selector="td",
                 props=[('padding', "0em 10em")]),
            dict(selector="th:hover",
                 props=[("font-size", "12pt")]),
            dict(selector="tr:hover td:hover",
                 props=[('max-width', '200px'),
                        ('font-size', '12pt')])]