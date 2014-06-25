function gridGalleryShortcode(){
  var contWidth = $j('.gridgallery').parent().width();
  var tileMargin = 10; 
  var tileBorder = 2;
  var tileRowNum = 5;
  var tileCount = 0;
  var origPict = "";
  var origSize;
  var rowsCount;
  var descHeight = 0;
  var descMarginBottom = 0;
  var superDescHeight = 0;
  if($j('.gridgallery').hasClass('five')){
     tileRowNum = 5;
  } else if($j('.gridgallery').hasClass('four')){
     tileRowNum = 4;
  } else if($j('.gridgallery').hasClass('three')){
     tileRowNum = 3;
  } 
  var tileHeight = $j("#gridgallery-setting-height").html();
  var tileWidth = parseInt((contWidth-(tileRowNum*(tileMargin+(tileBorder*2))))/tileRowNum)+parseInt(tileMargin/tileRowNum);
    
  $j('.gridgallery .ulHolder').css({'background':'none'});
  
  var tileCounter = 1;
  var rowCounter = 1;
  var tileCounterSmall = 1;
  var rowCounterSmall = 1;
  var tileCountGlobal = 0;
  $j('.gridgallery .ulHolder .ourHolder .item').each(function(){
    tileCountGlobal++;
  });
  rowCount = Math.ceil(tileCountGlobal/tileRowNum);
  $j('.gridgallery .ulHolder .ourHolder .item').each(function(){
    var editImage;
    var currTile = $j(this).children('.tile').children('.tileWrap');
    var currImage = currTile.html();
    if(tileHeight == 'auto'){
      editImage = currImage.replace('w=1',"w="+tileWidth).replace('h=1',"h="+tileWidth);
      currTile.html('<img src="'+editImage+'" width="'+tileWidth+'" height="'+tileWidth+'" alt="tile" />');
    } else {
      editImage = currImage.replace('w=1',"w="+tileWidth).replace('h=1',"h="+parseInt(tileHeight));
      currTile.html('<img src="'+editImage+'" width="'+tileWidth+'" height="'+tileHeight+'" alt="tile" />');
    }
    $j(this).children('.tile').width(tileWidth);
    $j(this).children('.tile').css({'display':'block'});
    $j(this).children('.tile-desc-wrap').children('.tile-desc').width(tileWidth);
    $j(this).children('.tile-desc-wrap').children('.tile-desc').css({'margin-left':tileMargin+tileBorder+'px'});
    $j(this).children('.tile-desc-wrap').children('.tile-desc').css({'margin-bottom':descMarginBottom+'px'});
    
    if($j(this).children().size() > 1){
      descHeight = parseInt($j(this).children('.tile-desc-wrap').children('.tile-desc').css('height'));
      descMarginBottom = 10;
      if(superDescHeight == 0){
        superDescHeight = descHeight;
      }
      $j(this).children('.tile-desc-wrap').height(superDescHeight);
      $j(this).children('.tile-desc-wrap').children('.tile-desc').height(superDescHeight);
    }
    
    if(tileHeight == 'auto'){
      $j(this).children('.tile').height(tileWidth);
      $j(this).children('.tile').parent().height(parseInt(tileWidth) + superDescHeight + descMarginBottom + tileBorder + tileMargin);
    } else {
      $j(this).children('.tile').height(parseInt(tileHeight));
      $j(this).children('.tile').parent().height(parseInt(tileHeight) + superDescHeight + descMarginBottom + tileBorder + tileMargin);
    }
    
    // children
    currChildTile = $j(this).children('.tile').children('.gridgallery-icon').children();
    
    if($j('.portfolio').hasClass('item-fancybox')){ } else {
      if(tileHeight == 'auto'){
        parsedWidth = parseInt((tileWidth*2)+tileMargin+(tileBorder*2));
        editImage = currImage.replace('w=1',"w="+parsedWidth).replace('h=1',"h="+parseInt(parsedWidth+(descHeight*2)+(descMarginBottom*2)));
        editImage = editImage.replace(/&amp;/g,"&");
        currChildTile.css({'background':'url(\''+editImage+'\') no-repeat center center'})
      } else {
        editImage = currImage.replace('w=1',"w="+((tileWidth*2)+tileMargin+(tileBorder*4))).replace('h=1',"h="+((parseInt(tileHeight)*2)+tileMargin+(tileBorder*4)+(descHeight*2)+(descMarginBottom*2)));
        editImage = editImage.replace(/&amp;/g,"&");
        currChildTile.css({'background':'url(\''+editImage+'\') no-repeat center center'})
      }
    }
    currChildTile.width(((tileWidth*2)+tileMargin+(tileBorder*2)));
    
    if(tileHeight == 'auto'){
      currChildTile.height(((tileWidth*2)+tileMargin+(tileBorder*2)));
    } else {
      currChildTile.height(((parseInt(tileHeight)*2)+tileMargin+(tileBorder*2) + (descHeight*2) + (descMarginBottom*2)));
    }
    
    if(rowCounter == 1){
      // first row
      if(tileCounter == 1){
        // first row | first tile
        if(tileHeight == 'auto'){
          currChildTile.css({'top':'-'+tileBorder+'px','left':'-'+tileBorder+'px','bottom':'0px','right':'0px','margin-left':'0px'});
        } else {
          currChildTile.css({'top':'-'+tileBorder+'px','left':'-'+tileBorder+'px','bottom':'0px','right':'0px','margin-left':'0px'});
        }
      } else if (tileCounter == tileRowNum){
        // first row | last tile
        if(tileHeight == 'auto'){
          currChildTile.css({'left':'-'+(tileWidth+tileMargin+tileBorder*3)+'px','right':'0px','top':'-'+tileBorder+'px' ,'margin-left':'0px'});
        } else {
          currChildTile.css({'left':'-'+(tileWidth+tileMargin+tileBorder*3)+'px','right':'0px','top':'-'+tileBorder+'px' ,'margin-left':'0px'});
        }
        tileCounter = 0;
        rowCounter++;
      } else {
        // first row | tiles between first and last
        currChildTile.css({'top':'-'+tileBorder+'px','left':'-'+tileBorder+'px','bottom':'0px','margin-left':'0px'});
      }
    } else if (rowCounter == (rowCount)){
      // last row
      if(tileCounter == 1){
        // last row | first tile
        if(tileHeight == 'auto'){
          currChildTile.css({'top':'-'+(tileWidth+tileMargin+tileBorder*2+descHeight+descMarginBottom)+'px','left':'-'+tileBorder+'px','bottom':'0px','bottom':'0px','right':'0px','margin-left':'0px'});
        } else {
          currChildTile.css({'top':'-'+(parseInt(tileHeight)+tileMargin+tileBorder*2+descHeight+descMarginBottom)+'px','left':'-'+tileBorder+'px','bottom':'0px','bottom':'0px','right':'0px','margin-left':'0px'});
        }
      } else if (tileCounter == tileRowNum){
        // last row | last tile
        if(tileHeight == 'auto'){
          currChildTile.css({'top':'-'+(tileWidth+tileMargin+tileBorder*2+descHeight+descMarginBottom)+'px','bottom':'0px','left':'-'+(tileWidth+tileMargin+tileBorder*3)+'px','bottom':'0px','right':'0px','margin-left':'0px'});
        } else {
          currChildTile.css({'top':'-'+(parseInt(tileHeight)+tileMargin+tileBorder*2+descHeight+descMarginBottom)+'px','bottom':'0px','left':'-'+(tileWidth+tileMargin+tileBorder*3)+'px','bottom':'0px','right':'0px','margin-left':'0px'});
        }
        tileCounter = 0;
        rowCounter++;
      } else {
        // last row | tiles between first and last
        if(tileHeight == 'auto'){
          currChildTile.css({'top':'-'+(tileWidth+tileMargin+tileBorder*2+descHeight+descMarginBottom)+'px','left':'-'+tileBorder+'px','bottom':'0px','margin-left':'0px'});
        } else {
          currChildTile.css({'top':'-'+(parseInt(tileHeight)+tileMargin+tileBorder*2+descHeight+descMarginBottom)+'px','left':'-'+tileBorder+'px','bottom':'0px','margin-left':'0px'});
        }
      }
    } else {
      // rows between first and last
      if(tileCounter == 1){
        // rows between first and last | first tile
        currChildTile.css({'top':'-'+tileBorder+'px','left':'-'+tileBorder+'px','bottom':'0px','right':'0px','margin-left':'0px'});
      } else if (tileCounter == tileRowNum){
        // rows between first and last | last tile
        if(tileHeight == 'auto'){
          currChildTile.css({'left':'-'+(tileWidth+tileMargin+tileBorder*3)+'px','right':'0px','top':'-'+tileBorder+'px','margin-left':'0px'});
        } else {
          currChildTile.css({'left':'-'+(tileWidth+tileMargin+tileBorder*3)+'px','right':'0px','top':'-'+tileBorder+'px','margin-left':'0px'});
        }
        tileCounter = 0;
        rowCounter++;
      } else {
        // rows between first and last | tiles between first and last
        currChildTile.css({'top':'-'+tileBorder+'px','left':'-'+tileBorder+'px','bottom':'0px','margin-left':'0px'});
      }
    } 
    tileCount++;
    tileCounter++;    
  });
  $j('.gridgallery').width(contWidth);  // width fix
  
  if(tileHeight == 'auto'){
    $j('.gridgallery .ulHolder .ourHolder').height(((tileWidth+tileMargin+descHeight+descMarginBottom)*rowCount+(tileBorder*2))+(tileMargin*2)+(tileBorder*2));
    $j('.gridgallery .ulHolder').height(((tileWidth+tileMargin+(tileBorder*2)+descHeight+descMarginBottom)*rowCount)+(tileMargin*2)+(tileBorder*2));
    $j('.gridgallery .portfolioHolder').css({'margin-left':'-'+tileMargin+'px'});
  } else {
    $j('.gridgallery .ulHolder .ourHolder').height(((parseInt(tileHeight)+tileMargin+descHeight+descMarginBottom)*rowCount+(tileBorder*2))+(tileMargin*2)+(tileBorder*2));
    $j('.gridgallery .ulHolder').height(((parseInt(tileHeight)+tileMargin+(tileBorder*2)+descHeight+descMarginBottom)*rowCount)+(tileMargin*2)+(tileBorder*2));
    $j('.gridgallery .portfolioHolder').css({'margin-left':'-'+tileMargin+'px'});
  }
  $j('.gridgallery #portfolio-loader').fadeOut('fast');
  $j('.gridgallery #filterOptions').css({'visibility':'visible'});
  $j('.gridgallery .port-cat').css({'visibility':'visible'});
  $j('.gridgallery .ulHolder').css({'visibility':'visible'});
}

