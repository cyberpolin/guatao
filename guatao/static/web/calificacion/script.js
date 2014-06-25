$j = jQuery.noConflict();

$j(document).ready(function() {

	ContactOwnerBox();
	ClaimListingBox();
	ShowRegNotifications();
	ApplyLightbox();
	ApplyFancyboxVideo();
	//PrettySociableInit();
	CloseableComments();
	InitMisc();
	ResponsiveMenu();
	RollUpMenu();
	SubmenuClass();
	HoverZoomInit();
	WidgetsSize('footer-widgets');

	/* GRID GALLERY SHORTCODE :: START */
	// !!! order must be like this !!!
	gridGalleryShortcode();

    initTile();

    if($j('.portfolio').hasClass('item-direct')){
        directLink();
    } else if($j('.portfolio').hasClass('item-fancybox')) {
        itemFancybox();
    } else {
        if(parseInt($j(document).width()) < 500){
          directLink();
        } else {
          showTile();
        }
    }

    quicksand();

    categorySlider();

    tileHover();
    /* GRID GALLERY SHORTCODE :: END */

    wpcfFix();
});

function wpcfFix(){
	$j('span.wpcf7-form-control-wrap').hover(function(){
		$j(this).children('span.wpcf7-not-valid-tip').fadeOut('fast');
	});
}

function ContactOwnerBox() {

	var button = $j("#contact-owner-button");

	var args = {
		social_tools:false,
		deeplinking: false,
		changepicturecallback: function () {

			$j(".pp_pic_holder").addClass("contact-owner-popup");

			var form = $j(".contact-owner-popup #contact-owner-form"),
				email = form.data("email");

			form.find(".contact-owner-send").click(function(event) {
				if ((form.find('.cowner-name').val()) && (form.find('.cowner-email').val()) && (form.find('.cowner-subject').val()) && (form.find('.cowner-message').val())) {
					$j.post(MyAjax.ajaxurl, {
						action: 'ait_contact_owner',
						nonce: MyAjax.ajaxnonce,
						name: form.find('.cowner-name').val(),
						from: form.find('.cowner-email').val(),
						to: email,
						subject: form.find('.cowner-subject').val(),
						message: form.find('.cowner-message').val()
					}, function(data, textStatus, xhr) {
						if(data == "success"){
							form.find('.messages > div').hide();
							form.find('.messages .success').show();
						} else {
							form.find('.messages > div').hide();
							form.find('.messages .error.server').text(data).show();
						}
					});
				} else {
					form.find('.messages > div').hide();
					form.find('.messages .error.validator').show();
				}
				return false;
			});

			$j.placeholder.shim();

		}
	};

	// responsive
	if ($j(window).width() < 480) {
		args.default_width = 280;
	};

	button.prettyPhoto(args);

}

function ClaimListingBox() {

	var button = $j("#claim-listing-button");

	var args = {
		social_tools:false,
		deeplinking: false,
		changepicturecallback: function () {

			$j(".pp_pic_holder").addClass("claim-listing-popup");

			var form = $j(".claim-listing-popup #claim-listing-form");

			$j("#claim-listing-form .claim-listing-send").click(function(event) {

				if ((form.find('.claim-name').val()) && (form.find('.claim-email').val()) && (form.find('.claim-username').val()) && (form.find('.claim-message').val())) {
					$j.post(MyAjax.ajaxurl, {
						action: 'ait_new_claim',
						nonce: MyAjax.ajaxnonce,
						itemId: form.data('item-id'),
						name: form.find('.claim-name').val(),
						email: form.find('.claim-email').val(),
						number: form.find('.claim-number').val(),
						username: form.find('.claim-username').val(),
						message: form.find('.claim-message').val()
					}, function(data, textStatus, xhr) {
						if(data == "success"){
							form.find('.messages > div').hide();
							form.find('.messages .success').show();
						} else {
							form.find('.messages > div').hide();
							form.find('.messages .error.server').text(data).show();
						}
					});
				} else {
					form.find('.messages > div').hide();
					form.find('.messages .error.validator').show();
				}
				return false;
			});

			$j.placeholder.shim();

		}
	};

	// responsive
	if ($j(window).width() < 480) {
		args.default_width = 280;
	};

	button.prettyPhoto(args);

}

