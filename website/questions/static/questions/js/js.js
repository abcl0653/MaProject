jQuery(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });
});

function copyCode() {
  /* Get the text field */
  var copyText = document.getElementById("sublimeCommand");

  /* Select the text field */
  copyText.select();

  /* Copy the text inside the text field */
  document.execCommand("copy");

  /* Alert the copied text */
//  alert("Copied the text: " + copyText.value);
}