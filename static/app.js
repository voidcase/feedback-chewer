console.log('JS loaded!');
$(document).ready(function() {
	console.log('in ready');
	$('#annotate_button').click(function(e) {
		const commentText = $('#comment_field').val();
		console.log('click detected!');
		$.ajax({
		    url: '/annotate',
		    data: {comment: commentText},
		    success: function(response) {
			    console.log('response' + response);
			    $('#output_field').text(Object.keys(response).join(','));
		    },
		    dataType: 'json'
		});
	});
});
