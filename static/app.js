$.prototype.highlight = function (words) {
    words.forEach(w => {
            re = RegExp(w, 'gi')
            this.html(this.html().replace(re, $('<mark></mark>').text(w).prop('outerHTML')))
            console.log(this.html())
            //this.html("<p>AAAAAAAAAAAAAAAAAAAAAAAAA</p>")
        });
    return this;
}

console.log('JS loaded!');
$(document).ready(function() {
    $.ajax({
        url: '/keywords',
        dataType: 'json',
        success: function(response) {
            var listItems = response.map(item => $('<li></li>')
                .addClass('list-group-item')
                .append($('<span></span>')
                    .addClass('badge')
                    .addClass((item.score >= 0 ) ? 'badge-info' : 'badge-danger')
                    .text(item.score)
                    )
                .append(' ')
                .append($('<span></span>').text(item.word))
                .click(x => {
                    $('#card-list').empty();
                    $.ajax({
                        url: '/mentions',
                        data: {word: item.word},
                        success: function(response) {
                            $('#card-list')
                                .append($('<h3></h3>').text(item.word))
                                .append(
                                response.map(
                                    text => $('<div></div>')
                                        .addClass('card')
                                        .addClass('card-primary')
                                        .addClass('mb-3')
                                        .append(
                                            $('<div></div>')
                                                .addClass('card-block')
                                                .append($('<p></p>').text(text).highlight([item.word]))
                                        )
                                )
                            )
                        }
                    });
                })
            );
            $('#keyword-list').append(listItems)
        }
    });
	console.log('in ready');
	$('#annotate-button').click(function(e) {
		const commentText = $('#comment-field').val();
		console.log('click detected!');
		$.ajax({
		    url: '/annotate',
		    data: {comment: commentText},
		    success: function(response) {
			    console.log('response' + response);
			    positives = Object.keys(response).filter(x => response[x] > 0);
			    negatives = Object.keys(response).filter(x => response[x] < 0);
			    plusitems = positives.map(x => $('<li></li>').addClass('plusitem').text(x));
			    minusitems = negatives.map(x => $('<li></li>').addClass('minusitem').text(x));
			    $('#output-field').html('');
			    plusitems.forEach(x => $('#output-field').append(x));
			    minusitems.forEach(x => $('#output-field').append(x));
		    },
		    dataType: 'json'
		});
	});
});
