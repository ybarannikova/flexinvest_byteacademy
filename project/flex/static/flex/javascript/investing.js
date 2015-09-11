
$(document).ready(function(){
  // HELPER FUNCTIONS

  var getTranche = function(list, tranche_id) {
    for (i in list) {
      var tranche = list[i];
      if (tranche["tranche_id"] == tranche_id) {
        return tranche
      }
    }
  }

  // Takes in a list of objects, and a key to sort by.
  // Key param can represent a string or number.
  // Has an optional param [reverse], if true, will return reversed sort.
  var sortBy = function(list, key, reverse) {
      reverse = typeof reverse !== 'undefined' ?  reverse : false;
      return list.sort(function(a,b){
          if (reverse==true) {
              c = a, a = b, b = c; 
          }
          if (a[key] < b[key]) {
              return -1
          }
          else if (a[key] > b[key]) {
              return 1
          }
          else {
              return 0
          }
      });
  }

  var formatTranche = function(json) {
    var formatted_json = "";
    for (var i in json) {
      var item = json[i];
      formatted_json += 
          "<tr class='tranche' id='"+ item['tranche_id'] +"'>" +
              "<td>" +
                "<div class='progress'>" + 
                  "<div class='progress-bar progress-bar-success progress-bar-striped active' role='progressbar' aria-valuenow='40' aria-valuemin='0' aria-valuemax='100' style='width:" + 
                    item['funded'] + "%'>" +
                    item['funded'] + "%" +
                  "</div>" + 
                "</div>" + 
              "</td>" +
              "<td>" + formatPercent(item['est_yield']) + "% </td>" +
              "<td> " + item['term'] + " mo. </td>" +
              "<td> $" + formatMoney(item['tranche']) + "</td>" +
              "<td> $" + formatMoney(item['amount_left']) + "</td>" +
              "<td> " + item['time_left'] + " days </td>" +
          "</tr>"
      }
    return formatted_json;
  };

  // END HELPER FUNCTIONS

  $(".filtering").click(function(event){
    event.preventDefault();
  });
  $(".filtering.uni").click(function(event) {
    $(this).parent().find('.filtering').toggleClass("active")
  });
  $(".filtering.multi").click(function(event) {
    $(this).toggleClass("active")
  });



  $("#tranche_loading").hide()
  $(document).ajaxStart(function() {
    $("#tranche_items").css("background-color", "#ddd")
    $("#tranche_div").css("opacity", ".2");
    $("#tranche_loading").show()
  });
  $(document).ajaxStop(function() {
    $("#tranche_items").css("background-color", "white")
    $("#tranche_div").css("opacity", "1");
    $("#tranche_loading").hide()
  });

  var tranches = undefined;
  var ajax_tranches = function(callback){
    var query = [];
    $(".active.filtering").each(function(){
      query.push(this.id);
    });
    query = query.join("+");
    $.ajax({
      type: "GET",
      url: '/flex/api/investing/',
      data: query,
      success: function(json){
        $("#tranche_items").html(formatTranche(json['data']));
        tranches = json['data'];
        callback(tranches)
      } //close success json
    }) //close ajax
  };



  ajax_tranches(function(tranches){
  });

  $(".filtering").click(function(){
    ajax_tranches(function(tranches){
    });
  });

  //SORTING
  $(document).on("click", ".sorting", function(event){
    event.preventDefault();
    key = this.id;
    $(this).find(".glyphicon").each(function(){
      if ( $(this).hasClass("glyphicon-sort") ) {
        $(this).removeClass("glyphicon-sort").addClass("glyphicon-sort-by-attributes-alt");
        tranches = sortBy(tranches, key, true)
        $("#tranche_items").html(formatTranche(tranches));
      }
      else if ( $(this).hasClass("glyphicon-sort-by-attributes-alt") ) {
        $(this).removeClass("glyphicon-sort-by-attributes-alt").addClass("glyphicon-sort-by-attributes");
        tranches = sortBy(tranches, key, false)
        $("#tranche_items").html(formatTranche(tranches));
      }
      else if ( $(this).hasClass("glyphicon-sort-by-attributes") ) {
        $(this).removeClass("glyphicon-sort-by-attributes").addClass("glyphicon-sort-by-attributes-alt");
        tranches = sortBy(tranches, key, true)
        $("#tranche_items").html(formatTranche(tranches));
      }
    })
  })

  //TRANCHE DETAILS
  var populate_footer_data = function(tranche) {
    $("#footer_data").find('#face').html(formatMoney(tranche["face"]));
    $("#footer_data").find("#dated_date").html(tranche["dated_date_year"] + "-" + tranche["dated_date_month"] + "-" + tranche["dated_date_day"]);
    $("#footer_data").find("#maturity").html(tranche["maturity_year"] + "-" + tranche["maturity_month"] + "-" + tranche["maturity_day"]);
    $("#footer_data").find("#payments_per_year").html(tranche["payments_per_year"]);
    $("#footer_data").find("#available").html(formatMoney(tranche["amount_left"]));
    $("#footer_data").find("#est_yield").html(formatPercent(tranche["est_yield"]));
    $("#footer_data").find("#tranche_id").attr({
      "value": tranche["tranche_id"],
    });
    $("#footer_data").find("#num_contracts").attr({
      "max": tranche["num_available"],
    });
  }

  var tranche = null;
  $("#footer_minimize").hide()
  $("#footer_data").hide()
  $(document).on("click", ".tranche", function(event){
    var footer_height = ($(window).height() - $(".navbar").height());
    $("#footer").animate({"height":footer_height});
    $("#footer").css({"border-top":"0px"});
    $("#footer_minimize").show();
    $("#footer_data").show();
    tranche = getTranche(tranches, this.id);
    populate_footer_data(tranche);
  })

  $(document).on("click", "#footer_minimize", function(event){
    $("#footer_minimize").hide()
    $("#footer_data").hide()
    $("#footer").animate({"height":0});
    $("#footer").css({"border-top":"10px #00295A solid"});
  })

  $(document).on("click, change", "#num_contracts", function(event){
    var num_contracts = $(this).val();
    $("#purchase_order_amount").html(formatMoney(num_contracts * tranche["face"]));
  })

});//end document