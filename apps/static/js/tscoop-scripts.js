$(document).ready(function () {
    const keywords = [];

    // Create a function to handle adding keywords
    function addKeywords(e) {
        if (e.type === 'keypress' && e.which !== 13 && e.which !== 9) {
            return;
        }
        e.preventDefault();
        const keywordInput = $('#keyword-input');
        const keywordValue = keywordInput.val().trim();
        if (keywordValue) {
            const keywordArray = keywordValue.split(','); // Split the keywords by comma
            keywordArray.forEach(function (keyword) {
                keyword = keyword.trim();
                if (keyword && !keywords.includes(keyword) && keywords.length < 3) {
                    keywords.push(keyword);
                    $('#keywords-wrapper').append(`<span class="keyword-bubble">${keyword}<span class="remove">x</span></span>`);
                } else if (keyword && !keywords.includes(keyword) && keywords.length === 3) {
                    // Show error when maximum number of keywords reached
                    $('#keyword-input').addClass('is-invalid');
                    keywordInput.val('');
                    keywordInput.attr('placeholder', 'Maximum number of keywords reached (3)');
                }
            });
            keywordInput.val('');
            updateHiddenKeywords();
            $('#keywords-wrapper').removeClass('d-none'); // Show the keywords wrapper
        }
    }

    // Bind the addKeywords function to the 'keypress' and 'focusout' events
    $('#keyword-input').on('keypress', addKeywords).on('focusout', addKeywords);

    $(document).on('click', '.keyword-bubble .remove', function () {
        const keyword = $(this).parent().text().slice(0, -1);
        const index = keywords.indexOf(keyword);
        if (index > -1) {
            keywords.splice(index, 1);
        }
        $(this).parent().remove();
        updateHiddenKeywords();
        if (keywords.length === 0) {
            $('#keywords-wrapper').addClass('d-none'); // Hide the keywords wrapper when all keywords are removed
        }

        // Clear the error message from the input box when keyword is removed
        $('#keyword-input').removeClass('is-invalid');
        $('#keyword-input').attr('placeholder', 'Cherry-pick news flavors! e.g. health, economy, AI, taylor swift...');
    });

    function updateHiddenKeywords() {
        $('input[name="keywords"]').val(keywords.join(','));
    }

    // Listen for form submission
    // Need to do this to make modal popup AND form validation with django
    $('form').on('submit', function (e) {
        e.preventDefault();

        // Perform any required validation or submission actions here


        // AJAX form submission
        $.ajax({
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function (response) {
                // Show the thank you modal
                var thankYouModal = new bootstrap.Modal(document.getElementById('thankYouModal'), {});
                thankYouModal.show();

                // Clear the form fields
                $('form').trigger('reset');
            },
            error: function (response) {

                // Handle any errors here
                console.log('Error:', response);
            }
        });

    });
});