function ShowRegNotifications() {
	$j("#ait-dir-register-notifications .close").click(function () {
		$j(this).parent().parent().slideUp(500,function () {
			$j(this).remove();
		});
	});
}

function SubmenuClass() {
	var menuLinks = $j('nav.mainmenu a');
	$j(menuLinks).each(function () {
		if($j(this).next().is('ul')){
			$j(this).addClass('has-submenu');
		}
	});
}

function RollUpMenu(){
	$j("nav.mainmenu ul li").hover(function(){
		var submenu = $j(this).find('> ul');
		var submenuHeight = submenu.innerHeight();
		submenu.show().height(0).stop(true,true).animate({
			height: submenuHeight
		});
	}, function(){
		$j(this).find('> ul').hide();
	});
}

function ResponsiveMenu() {

	// Save list menu and create select
	var mainNavigation = $j('nav.mainmenu').clone();
	$j('nav.mainmenu').append('<select class="responsive-menu"></select>');
	var selectMenu = $j('select.responsive-menu');
	$j(selectMenu).append('<option>Main Menu...</option>');

	// Loop through each first level list items
	$j(mainNavigation).children('ul').children('li').each(function() {

		// Save menu item's attributes
 		var href = $j(this).children('a').attr('href'),
			text = $j(this).children('a').text();

		// Create menu item's option
		$j(selectMenu).append('<option value="'+href+'">'+text+'</option>');

		// Check if there is a second level of menu
		if ($j(this).children('ul').length > 0) {

			// Loop through each second level list items
			$j(this).children('ul').children('li').each(function() {

				// Save menu item's attributes
				var href2 = $j(this).children('a').attr('href'),
					text2 = $j(this).children('a').text();

				// Create menu item's option
				$j(selectMenu).append('<option value="'+href2+'">--- '+text2+'</option>');

				// Check if there is a third level of menu
				if ($j(this).children('ul').length > 0) {

					// Loop through each third level list items
					$j(this).children('ul').children('li').each(function() {

						// Save menu item's attributes
						var href3 = $j(this).children('a').attr('href'),
							text3 = $j(this).children('a').text();
						// Create menu item's option
						$j(selectMenu).append('<option value="'+href3+'">------ '+text3+'</option>');

					}); 	// End of third level loop
				} 			// If there is third level
			}); 			// End of second level loop
		} 					// If there is second level
	}); 					// End of first level loop

	$j(selectMenu).change(function() {
		location = this.options[this.selectedIndex].value;
	});
}

function InitMisc() {
	$j('#content input, #content textarea').each(function() {
		var id 	 = $j(this).attr('id'),
			name = $j(this).attr('name');

		if(id == undefined) {
			id = "";
		}

		if( name == undefined ) {
			name = "";
		}

		if (id.length == 0 && name.length != 0) {
			$j(this).attr('id', name);
		}
	});

	$j('.wpcf7 label, #comments label').inFieldLabels();

	$j('.rule .top').click(function(event) {
		$j("html, body").animate({ scrollTop: 0 }, "slow");
		return false;
	});

	$j('.sc-notification').children('a.close').click( function(event) {
		event.preventDefault();
		$j(this).parent().fadeOut('slow');
	});

	var more = $j('.more-link')
	if (more.not(':visible')) {
		more.parent().remove();
	};

}

function WidgetsSize(sidebar) {

	 $j('#'+sidebar+' .widget-container').each( function(index) {
	 	$j(this).addClass('col-' + (index + 1));
	 });
}