function refreshGridGallery(){
  var contWidth = $j('.gridgallery').parent().width();
  var tileRowNum = 5;
  var tileMargin = 10;  // margin: 0 0 3px 3px 
  var tileBorder = 2;  // border: 10px
  var tileCount = 0;
  var tileCounter = 1;
  var rowCounter = 1;
  var tileCountGlobal = 0;
  var descHeight = 0;
  var descMarginBottom = 0;
  if($j('.gridgallery').hasClass('five')){
     tileRowNum = 5;
  } else if($j('.gridgallery').hasClass('four')){
     tileRowNum = 4;
  } else if($j('.gridgallery').hasClass('three')){
     tileRowNum = 3;
  }
  var tileHeight = $j("#gridgallery-setting-height").html();  
  var tileWidth = parseInt((contWidth-(tileRowNum*tileMargin))/tileRowNum);
  $j('.gridgallery .ulHolder .ourHolder .item').each(function(){
    tileCountGlobal++;
  });
  rowCount = Math.ceil(tileCountGlobal/tileRowNum);
  $j('.gridgallery .ulHolder .ourHolder .item').each(function(){
    if($j(this).children().size() > 1){
      descHeight = parseInt($j(this).children('.tile-desc').css('height'));
      descMarginBottom = 10;
    }
    
    var tile_small = $j(this).children('.tile');
    var tile_big = tile_small.children().children('a'); 
    if(rowCounter == 1){
      // first row
      if(tileCounter == 1){
        // first row | first tile
        tile_big.css({'top':'-'+tileBorder+'px','left':'-'+tileBorder+'px','bottom':'0px','right':'0px','margin-left':'0px'});
      } else if (tileCounter == tileRowNum){
        // first row | last tile
        if(tileHeight == 'auto'){
          tile_big.css({'left':'-'+(tileWidth+tileMargin+tileBorder*2)+'px','right':'0px','top':'-'+tileBorder+'px' ,'margin-left':'0px'});
        } else {
          tile_big.css({'left':'-'+(tileWidth+tileMargin+tileBorder)+'px','right':'0px','top':'-'+tileBorder+'px' ,'margin-left':'0px'});
        }
        tileCounter = 0;
        rowCounter++;
      } else {
        // first row | tiles between first and last
        if(tileHeight == 'auto'){
          tile_big.css({'top':'-'+tileBorder+'px','left':'-'+tileBorder+'px','bottom':'0px','margin-left':'0px'});
        } else {
          tile_big.css({'top':'-'+tileBorder+'px','left':'-'+tileBorder+'px','bottom':'0px','margin-left':'0px'});
        }
      }
    } else if (rowCounter == (rowCount)){
      // last row
      if(tileCounter == 1){
        // last row | first tile
        if(tileHeight == 'auto'){
          tile_big.css({'top':'-'+(tileWidth+tileMargin+tileBorder+descHeight+descMarginBottom)+'px','left':'-'+tileBorder+'px','bottom':'0px','bottom':'0px','right':'0px','margin-left':'0px'});
        } else {
          tile_big.css({'top':'-'+(parseInt(tileHeight)+tileMargin+tileBorder*2+descHeight+descMarginBottom)+'px','left':'-'+tileBorder+'px','bottom':'0px','bottom':'0px','right':'0px','margin-left':'0px'});
        }
      } else if (tileCounter == tileRowNum){
        // last row | last tile
        if(tileHeight == 'auto'){
          tile_big.css({'top':'-'+(tileWidth+tileMargin+tileBorder+descHeight+descMarginBottom)+'px','bottom':'0px','left':'-'+(tileWidth+tileMargin+tileBorder)+'px','bottom':'0px','right':'0px','margin-left':'0px'});
        } else {
          tile_big.css({'top':'-'+(parseInt(tileHeight)+tileMargin+tileBorder*2+descHeight+descMarginBottom)+'px','bottom':'0px','left':'-'+(tileWidth+tileMargin+tileBorder)+'px','bottom':'0px','right':'0px','margin-left':'0px'});
        }
        tileCounter = 0;
        rowCounter++;
      } else {
        // last row | tiles between first and last
        if(tileHeight == 'auto'){
          tile_big.css({'top':'-'+(tileWidth+tileMargin+(tileBorder)+descHeight+descMarginBottom)+'px','left':'-'+tileBorder+'px','bottom':'0px','margin-left':'0px'});
        } else {
          tile_big.css({'top':'-'+(parseInt(tileHeight)+tileMargin+(tileBorder*2)+descHeight+descMarginBottom)+'px','left':'-'+tileBorder+'px','bottom':'0px','margin-left':'0px'});
        }
      }
    } else {
      // rows between first and last
      if(tileCounter == 1){
        // rows between first and last | first tile
        tile_big.css({'top':'-'+tileBorder+'px','left':'-'+tileBorder+'px','bottom':'0px','right':'0px','margin-left':'0px'});
      } else if (tileCounter == tileRowNum){
        // rows between first and last | last tile
        if(tileHeight == 'auto'){
          tile_big.css({'left':'-'+(tileWidth+tileMargin+tileBorder)+'px','right':'0px','top':'-'+tileBorder+'px','margin-left':'0px'});
        } else {
          tile_big.css({'left':'-'+(tileWidth+tileMargin+tileBorder)+'px','right':'0px','top':'-'+tileBorder+'px','margin-left':'0px'});
        }
        tileCounter = 0;
        rowCounter++;
      } else {
        // rows between first and last | tiles between first and last
        tile_big.css({'top':'-'+tileBorder+'px','left':'-'+tileBorder+'px','bottom':'0px','margin-left':'0px'});
      }
    }     
    tileCount++;
    tileCounter++;
  });
}

