CKEDITOR.editorConfig = function (config) {
    {% for key, option in config.items %}
        config.{{ key }} = {{option | safe}};
    {% endfor %}
}