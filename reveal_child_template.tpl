{%- extends 'slides_reveal.tpl' -%}

{% block header %}
<!DOCTYPE html>
<html>
<head>

<meta charset="utf-8" />
<meta http-equiv="X-UA-Compatible" content="chrome=1" />

<meta name="apple-mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />

<title>{{resources['metadata']['name']}} slides</title>

<!-- the following two lines are very important! you could delte lines 8-14 but not 17 and 18 -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.1.10/require.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>

<!-- General and theme style sheets -->
<link rel="stylesheet" href="{{resources.reveal.url_prefix}}/css/reveal.css">
<link rel="stylesheet" href="{{resources.reveal.url_prefix}}/css/theme/sky.css">
<link rel="stylesheet" href="./css/style.css" id="my_theme">

<!-- Code syntax highlighting -->
<link rel="stylesheet" href="{{resources.reveal.url_prefix}}/lib/css/zenburn.css">

<!-- If the query includes 'print-pdf', include the PDF print sheet -->
<script>
if( window.location.search.match( /print-pdf/gi ) ) {
        var link = document.createElement( 'link' );
        link.rel = 'stylesheet';
        link.type = 'text/css';
        link.href = '{{resources.reveal.url_prefix}}/css/print/pdf.css';
        document.getElementsByTagName( 'head' )[0].appendChild( link );
}

</script>

<!--[if lt IE 9]>
<script src="{{resources.reveal.url_prefix}}/lib/js/html5shiv.js"></script>
<![endif]-->

<!-- Loading the mathjax macro -->
{{ mathjax() }}

<!-- Get Font-awesome from cdn -->
<link rel="stylesheet" href="//netdna.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.css">


<!-- these few line jinja lines are crazy. will add a million styling lines to final html -->
<!-- you can remove them. the html output would be smaller but the look is a bit different -->
<!-- not sure why we are having so many inline styles -->
{% for css in resources.inlining.css -%}
    <style type="text/css">
    {{ css }}
    </style>
{% endfor %}

<!-- Add favicon -->
<link rel="shortcut icon" type="image/ico" href="favicon.ico" />

<!-- Additional imports for plugins -->
<link rel="stylesheet" href="./plugin/title-footer/title-footer.css">

</head>

{% endblock header%}

{% block body %}

{{ super() }}

<script>
require(
    [
      "{{resources.reveal.url_prefix}}/lib/js/head.min.js",
      "{{resources.reveal.url_prefix}}/js/reveal.js"
    ],
    function(head, Reveal){
    
        Reveal.initialize({
            dependencies:
                [
                { src: './plugin/highlight/highlight.js', async: true, condition: function() { return !!document.querySelector( 'pre code' ); }, callback: function() { hljs.initHighlightingOnLoad(); } },
                    { src: './plugin/title-footer/title-footer.js', async: true, callback: function() { title_footer.initialize("© 2018 Ali Dashti.  All rights reserved.", 'rgba(173,217,228,1.0)' ); } }
                ]
        });
    
        Reveal.configure({width: "100%", height:"100%",margin: 0, minScale:1, maxScale:1});
        Reveal.configure({slideNumber: true})
    }
    
);
</script>




{% endblock body %}