function initTile() {
	if($j('#header-container').css('display') == 'none') {$j('#header-container').remove();}
	
	$j('.tile').each( function() {
		$j(this).removeClass('endLine corner goRight');
	});
	counter = 0;
	if($j('.portfolio').hasClass('five')){counter = 5;}
	if($j('.portfolio').hasClass('four')){counter = 4;}
	if($j('.portfolio').hasClass('three')){counter = 3;}
	
	sizeOfRows = Math.ceil(($j('.tile').size())/(counter));
	cou = 0;
	$j('.tile').each( function() {
		cou++;
		if((cou) == counter){
			$j(this).addClass('goRight');
			cou = 0;
		}
	});
	
	fullRow = sizeOfRows - 1;
	var n;
	for (n=0;n<=$j('.tile').size();n++) {
		if(n >= (counter * fullRow)){
			if(fullRow != 0) {
				$j('.tile').eq(n).addClass('endLine');
			}
		}
		if(n == ($j('.tile').size()-1) && n != counter * fullRow ) {
			$j('.tile').eq(n).addClass('corner').removeClass('goRight');
		}
		if(n == ($j('.tile').size()-1) && fullRow == 0) {
			$j('.tile').eq(n).addClass('goRight').removeClass('corner');
		}
	}
	//$j('.tile').last().addClass('corner');
        
        if($j('.tile').size() == 1){
            $j('.tile').removeClass('corner').removeClass('goRight').removeClass('endLine');
        }
}

