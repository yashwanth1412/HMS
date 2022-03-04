window.addEventListener("load", function () {
    (function ($) {
        $('form').submit(function () {
            var c = confirm("Are you sure?");
            return c;
        });
    
    
    })(django.jQuery)});