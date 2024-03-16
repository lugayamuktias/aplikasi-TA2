$(document).ready(function() {
    // Function to display image preview, size, and resolution
    function showImagePreview(input, previewElement) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function(e) {
                var img = new Image();
                img.src = e.target.result;

                img.onload = function() {
                    var fileSize = input.files[0].size;
                    var resolution = this.width + "x" + this.height;
                    var preview = '<img src="' + e.target.result + '" style="max-width:300px; max-height:300px;"><br>';
                    preview += 'Size: ' + fileSize + ' bytes<br>';
                    preview += 'Resolution: ' + resolution + '<br>';
                    $(previewElement).html(preview);
                };
            };

            reader.readAsDataURL(input.files[0]);
        }
    }

    // Show preview for cover image
    $('#cover_image').change(function() {
        showImagePreview(this, '#cover_image_preview');
    });

    // Show preview for secret image
    $('#secret_image').change(function() {
        showImagePreview(this, '#secret_image_preview');
    });
});