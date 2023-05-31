$(document).ready(function () {

    validKeywords  = [
        'us',
        'world',
        'world news',
        'business',
        'technology',
        'entertainment',
        'sports',
        'science',
        'health',
        'economy',
        'economics',
        'markets',
        'jobs',
        'personal finance',
        'entrepreneurship',
        'mobile',
        'gadgets',
        'internet',
        'vr',
        'virtual reality',
        'ai',
        'artificial intelligence',
        'computing',
        'movies',
        'music',
        'tv',
        'books',
        'arts',
        'design',
        'celebrities',
        'environment',
        'space',
        'physics',
        'genetics',
        'wildlife',
        'healthcare',
        'health care',
        'mental health',
        'nutrition',
        'fitness',
        'medication',
        'taylor swift',
        'politics',
        'education',
        'real estate',
        'travel',
        'social media',
        'cybersecurity',
        'climate change',
        'renewable energy',
        'sustainability',
        'human rights',
        'immigration',
        'cultural diversity',
        'philosophy',
        'animal rights',
        'architecture',
        'astronomy',
        'military',
        'gender equality',
        'religion',
        'terrorism',
        'infrastructure',
        'agriculture',
        'aviation',
        'psychology',
        'robotics',
        'quantum computing',
        'emerging technologies',
        'pharmaceutical industry',
        'insurance',
        'retail',
        'e-commerce'
    ].map(keyword => keyword.toLowerCase());
    
    ///////////////////////
    // AutoComplete
    ///////////////////////

    const autoCompleteJS = new autoComplete({
        placeHolder: "Cherry-pick news flavors! e.g. health, economy, AI, politics...",
        data: {
            src: validKeywords ,
            cache: true,
        },
        resultItem: {
            highlight: true
        },
        resultsList: {
            element: (list, data) => {
                if (!data.results.length) {
                    // Create "No Results" message list element
                    const message = document.createElement("li");
                    // Add message text content
                    message.innerHTML = `Found No Results for "${data.query}"`;
                    // Add message list element to the list
                    list.appendChild(message);
                }
            },
            noResults: true,
        },
        events: {
            input: {
                selection: (event) => {
                    const selection = event.detail.selection.value;
                    autoCompleteJS.input.value = selection;
                }
            }
        },
        submit: true,
        searchEngine: "loose"
    });

    // 
    const keywords = [];

    ///////////////////////
    // ADDING KEYWORDS
    ///////////////////////

    // Helper functions
    function addKeyword(keyword) {
        keywords.push(keyword);
        $('#keywords-wrapper').append(`<span class="keyword-bubble">${keyword}<span class="remove">x</span></span>`);
        $('#autoComplete').attr('placeholder', 'Cherry-pick news flavors! e.g. health, economy, AI, politics...');
        updateHiddenKeywords();
        $('#keywords-wrapper').removeClass('d-none');
    }

    function handleErrors(keyword, inputElement) {
        inputElement.addClass('is-invalid');
        if (keywords.length === 3) {
            inputElement.val('').attr('placeholder', 'Maximum number of keywords reached (3)');
        } else {
            inputElement.val('').attr('placeholder', 'Invalid Keyword -- Try "politics" or "sports"!');
        }
    }

    // Main function
    function addKeywords(e) {
        if (e.type === 'keypress' && e.which !== 13 && e.which !== 9) {
            return;
        }
        e.preventDefault();
        const keywordInput = $('#autoComplete');
        const keywordValue = keywordInput.val().trim().toLowerCase();
        if (keywordValue) {
            const keywordArray = keywordValue.split(',');
            keywordArray.forEach(function (keyword) {
                keyword = keyword.trim();
                if (validKeywords.includes(keyword) && !keywords.includes(keyword) && keywords.length < 3) {
                    addKeyword(keyword);
                    keywordInput.val('');
                } else {
                    handleErrors(keyword, keywordInput);
                }
            });
        }
    }


    // Bind the addKeywords function to the 'keypress' and 'focusout' events
    $('#autoComplete').on('keypress', addKeywords).on('focusout', addKeywords);

    ///////////////////////
    // REMOVING KEYWORDS
    ///////////////////////

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
        $('#autoComplete').removeClass('is-invalid');
        $('#autoComplete').attr('placeholder', 'Cherry-pick news flavors! e.g. health, economy, AI, politics...');
    });

    function updateHiddenKeywords() {
        keywords.sort((a, b) => a.trim().toLowerCase().localeCompare(b.trim().toLowerCase()));
        $('input[name="keywords"]').val(keywords.join(','));
    }

    ///////////////////////
    // FORM SUBMISSION
    ///////////////////////

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
