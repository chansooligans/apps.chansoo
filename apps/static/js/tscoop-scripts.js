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
                if (keyword && !keywords.includes(keyword)) {
                    keywords.push(keyword);
                    $('#keywords-wrapper').append(`<span class="keyword-bubble">${keyword}<span class="remove">x</span></span>`);
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
    });

    function updateHiddenKeywords() {
        $('input[name="keywords"]').val(keywords.join(','));
    }
});
