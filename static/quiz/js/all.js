function confirmation(){
      ret = confirm("Are you sure you want to submit?");
  }

function color_change(pk){
  document.getElementById("original-"+pk).classList.toggle('correction_toggle');

}


var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
  var currentScrollPos = window.pageYOffset;
  if (prevScrollpos > currentScrollPos) {
    document.getElementById("navbar").style.top = "0";
  } else {
    document.getElementById("navbar").style.top = "-100px";
  }
  prevScrollpos = currentScrollPos;
}
