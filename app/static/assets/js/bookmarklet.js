/*PageImages - Bookmarklet*/
/*Based on Pinterest's bookmarklet*/ 

/*Todo: Add functions, show total number of images, filter between background and foreground, allow user to set max and min size. resize thumbnails. lightbox image. download all. */


if (typeof jQuery == 'undefined') {
	var jQ = document.createElement('script');
	jQ.type = 'text/javascript';
	jQ.onload=runthis;
	jQ.src = 'http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js';
	document.body.appendChild(jQ);
}

else {
	runthis();
}

function runthis() {
	
	jQuery(document).ready(function(){
    	
    	jQuery('html, body').animate({scrollTop:0}, 'fast');
    	var now = Date();
    	/* Check whether Bookmarklet is already visible */	
		if(jQuery('#image-grabber-container').length == 0) {
			var numberOfImages = 0;
			/*Add css - Must change this if you want to use your own CSS*/
			jQuery('<style type="text/css">@import url("http://test.keepcd.com/static/assets/css/bookmarklet.css?v='+now+'");</style>').appendTo("head");
			/*Add toggle*/
			jQuery('body').append('<div id="background-blocker"></div><div id="image-grabber-container"><div id="keepcd-button-toggle"><a id="keepcd-button-close" href="#">Close</a></div><ul id="list-of-images"></ul></div>');
			/*Make toggle work*/
			jQuery("#keepcd-button-close").click(function() {
				jQuery("#image-grabber-container, #background-blocker").remove();
			});
	
			/*Find images and add to list*/			
			// jQuery('img').each(function() {
			// 	var _sudoThing = jQuery(this);							
			// 	addImage(_sudoThing);
			// });
			addObject();
			/*Find background images and add to list*/
			// jQuery('*:visible').each(function() {
			// 	var _sudoBackground = jQuery(this);
			// 	var	backgroundImage = _sudoBackground.css('background-image');
			// 	if (backgroundImage !== "none")
			// 	{
			// 		addImage(_sudoBackground);
			// 	}			
			// });
   	}
   });
}
   	function addImageHtml(thumb){
   		var beginLiTag = "<li><a href='";
		var endATag = "'>";
		var beginImageTag = "<img src='";
		var middleImageTag = "' style='margin-top:";
		var endImageTag = "px'>";
		var endLiTag = "</a></li>";
		var imageWidth = thumb.width;
		var imageHeight = thumb.height;
		var calculatedMargin = 0;
		if (imageWidth > imageHeight) {
				calculatedMargin = (200 - (200 * (imageHeight / imageWidth))) * 0.5;
		}
		var imageURL = thumb.logo;
		var finalLink =  beginLiTag + imageURL + endATag + beginImageTag + imageURL + middleImageTag + calculatedMargin + endImageTag + "<span>" + imageWidth + " x " + imageHeight + "</span>" + endLiTag;
		jQuery('#list-of-images').append(finalLink);

   	}

	function addImage( imageToAdd ) {
				
		var imageURL = imageToAdd.attr('src');
		console.log(imageURL);
		
		if (imageURL === undefined)
		{
			console.log(imageToAdd.css('background-image').slice(4,-1));
			imageURL = imageToAdd.css('background-image').slice(4,-1);
		}
		
		var beginLiTag = "<li><a href='";
		var endATag = "'>";
		var beginImageTag = "<img src='";
		var middleImageTag = "' style='margin-top:";
		var endImageTag = "px'>";
		var endLiTag = "</a></li>";
		var imageWidth = imageToAdd.width();
		var imageHeight = imageToAdd.height();
		
		var containData = imageURL.indexOf('data:');

			
		/*Check whether image big enough*/
		if(imageWidth > 100 && imageHeight > 150 && containData === -1) {
			/*Calculate margin to vertically center*/		
			if (imageWidth > imageHeight) {
				var calculatedMargin = (200 - (200 * (imageHeight / imageWidth))) * 0.5;
			}
				
			else {
				calculatedMargin = 0;
				}
			
			var finalLink =  beginLiTag + imageURL + endATag + beginImageTag + imageURL + middleImageTag + calculatedMargin + endImageTag + "<span>" + imageWidth + " x " + imageHeight + "</span>" + endLiTag;
			jQuery('#list-of-images').append(finalLink);
			numberOfImages ++;
			
		}
		
	}

	function escapeImage(e) {
        var t = new Image;
        t.src = e.src;
        var n = {
            w: e.naturalWidth || e.width,
            h: e.naturalHeight || e.height,
            src: e.src,
            img: e,
            alt: "",
            img2: t
        };
        return n
    }

    function isValidImage(e) {
        return e.src && e.src.indexOf("data:") == 0 ? !1 : e.style.display != "none" && e.className != "ImageToPin" && e.width >= minWidth && e.height >= minHeight ? !0 : !1
    }

    function httpFetch(e) {
        var t = null;
        return t = new XMLHttpRequest,
        t.open("GET", e, !1),
        t.send(null),
        t.responseText
    }

	function addObject(){
		var url = document.location.href;
		var thumb = new Image;
		var images = [];
		if (url.indexOf("v.youku.com") > 0) {
            var json = eval("(" + httpFetch("http://v.youku.com/player/getPlayList/VideoIDS/" + videoId2) + ")");
            thumb.src = json.data[0].logo,
            thumb.width = 448,
            thumb.height = 336,
            thumb = escapeImage(thumb),
            thumb.container = _document.getElementById("player"),
            thumb.video = "http://player.youku.com/player.php/sid/" + videoId2 + "/v.swf",
            thumb.type = "video",
            images.push(thumb);
		}

		addImageHtml(thumb);

	}

