jQuery(document).ready(function($) {

	var themeUrl = $('body').data('themeurl');
	var postId = $('#ait-rating-system').data('post-id');
	var star = $('#ait-rating-system .rating-send-form .star');
	var sendForm = $('#ait-rating-system button.send-rating');
	
	// invield labels
	if ($.fn.inFieldLabels) {
		$('#ait-rating-system label').inFieldLabels();
	}

	// hover effect
	$(document).on("mouseenter", "#ait-rating-system .rating-send-form .star", function() {
		var id = parseInt($(this).data('star-id'));
		$(this).parent().find('> div').slice(0,id).css("background","url('"+themeUrl+"/design/img/rating_star_hover.png') no-repeat 0 0");
	});
	$(document).on("mouseleave", "#ait-rating-system .rating-send-form .star", function() {
		var rating = $(this).parent().parent();
		var mean = parseInt(rating.data('rated-value'));
		$(this).parent().find('> div').css("background","url('"+themeUrl+"/design/img/rating_star.png') no-repeat 0 0");
		$(this).parent().find('> div').slice(0,mean).css("background","url('"+themeUrl+"/design/img/rating_star_active.png') no-repeat 0 0");
	});

	// rating
	$(document).on("click", "#ait-rating-system .rating-send-form .star", function(event) {
		var rating = $(this).parent().parent();
		var ratingId = rating.data('rating-id');
		var id = parseInt($(this).data('star-id'));
		$(this).parent().find('> div').slice(0,id).css("background","url('"+themeUrl+"/design/img/rating_star_active.png') no-repeat 0 0");
		rating.data('rated-value',id).addClass('already');		
	});

	// send via ajax
	$(document).on("click", "#ait-rating-system button.send-rating", function(event) {
		var values = {};
		var validator = true;
		$('#ait-rating-system .rating-send-form .rating').each(function(event) {
			if($(this).data('rated-value') == '0'){
				validator = false;
			}
			values[$(this).data('rating-id')] = $(this).data('rated-value');
		});
		if(!$('#ait-rating-system #rating-name').val()) { validator = false };

		if(validator) {
			$.post(MyAjax.ajaxurl, { action: 'ait_rate_item', nonce: MyAjax.ajaxnonce, post_id: postId, rating_name: $('#ait-rating-system #rating-name').val(), rating_description: $('#ait-rating-system #rating-description').val(), rating_values: values }, function(data, textStatus, xhr) {
				if(data != "nonce" && data != "already" && data != "nonce"){
					$('#ait-rating-system').replaceWith(data);
					if ($.fn.inFieldLabels) {
						$('#ait-rating-system label').inFieldLabels();
					}
				}
			});
		} else {
			// show error message
			$('#ait-rating-system .rating-send-form .message.success').hide();
			$('#ait-rating-system .rating-send-form .message.error').show();
		}
	});

	// user ratings details
	$(document).on("mouseover", "#ait-rating-system .user-details .value", function(event) {
		$(this).parent().parent().find('.user-values').show();
	});
	$(document).on("mouseout", "#ait-rating-system .user-details .value", function(event) {
		$(this).parent().parent().find('.user-values').hide();
	});

});