function showTile() {	
	var tileMargin = 10;
	var tileBorder = 2;
  var descHeight = 0;
  var descMarginBottom = 0;
  
  if($j('.item').children('.tile-desc')){
      descHeight = parseInt($j('.item').children('.tile-desc').css('height'));
      descMarginBottom = 10;
    }
  
  $j('span').click(function(){
	 $j('.tile').unbind('mouseleave');
		var cat = $j(this).attr('class');
		$j('.portfolio .tile').each( function() {
				$j(this).children().children('.bbox').css('opacity','0');
			if( !$j(this).hasClass(cat)) {
				$j(this).children().children('.bbox').animate({opacity: '+=0.6'});
				//$j(this).children('.bbox').show();
			}
		});
	});

	tileWidth = (($j('.tile').width()*2)+tileMargin+(tileBorder*2));
	tileHeight = (($j('.tile').height()*2)+tileMargin+(2*tileBorder)+(descHeight*2)+descMarginBottom);
	tileMarginLeft = parseInt($j('.goRight').children().children('.tileImage').css('marginLeft'));
	
	$j('.tile').children().children('.tileImage').css('width',tileWidth).css('height',tileHeight);
	
	$j('.tile').click( function() {
        try{
            window.getSelection().removeAllRanges();
        }
	catch(e){}
	  $j('.tile').css('opacity','1');
		$j(this).removeClass('noOut');
		if($j(this).hasClass('noOut')){
			$j('.tile').children().children('.tileImage').children('.about').fadeOut('fast')
			$j('.tile').children().children('.tileImage').fadeOut('fast')
			$j('.tile').css('opacity','1');
		}
		else{
			//$j(this).children('.tileImage').children('.about').css('display','block');
			if($j(this).hasClass('goRight')){
				$j(this).addClass('noOut');
				$j(this).addClass('notOpacity');
				$j('.tile').each(function(){
					if($j(this).hasClass('notOpacity')){$j(this).removeClass('notOpacity');}
					else {
						$j(this).css('opacity','0.5');
					}
				});
				$j(this).children().children('.tileImage').fadeIn('normal').css('zIndex','110');
				
			}
			else {
				if($j(this).hasClass('endLine')) {
					$j(this).addClass('noOut');
					$j(this).addClass('notOpacity');
					$j('.tile').each(function(){
						if($j(this).hasClass('notOpacity')){$j(this).removeClass('notOpacity');}
						else{
						$j(this).css('opacity','0.5');
						}
					});
					$j(this).children().children('.tileImage').fadeIn('normal').css('zIndex','110');
				}
				else {
					if(!$j(this).hasClass('noOut')){
						$j(this).addClass('noOut');
						$j(this).addClass('notOpacity');
						$j('.tile').each(function(){
							if($j(this).hasClass('notOpacity')){$j(this).removeClass('notOpacity');}
							else{
							$j(this).css('opacity','0.5');
							}
						});
						$j(this).children().children('.tileImage').fadeIn('normal').css('zIndex','110');
					}
				}
			}
		}
		$j('.tile').bind('mouseleave', function(){
			$j('.tile').css('opacity','1');
			if($j(this).hasClass('goRight')){ 
				$j(this).children().children('.tileImage').css('zIndex','100').fadeOut('fast')
				$j(this).removeClass('noOut');
			}
			else {
				if($j(this).hasClass('endLine')) {
					$j(this).children().children('.tileImage').css('zIndex','100').fadeOut('fast')
					$j(this).removeClass('noOut');
				}
				else{
					if($j(this).hasClass('noOut')){
						$j(this).children().children('.tileImage').css('zIndex','100').fadeOut('fast')
						$j(this).removeClass('noOut');
					}
				}
			}
			$j('.tile').css('opacity','1'); 
		});
	});
}

