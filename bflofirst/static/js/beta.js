
//Initializing Variables
$('.jalendar').jalendar();
$(".button-collapse").sideNav();
$(document).ready(function() {
    $('select').material_select();
    $('.parallax').parallax();
});
leads_page = 0

//Brings up a "new" page (i.e., card)
showCard = function(card_id){
    $(".nav_item").removeClass('active');
    $("#nav_"+card_id).addClass('active');

    if (card_id == "lead_card"){
        getLeads(leads_page);
    }
    $('.main-card').hide();
    $('#'+card_id).show();
    $('.button-collapse').sideNav('hide');
};

// Gets additional parameters from URL
var page_param = location.search.split('page=')[1]
if (page_param == "leads"){
    showCard("lead_card");
}



// LEADS ##############

// Gets list of leads
getLeads = function(page){
    $('.progress').show()
    callback = function(passed_data){
        data = passed_data.responseJSON
        console.log(data);
        appendLeads(data);
        $('.progress').hide();
    }
    $.ajax({
        url: "leads?page="+page,
        type: "GET",
        //data: JSON.stringify(new_data),
        processData: false,
        dataType: 'json',
        contentType: "application/json; charset=UTF-8",
        complete: callback
    });
}

// Gets single lead
getLead = function(lead_id){
    callback = function(passed_data){
        data = passed_data.responseJSON
        console.log(data);

        lead_card = $('#lead_modal_'+lead_id);

        lead_card.find('.address').html(data['address']);
        lead_card.find('.city').html(data['city'] + ', ' + data['zipcode']);
        lead_card.find('.date_created').html("Added " + data['date_created']);
        lead_card.find('.status').html("Status: " + data['status']);

        lead_card.find('.owner_name').html(data['owner_name']);
        lead_card.find('.owner_address').html(data['owner_address']);
        lead_card.find('.owner_city').html(data['owner_city'] + ', ' + data['owner_zipcode']);
        lead_card.find('.owner_phone').html(data['owner_phone']);

        google_maps_params = data['owner_address']+' '+data['owner_city']+' '+data['owner_zipcode']
        lead_card.find('iframe').attr('src','https://www.google.com/maps/embed/v1/place?q='+ google_maps_params +'&zoom=14&key=AIzaSyCTisQRQa4RxwdThBQvWjAF9pwbHW9F3RY')
        $('.progress').hide();
    }

    $('.modal-progress').show()
    $.ajax({
        url: "leads/"+lead_id,
        type: "GET",
        //data: JSON.stringify(new_data),
        processData: false,
        dataType: 'json',
        contentType: "application/json; charset=UTF-8",
        complete: callback
    });
}

// Appends the LIST of leads to the Lead Card
appendLeads = function(leads){
    $('#lead_model').hide();
    last_id = ""
    for(i = 0; i < leads.length; ++i){
        lead_card = $( "#lead_model" ).clone()
        lead_card.show()
        lead_card.attr('id',leads[i]['id'])
        lead_card.find('.address').html(leads[i]['address']);
        lead_card.find('.city').html(leads[i]['city'] + ', ' + leads[i]['zipcode']);
        lead_card.find('.date_created').html("Added " + leads[i]['date_created']);
        lead_card.appendTo( "#lead_row" );

        lead_id = leads[i]['id']
        lead_card.find('.modal').attr('data-id',lead_id);

        lead_card.find('.claim_btn').attr('data-target','lead_modal_'+lead_id)
        lead_card.find('#lead_modal').attr('id','lead_modal_'+lead_id)
    };

    var options = [
                {selector: '.container', offset: 0, callback: function() {
                    getLeads(leads_page);
                    leads_page++;
                    }}];
    Materialize.scrollFire(options);

    $(document).ready(function(){
        $('.modal').modal({
            starting_top: '4%', // Starting top style attribute
            ending_top: '10%', // Ending top style attribute
            ready: function(modal, trigger) { // Callback for Modal open. Modal and trigger parameters available.
            getLead(modal.attr('data-id'));
          },
          complete: function() { } // Callback for Modal close
        }
      );
    });
}