function HoverZoomInit() {
	//// Post images
	//$j('article .entry-thumbnail a').hoverZoom({overlayColor:'#ffffff',overlayOpacity: 0.8,zoom:0});

	// default wordpress gallery
	$j('.entry-content .gallery-item a').hoverZoom({overlayColor:'#333',overlayOpacity: 0.8,zoom:0});

	// ait-portfolio
	$j('.entry-content .ait-portfolio a').hoverZoom({overlayColor:'#333',overlayOpacity: 0.8,zoom:0});

	// schortcodes
	$j('.entry-content a.sc-image-link').hoverZoom({overlayColor:'#333',overlayOpacity: 0.8,zoom:0});

}

function CloseableComments() {
	var comments = $j('.closeable #comments'),
		commentlist = comments.find('.commentlist'),
		button 	 = comments.parent().find('.open-button');

	if(comments.children().length == 0) {

		$j('.closeable').remove();

	} else {

		button.show();

		if(button.hasClass('comments-closed') && commentlist.is(':visible')) {
			commentlist.hide();
		}

		button.click(function() {

			if (button.hasClass('comments-closed')) {

				commentlist.not(':animated').slideDown('slow') && button.removeClass('comments-closed').addClass('comments-opened');
				if(button.hasClass('item')){
					button.text('Close Reviews');
				} else {
					button.text('Close Comments');
				}

			} else if (button.hasClass('comments-opened')) {

				commentlist.not(':animated').slideUp('slow') && button.removeClass('comments-opened').addClass('comments-closed');
				if(button.hasClass('item')){
					button.text('Show Reviews');
				} else {
					button.text('Show Comments');
				}

			} else {

				commentlist.slideToggle();

			}
		});
	}
}

function ApplyLightbox(){
	// make galleries
	var selector = "a[href$='gif'], a[href$='jpg'], a[href$='png']",
		linksWithImages = $j(selector);
	// groups
	linksWithImages.attr('rel', 'prettyPhoto[]');
	$j(".widget_flickr").find(selector).attr('rel', 'prettyPhoto[flickr]');
	$j(".gallery").find(selector).attr('rel', 'prettyPhoto[gallery]');
	// apply pretty photo
	linksWithImages.prettyPhoto({
		allow_resize: true,
		default_width: window.innerWidth - 20,
		deeplinking: false,
		social_tools: '',
	});
}

function ApplyFancyboxVideo(){
	// AIT-Portfolio videos
	$j(".ait-portfolio a.video-type").click(function() {

		var address = this.href
		if(address.indexOf("youtube") != -1){
			// Youtube Video
			$j.fancybox({
				'padding'		: 0,
				'autoScale'		: false,
				'transitionIn'	: 'elastic',
				'transitionOut'	: 'elastic',
				'title'			: this.title,
				'width'			: 680,
				'height'		: 495,
				'href'			: this.href.replace(new RegExp("watch\\?v=", "i"), 'v/'),
				'type'			: 'swf',
				'swf'			: {
					'wmode'		: 'transparent',
					'allowfullscreen'	: 'true'
				}
			});
		} else if (address.indexOf("vimeo") != -1){
			// Vimeo Video
			// parse vimeo ID
			var regExp = /http:\/\/(www\.)?vimeo.com\/(\d+)($|\/)/;
			var match = this.href.match(regExp);

			if (match){
			    $j.fancybox({
					'padding'		: 0,
					'autoScale'		: false,
					'transitionIn'	: 'elastic',
					'transitionOut'	: 'elastic',
					'title'			: this.title,
					'width'			: 680,
					'height'		: 495,
					'href'			: "http://player.vimeo.com/video/"+match[2]+"?title=0&amp;byline=0&amp;portrait=0&amp;color=ffffff",
					'type'			: 'iframe'
				});
			} else {
			    alert("not a vimeo url");
			}
		}
		return false;
	});

	// Images shortcode
	$j("a.sc-image-link.video-type").click(function() {

		var address = this.href
		if(address.indexOf("youtube") != -1){
			// Youtube Video
			$j.fancybox({
				'padding'		: 0,
				'autoScale'		: false,
				'transitionIn'	: 'elastic',
				'transitionOut'	: 'elastic',
				'title'			: this.title,
				'width'			: 680,
				'height'		: 495,
				'href'			: this.href.replace(new RegExp("watch\\?v=", "i"), 'v/'),
				'type'			: 'swf',
				'swf'			: {
					'wmode'		: 'transparent',
					'allowfullscreen'	: 'true'
				}
			});
		} else if (address.indexOf("vimeo") != -1){
			// Vimeo Video
			// parse vimeo ID
			var regExp = /http:\/\/(www\.)?vimeo.com\/(\d+)($|\/)/;
			var match = this.href.match(regExp);

			if (match){
			    $j.fancybox({
					'padding'		: 0,
					'autoScale'		: false,
					'transitionIn'	: 'elastic',
					'transitionOut'	: 'elastic',
					'title'			: this.title,
					'width'			: 680,
					'height'		: 495,
					'href'			: "http://player.vimeo.com/video/"+match[2]+"?title=0&amp;byline=0&amp;portrait=0&amp;color=ffffff",
					'type'			: 'iframe'
				});
			} else {
			    alert("not a vimeo url");
			}
		}
		return false;
	});
}

