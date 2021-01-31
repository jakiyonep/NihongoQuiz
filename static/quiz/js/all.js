'use strict'
function confirmation(){
      ret = confirm("Are you sure you want to submit?");
  }

function color_change(pk){
	document.getElementById('original-' + pk).classList.toggle('correction_visible')
}

$('.correction_btn').on('click', function(){
    var id =  $(this).attr("id");
    $('#desc-' + id).slideToggle('normal');
		$('#' + id).toggleClass('correction_button')
});


var dropIs = 0;

$(document).on('click', '.navbar_button', function(event){
	$('#navbar_collapse').css('transform', 'translateY(0)')
})

$(document).scroll(function(){
	$('#navbar_collapse').css('transform', 'translateY(-100%)')
})


var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
  var currentScrollPos = window.pageYOffset;
  if (prevScrollpos > currentScrollPos) {
    document.getElementById("navbar").style.top = "0";
  } else {
    document.getElementById("navbar").style.top = "-200px";
		if (dropIs == 1){
		document.getElementById("navbar_collapse").classList.toggle('menu_drop')
		dropIs = 0
	}
  }
  prevScrollpos = currentScrollPos;

}



function openNav() {
  document.getElementById("articles_sidebar").classList.toggle('open_nav')
}

$(function(){
	$('#sentence_casual_btn').on('click', function(){
		$('.sentence_casual').slideToggle('normal');
	})
})

$(function(){
	$('#sentence_yomi_btn').on('click', function(){
		$('.sentence_yomi').slideToggle('normal');
	})
})

$(function(){
	$('#sentence_en_btn').on('click', function(){
		$('.sentence_en').slideToggle('normal');
	})
})

$(function(){
	$('#question_answer_btn').on('click', function(){
		$('.question_answer').slideToggle('normal');
	})
})

$(function(){
	$('#question_yomi_btn').on('click', function(){
		$('.question_yomi').slideToggle('normal');
	})
})

$(function(){
	$('#question_en_btn').on('click', function(){
		$('.question_en').slideToggle('normal');
	})
})


$(function(){
	$('.answer_button_a').on('click', function() {
		var target_id = $(this).attr('id');
		$('#collapse-' + target_id).slideToggle('slow');
})
});

$(function(){
	$('#collapse_open_button').on('click', function() {
		$('.collapse_target').slideToggle('fast');

})
});

$(document).on('click', '.triger_user_info_subsection_head', function(event){
	event.preventDefault();
	var selected_id = $(this).attr('id')
	var selected_container = $('#' + selected_id + '_container')
	$(selected_container).slideToggle()
	$(selected_container).toggleClass('selected_container')
})

$(document).on('click', '.top_item', function(event){
	event.preventDefault();
	var selected_id = $(this).attr('id')
	var selected_wrapper = $('#' + selected_id + '_wrapper')
	if($(this).hasClass('active')){

	}else{
		$(this).addClass('active')
		$(this).siblings().removeClass('active')
		$(selected_wrapper).siblings().hide()
		$(selected_wrapper).show()
	}
})

$(document).on('click', '.comment_collapse_button', function(event){
	event.preventDefault();
	$('.comment_form_collapse').slideToggle()
})

$(document).on('click', '.reply_collapse_button', function(event){
	event.preventDefault();
	var comment_id = $(this).attr('name')

	$('#reply_' + comment_id + '_form_wrapper').slideToggle()
})

$(document).on('click', '.show_replies', function(event){
	event.preventDefault();
	var comment_id = $(this).attr('name')

	$('#' + comment_id + '_replies_container').slideToggle()
})

$(document).on('click', '.sidebar_head', function (event) {
	$(this).next().slideToggle('fast')
	$(this).classToggle('clicked')
})

/* difficulty switch */
$(document).on('click', '.switch_button', function(event){
	var selected_difficulty = $(this).attr('id')
	var selected_container = "." + selected_difficulty + "_container"
	if($(this).hasClass('active')){

	}else{
		$(this).addClass('active')
		$(this).siblings().removeClass('active')
		$(selected_container).siblings().hide()
		$(selected_container).show()
	}
})

/* terms and conditions */
$(document).on('click', '.terms_check', function(event){
	if($(this).prop("checked")){
		$('.terms_button_container').html(
			'<button type=submit class="button strong_button terms_button">Submit</button>'
		)
	}
	else{
		$('.terms_button_container').html(
			'<div class="button not_checked terms_button">Submit</div>'
		)
	}
})

/* fixed buttons fade in/out */
var lastScrollTop = 0;
$(window).scroll(function(event){
	var st = $(this).scrollTop();
		if (st < lastScrollTop){
			$(".back_top_button").stop().fadeIn("fast")
			$(".side_menu_button").stop().fadeIn("fast")
		} else {
			$(".back_top_button").stop().fadeOut("fast")
			$(".side_menu_button").stop().fadeOut("fast")
		}
	lastScrollTop = st;
})

$(function () {

	$(".back_top_button").click(function () {
		$("body,html").animate({
			scrollTop: 0
		}, 500);
		return false;
	});
});