//$j.when(quicksand()).then(function(){alert('aaa');});
function quicksand() {
	// get the action filter option item on page load
  var $filterType = $j('#filterOptions li.active a').attr('class');
	
  // get and assign the ourHolder element to the
	// $holder varible for use later
  var $holder = $j('ul.ourHolder');

  // clone all items within the pre-assigned $holder element
  var $data = $holder.clone();

  // attempt to call Quicksand when a filter option
	// item is clicked
	$j('#filterOptions li a').click(function(e) {
		// reset the active class on all the buttons
		$j('#filterOptions li').removeClass('active');
		
		// assign the class of the clicked filter option
		// element to our $filterType variable
		var $filterType = $j(this).attr('class');
		$j(this).parent().addClass('active');
		
		if ($filterType == 'all') {
			// assign all li items to the $filteredData var when
			// the 'All' filter option is clicked
			var $filteredData = $data.find('li');
		} 
		else {
			// find all li elements that have our required $filterType
			// values for the data-type element
			var $filteredData = $data.find('li[class~=' + $filterType + ']');

		}
		
		// call quicksand and assign transition parameters
		$holder.quicksand($filteredData, {
			duration: 800,
			easing: 'jswing'
		},function(){
			refreshGridGallery();
      initTile();
      tileHover();
      if($j('.portfolio').hasClass('item-direct')){
          directLink();
      } else if($j('.portfolio').hasClass('item-fancybox')) {
          itemFancybox();
      } else {
          showTile();
      }
      if(typeof Cufon != 'undefined'){      
			 Cufon.refresh();
      }
		});		
		
		return false;
	});
} 