function PrettySociableInit(){

	var homeUrl = $j("body").data("themeurl");

	$j.prettySociable({websites: {
		facebook : {
			'active': true,
			'encode':true, // If sharing is not working, try to turn to false
			'title': 'Facebook',
			'url': 'http://www.facebook.com/share.php?u=',
			'icon':homeUrl+'/design/img/prettySociable/large_icons/facebook.png',
			'sizes':{'width':70,'height':70}
		},
		twitter : {
			'active': true,
			'encode':true, // If sharing is not working, try to turn to false
			'title': 'Twitter',
			'url': 'http://twitter.com/home?status=',
			'icon':homeUrl+'/design/img/prettySociable/large_icons/twitter.png',
			'sizes':{'width':70,'height':70}
		},
		delicious : {
			'active': true,
			'encode':true, // If sharing is not working, try to turn to false
			'title': 'Delicious',
			'url': 'http://del.icio.us/post?url=',
			'icon':homeUrl+'/design/img/prettySociable/large_icons/delicious.png',
			'sizes':{'width':70,'height':70}
		},
		digg : {
			'active': true,
			'encode':true, // If sharing is not working, try to turn to false
			'title': 'Digg',
			'url': 'http://digg.com/submit?phase=2&url=',
			'icon':homeUrl+'/design/img/prettySociable/large_icons/digg.png',
			'sizes':{'width':70,'height':70}
		},
		linkedin : {
			'active': true,
			'encode':true, // If sharing is not working, try to turn to false
			'title': 'LinkedIn',
			'url': 'http://www.linkedin.com/shareArticle?mini=true&ro=true&url=',
			'icon':homeUrl+'/design/img/prettySociable/large_icons/linkedin.png',
			'sizes':{'width':70,'height':70}
		},
		reddit : {
			'active': true,
			'encode':true, // If sharing is not working, try to turn to false
			'title': 'Reddit',
			'url': 'http://reddit.com/submit?url=',
			'icon':homeUrl+'/design/img/prettySociable/large_icons/reddit.png',
			'sizes':{'width':70,'height':70}
		},
		stumbleupon : {
			'active': true,
			'encode':false, // If sharing is not working, try to turn to false
			'title': 'StumbleUpon',
			'url': 'http://stumbleupon.com/submit?url=',
			'icon':homeUrl+'/design/img/prettySociable/large_icons/stumbleupon.png',
			'sizes':{'width':70,'height':70}
		},
		tumblr : {
			'active': true,
			'encode':true, // If sharing is not working, try to turn to false
			'title': 'tumblr',
			'url': 'http://www.tumblr.com/share?v=3&u=',
			'icon':homeUrl+'/design/img/prettySociable/large_icons/tumblr.png',
			'sizes':{'width':70,'height':70}
		}
	}});

}