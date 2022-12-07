$(window).on("load", function () {
  window.setTimeout(function () {
    $("body").removeClass("is-preload");
  }, 100);
});
$(window).on("load", function () {
  window.setTimeout(function () {
    $("#userIcon").removeClass("user-hidder");
    $("#footer").removeClass("user-hidder");
    $("#userIcon").addClass("user-fade");
    $("#footer").addClass("user-fade");
    $("#userIcon").addClass("buzz");
  }, 1200);
});
$(window).on("load", function () {
  window.setTimeout(function () {
    $("#userIcon").removeClass("user-fade");
    $("#footer").removeClass("user-fade");
    $("#userIcon").removeClass("buzz");
  }, 2500);
});
