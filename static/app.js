// const bsTab = new bootstrap.Tab("#myTab");
// bsTab.srow;
// console.log("Hello");
// const tabEl = document.querySelector('button[data-bs-toggle="tab"]');
// tabEl.addEventListener("shown.bs.tab", (event) => {
//   console.log(event.target); // newly activated tab
//   console.log(event.relatedTarget); // previous active tab
// });
//
// $(document).ready(function () {
//   $('li[data-toggle="tab"]').on("show.bs.tab", function (e) {
//     localStorage.setItem("activeTab", $(e.target).attr("href"));
//   });
//   var activeTab = localStorage.getItem("activeTab");
//   if (activeTab) {
//     $('#myTab a[href="' + activeTab + '"]').tab("show");
//   }
// });
$(document).ready(function () {
  $('button[data-bs-toggle="tab"]').on("show.bs.tab", function (e) {
    localStorage.setItem("activeTab", e.target.id);
    console.log(e.target.id);
  });
  var activeTab = localStorage.getItem("activeTab");
  console.log(activeTab);
  if (activeTab) {
    $('#myTab button[id="' + activeTab + '"]').tab("show");
  }
});
