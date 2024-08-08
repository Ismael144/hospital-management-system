document.addEventListener("DOMContentLoaded", function() {
    // Check if CKEditor is available
    if (typeof CKEDITOR !== 'undefined') {
        // Find all textareas with the `ckeditor` class
        var textareas = document.querySelectorAll('textarea.django_ckeditor_5');

        // Iterate over each textarea and replace it with CKEditor instance
        textareas.forEach(function(textarea) {
            CKEDITOR.replace(textarea.id, {
                // Configuration options
                filebrowserUploadUrl: '/ckeditor/upload/',
                filebrowserBrowseUrl: '/ckeditor/browse/',
                fileTools_requestHeaders: {
                    'X-CSRF-TOKEN': document.querySelector('input[name=csrfmiddlewaretoken]').value
                },
                extraPlugins: 'image2,uploadimage',
                removePlugins: 'image',  // Remove the default image plugin to use image2
                height: 400,
                toolbar: [
                    { name: 'clipboard', items: ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo'] },
                    { name: 'editing', items: ['Find', 'Replace', '-', 'SelectAll'] },
                    { name: 'basicstyles', items: ['Bold', 'Italic', 'Underline', 'Strike', '-', 'RemoveFormat'] },
                    { name: 'paragraph', items: ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'] },
                    { name: 'links', items: ['Link', 'Unlink'] },
                    { name: 'insert', items: ['Image', 'Table', 'HorizontalRule', 'SpecialChar'] },
                    { name: 'styles', items: ['Styles', 'Format', 'Font', 'FontSize'] },
                    { name: 'colors', items: ['TextColor', 'BGColor'] },
                    { name: 'tools', items: ['Maximize', 'ShowBlocks'] }
                ],
                // Additional configuration for image uploads
                imageUploadUrl: '/ckeditor/upload/',
                fileTools_requestHeaders: {
                    'X-CSRF-TOKEN': document.querySelector('input[name=csrfmiddlewaretoken]').value
                }
            });
        });
    } else {
        console.error('CKEditor not found');
    }
});
