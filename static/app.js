console.log('JS loaded!');
$(document).ready(function() {
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
