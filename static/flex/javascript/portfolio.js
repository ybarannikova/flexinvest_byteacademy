  $(document).ready(function(){

    //sidebar active/inactive formatting

      $('.nav-sidebar li').click(function(event) {
          $('.nav-sidebar li.active').removeClass('active');
          var $this = $(this);
          if (!$this.hasClass('active')) {
              $this.addClass('active');
          }
          event.preventDefault();
      });

    //functions to format json

    var json_data = function(json) {
      var formatted_json = "";
          for (var key in json) {
            var value = json[key];
            formatted_json +=
                  "<tr data-id='" + value['contract'] +"'><td style='width:7%'><button type='button' class='btn btn-primary' id=button"+value['contract'] + ">"+ value['contract']+"</button> </td>" + 
                  "<td> $" + formatMoney(value['price'])+ "</td>"+
                  "<td>$" + formatMoney(value['current_value']) + "</td>" + 
                  "<td>" + formatPercent(value['change_in_value']) + "%</td>"+
                  "<td>" + value['purchase_date'] + "</td>"+
                  "<td>" + value['maturity'] + "</td>" +"</tr>"+
                  "<tr><td colspan='5' id='info'><div class='collapse details' data-id='" + value['contract'] +"'>stuff here</div></td></tr>"
          }
    return formatted_json;
  };

    var formatted_cashflows = function(json) {
      var formatted_json = 

      "<h4>Details</h4>" +
      "<p> Average annualized yield: "  + formatPercent(json['average_return']) + "%</p>" + 
      "<h5>Cashflows received since contract's purchase: </h5>" +
              "<table class='table table-bordered table-condensed' id='cashflow_table'>" +
          "<tr>" +
            "<th>Date</th>"+
            "<th>Amount ($)</th></tr>" ;
      for (var key in json['cashflows']) {
        var value = json['cashflows'][key];
        formatted_json +=
          "<tr>" +
            "<td>" + value['date'] + "</td>"+
            "<td>" + formatMoney(value['amount']) + "</td></tr>"
                  }
        formatted_json += "<tr>" +
        "<td> Total </td>" +
        "<td>" + json['total'] + "</td>" + 
        "</table>"
      return formatted_json;
    };

      var formatted_transactions = function(json) {
        var formatted_json = "";
            for (var key in json['transactions']) {
              var value = json['transactions'][key];
              formatted_json +=
                    "<tr>" + 
                    "<td>" + value['date']+ "</td>"+
                    "<td>" + value['category'] + "</td>" + 
                    "<td colspan='2' style='width:40%'>" + value['description'] + "</td>"+
                    "<td>" + formatMoney(value['amount']) + "</td>" +"</tr>"
            }

      return formatted_json;
      }

      //default portfolio display

      event.preventDefault();
      $.ajax({
        type:"GET",
        url: '/flex/portfolio/investments',
        success: function(json){
          $("#information_table").css('display', 'none');
          $("#portfolio_caption").html("YOUR INVESTMENTS")
          $("#portfolio_head").html("<tr><th style='width:7%'>Contract</th><th>Price paid</th><th>Current Value</th><th>Change in Value</th><th>Purchase Time</th><th>Maturity Date</th></tr>");
          $("#portfolio_items").html(json_data(json['investments']));
          $(".btn-primary").each(function(){
            $(this).click(function() {
              var target_id = $( $(this).closest('tr')[0] ).attr('data-id');
              $.ajax({
                type:"GET",
                url: '/flex/portfolio/contract',
                data: {'contract' : target_id},
                success: function(json){
                  if ("cashflows" in json['data']) {
                    $('[data-id="'+ target_id +'"].collapse').html(formatted_cashflows(json['data']));}
                    else {
                      $('[data-id="'+ target_id +'"].collapse').html('The contract does not have any returns yet');
                    }
                  $('[data-id="'+ target_id +'"].collapse').collapse('toggle');
                }
              })
            })
          })
        }
      })


      $("#portfolio").on("click", function(event){
        event.preventDefault();
        window.location.href="/flex/portfolio"
      })  

      //activity

      $("#trade_history").on("click", function(event){
        event.preventDefault();
        $.ajax({
        type: "GET",
        url: '/flex/portfolio/activity',
        success: function(json){
          $("#information_table").css('display', 'table');
          $("#portfolio_table").css('height','75%')
          $("#information_table").html("<caption>ACCOUNT BALANCES</caption><tbody class='table rows-fixed'><tr><td>Available Cash</td><td>$" + formatMoney(json['balance']) + "</td></tr></tbody>")
          $("#portfolio_caption").html("TRANSACTION HISTORY")
          $("#portfolio_head").html("<tr><th>Date</th><th>Category</th><th colspan='2' style='width:40%'>Description</th><th>Amount ($)</th></tr>");
          $("#portfolio_items").html(formatted_transactions(json));
          console.log(json)
        }
      });
    }); 



});  