function categorySlider() {
        strong = parseInt($j('.strong').css('width'));
        $j('.strong').css('width',strong+'px')
        
        $j('.category-list a').click(function(e){
            e.preventDefault();
            $j('.gallery-portfolio').hide();
            var link = $j(this).attr('id');
            $j('.'+link).show();
        });
        
	var f = 1;
	ulWidth = 0;
	$j('.galery-holder').each(function(){
		liW = $j(this).children('.galery-wrap').children('.galery-slider').children('li').width() + parseInt($j('.galery-slider li').css('marginRight'));
		ulWidth = $j(this).children('.galery-wrap').children('.galery-slider').children('li').size() * liW;
		maxL = 0;
		if($j(this).children('.galery-wrap').children('.galery-slider').children('li').size() <= 5)
		{
			maxL = $j(this).children('.galery-wrap').children('.galery-slider').children('li').size();			
			max = $j(this).children('.galery-wrap').children('.galery-slider').children('li').size();
			$j(this).attr('data-enable', maxL);			
			$j(this).attr('data-max', max);
		}
		else{
			maxL =$j(this).children('.galery-wrap').children('.galery-slider').children('li').size()-5;
			max = $j(this).children('.galery-wrap').children('.galery-slider').children('li').size()-5;
			$j(this).attr('data-enable', maxL);
			$j(this).attr('data-max', max);
		}
		
		mL = maxL;
		
		$j(this).attr('data-ulWidth',ulWidth);
                $j(this).children('ul').css('width',ulWidth);
	});
	
	//$j('.galery-slider').css('width',ulWidth);
	$j('.gall-r').click(function(){
    //console.log();
		if($j(this).parent('.name').siblings('.galery-holder').attr('data-enable') != parseInt($j(this).parent('.name').siblings('.galery-holder').attr('data-max')-($j(this).parent('.name').siblings('.galery-holder').attr('data-max')-3))){
			$j(this).parent('.name').siblings('.galery-holder').children('.galery-wrap').children('.galery-slider').stop('true','true');
			$j(this).parent('.name').siblings('.galery-holder').children('.galery-wrap').children('.galery-slider').animate({"left": "-="+liW+"px"});
			mL=$j(this).parent('.name').siblings('.galery-holder').attr('data-enable')-1;
			$j(this).parent('.name').siblings('.galery-holder').attr('data-enable', mL);
		}
		return false;
	});
	//$j('.galery-slider').css('width',ulWidth);
	$j('.gall-l').click(function(){
    //console.log();
		if($j(this).parent('.name').siblings('.galery-holder').attr('data-enable') != $j(this).parent('.name').siblings('.galery-holder').attr('data-max')){
			$j(this).parent('.name').siblings('.galery-holder').children('.galery-wrap').children('.galery-slider').stop('true','true');
			$j(this).parent('.name').siblings('.galery-holder').children('.galery-wrap').children('.galery-slider').animate({"left": "+="+liW+"px"});
			mL=$j(this).parent('.name').siblings('.galery-holder').attr('data-enable');
			mL++;
			$j(this).parent('.name').siblings('.galery-holder').attr('data-enable', mL);
		}
		return false;
	});
}



function directLink(){
  $j('.tile').parent().click(function(){
      window.location = $j(this).children().children().children('a').attr('href');
  });
}

function itemFancybox(){
  $j(".portfolio .ourHolder li").each(function(){
    var type = 'image';
    var href = ''; 
    
    if($j(this).hasClass('itemType-image')){
      type = 'image';
      href = $j(this).children('.tile').children().children('a').attr('href');
      $j(this).children('.tile').fancybox({
        'type' : type,
        'href' : href,
        'transitionIn'  : 'elastic',
        'transitionOut' : 'elastic',
        'speedIn'   : 600, 
        'speedOut'    : 200, 
        'overlayShow' : true,
        'autoDimensions' : false,
        'width' : $j('.gridgallery').parent().width(),
        'height' : parseInt($j('.gridgallery').parent().width()/1.5)
      });      
    } else if ($j(this).hasClass('itemType-video')){
      type = 'swf';
      href = $j(this).children('.tile').children().children('a').attr('href');
      if(href.indexOf("youtube") != -1){
       href = href.replace(new RegExp("watch\\?v=", "i"), 'v/');
      } else {
        type = 'iframe';
        var regExp = /http:\/\/(www\.)?vimeo.com\/(\d+)($|\/)/;
        var match = href.match(regExp);
        href = "http://player.vimeo.com/video/"+match[2]+"?title=0&amp;byline=0&amp;portrait=0&amp;color=ffffff";
      }
      $j(this).children('.tile').fancybox({
        'type' : type,
        'href' : href,
        'transitionIn'  : 'elastic',
        'transitionOut' : 'elastic',
        'speedIn'   : 600, 
        'speedOut'    : 200, 
        'overlayShow' : true,
        'autoDimensions' : false,
        'width' : $j('.gridgallery').parent().width(),
        'height' : parseInt($j('.gridgallery').parent().width()/1.5)
      }); 
    } else {
      type = 'iframe';
      href = $j(this).children('.tile').children().children('a').attr('href');
      $j(this).children('.tile').click(function(){
        window.open(href);
      });
    }
    
    
  });
}

function portCatShow() {
  $j(".portfolio .port-cat.icon").click(
      (function() {
        $j('.portfolio .port-cat.categories').fadeToggle('slow');
      })
  );
}

function tileHover(){
  $j('.gridgallery .ourHolder .item').each(function(){
    var tileIcon = $j(this).children('.tile').children('.gridgallery-icon');
    
    $j(this).hover(function(){
      tileIcon.css({'background-color' : 'rgba(51, 51, 51, 0.8)'});
      tileIcon.stop(true,true).fadeIn('slow');
    },function(){
      tileIcon.stop(true,true).fadeOut('slow');
      tileIcon.css({'background-color' : 'none'});      
    });    
  });
}