
//Initializing Variables
$('.jalendar').jalendar();
$(".button-collapse").sideNav();
$(document).ready(function() {
    $('.parallax').parallax();
});
page = 0
$('#tile_lead_model').hide();
$('#hybrid_lead_model').hide();

// Getting Admin Stuff
admin_rights = ( $('#admin_rights').attr('class') == 'True')

if (admin_rights){
    $('.admin_only').show()
}else{
    $('.admin_only').hide()
}

// LEADS ##############

// Gets list of leads
getLeads = function(page, page_type){
    $('.progress').show()

    if(page_type == "leads"){
        callback = function(passed_data){
            data = passed_data.responseJSON
            appendLeads(data);
            $('.progress').hide();
            page++;
        }
        $.ajax({
            url: "leads?phone=true&local=true&page="+page,
            type: "GET",
            //data: JSON.stringify(new_data),
            processData: false,
            dataType: 'json',
            contentType: "application/json; charset=UTF-8",
            complete: callback
        });
    };

    if(page_type == "claimed"){
        callback = function(passed_data){
            data = passed_data.responseJSON
            appendLeads(data, page_type="claimed");
            $('.progress').hide();
            page++;
        }
        $.ajax({
            url: "leads/claimed?page="+page,
            type: "GET",
            //data: JSON.stringify(new_data),
            processData: false,
            dataType: 'json',
            contentType: "application/json; charset=UTF-8",
            complete: callback
        });
    };

    if(page_type == "admin"){
        callback = function(passed_data){
            data = passed_data.responseJSON
            appendLeads(data, page_type="admin");
            $('.progress').hide();
            page++;
        }
        $.ajax({
            url: "leads/admin?phone=true&page="+page,
            type: "GET",
            //data: JSON.stringify(new_data),
            processData: false,
            dataType: 'json',
            contentType: "application/json; charset=UTF-8",
            complete: callback
        });
    };
}

// Gets single lead
getLead = function(passed_data){
    data = passed_data.responseJSON
    console.log(data);

    lead_id = data['id']
    lead_card = $('#lead_modal_'+lead_id);

    console.log('#lead_modal_'+lead_id)

    lead_card.attr('lead_id',lead_id)
    lead_card.find('.edit-btn').attr('disabled', 'disabled');

    lead_card.find('input').each(function(){
        $(this).attr('id', $(this).attr('id')+'_'+lead_id)
        $(this).change(function(){
            lead_card.find('.edit-btn').removeAttr('disabled');
        })
    })

    lead_card.find('#notes').attr('id', 'notes_'+lead_id);
    lead_card.find('#notes_'+lead_id).change(function(){
            lead_card.find('.edit-btn').removeAttr('disabled');
        })

    lead_card.find('#phone_status').attr('id', 'phone_status_'+lead_id);
    lead_card.find('#phone_status_'+lead_id).change(function(){
            lead_card.find('.edit-btn').removeAttr('disabled');
        })

    lead_card.find('label').each(function(){
        $(this).attr('for', $(this).attr('for')+'_'+lead_id)
    })

    lead_card.find('#claim_user_'+lead_id).val(data['claim_user']);
    lead_card.find('#claim_datetime_'+lead_id).val(data['claim_datetime']);

    $('#claimed_'+lead_id).prop( "checked" , data['claimed'])

    lead_card.find('#address_'+lead_id).val(data['address']);
    lead_card.find('#city_'+lead_id).val(data['city']);
    lead_card.find('#zipcode_'+lead_id).val(data['zipcode']);
    lead_card.find('#date_created_'+lead_id).val(data['date_created']);
    lead_card.find('#status_'+lead_id).val(data['status']);

    lead_card.find('#owner_name_'+lead_id).val(data['owner_name']);
    lead_card.find('#owner_address_'+lead_id).val(data['owner_address']);
    lead_card.find('#owner_city_'+lead_id).val(data['owner_city']);
    lead_card.find('#owner_zipcode_'+lead_id).val(data['owner_zipcode']);
    lead_card.find('#owner_phone_'+lead_id).val(data['owner_phone']);

    lead_card.find('#next_contact_date_'+lead_id).val(data['next_contact_date']);
    lead_card.find('#notes_'+lead_id).val(data['notes']);
    lead_card.find('#phone_status_'+lead_id).val(data['phone_status'])

    google_maps_params = data['address']+' '+data['city']+' '+data['zipcode']
    lead_card.find('iframe').attr('src','https://www.google.com/maps/embed/v1/place?q='+ google_maps_params +'&zoom=14&key=AIzaSyCTisQRQa4RxwdThBQvWjAF9pwbHW9F3RY')
    $('.progress').hide();
    $('select').material_select();

    lead_card.find('.edit-btn').click(function(evt){
        //UPDATE LEAD INFO
        evt.stopImmediatePropagation();
        lead_card.find('.edit-btn').attr('disabled', 'disabled');
        lead_card = $('#lead_modal_'+lead_id);
        post_data = {

            'claim_user':$('#claim_user_'+lead_id).val(),
            'claim_datetime':$('#claim_datetime_'+lead_id).val(),
            'claimed':$('#claimed_'+lead_id).prop( "checked" ),

            'address':$('#address_'+lead_id).val(),
            'city':$('#city_'+lead_id).val(),
            'zipcode':$('#zipcode_'+lead_id).val(),
            'date_created':$('#date_created_'+lead_id).val(),
            'status':$('#status_'+lead_id).val(),

            'owner_name':$('#owner_name_'+lead_id).val(),
            'owner_address':$('#owner_address_'+lead_id).val(),
            'owner_city':$('#owner_city_'+lead_id).val(),
            'owner_zipcode':$('#owner_zipcode_'+lead_id).val(),
            'owner_phone':$('#owner_phone_'+lead_id).val(),

            'next_contact_date':$('#next_contact_date_'+lead_id).val(),
            'notes':$('#notes_'+lead_id).val(),
            'phone_status':$('#phone_status_'+lead_id).val()
        }

        $.ajax({
            url: "leads/"+lead_id,
            type: "POST",
            data: JSON.stringify(post_data),
            processData: false,
            dataType: 'json',
            contentType: "application/json; charset=UTF-8",
            complete: function(data){
                Materialize.toast('Lead Updated.', 4000)
                console.log(data)
            }
        });
    })
}

// Appends the LIST of leads to the Lead Card
appendLeads = function(leads, page_type="lead"){

    modalCompleteFunctions = {
        "lead": function(){
            $("#"+$(this).attr('data-id')).remove();
            Materialize.toast('Lead added to Claimed.', 4000);
        },
        "claimed": function(){
            Materialize.toast('!', 4000);
        },
        "admin": function(){
            Materialize.toast('!', 4000);
        }
    };

    for(i = 0; i < leads.length; ++i){
        lead_row = $( "#hybrid_lead_model" ).clone()
        lead_row.show()
        lead_id = leads[i]['id']
        lead_row.attr('id',leads[i]['id'])
        //lead_row.attr('class','lead_model')

        lead_row.find('.address').html(leads[i]['address']);
        lead_row.find('.city').html(leads[i]['city'] + ', ' + leads[i]['zipcode']);
        lead_row.find('.date_created').html("Added " + leads[i]['date_created']);
        lead_row.find('.status').html(leads[i]['status']);

        lead_row.find('.collapsible-header.lead_collapsible').append(leads[i]['address'])
        lead_row.find('.collapsible-body').attr('id', 'lead_modal_'+leads[i]['id'])

        lead_row.find('#lead_detail_list_').attr('id', 'lead_detail_list_'+leads[i]['id'])

        lead_row.find('#lead_modal').attr('id','lead_modal_'+lead_id)
        lead_row.find('#lead_modal_'+lead_id).attr('data-id',lead_id)

        lead_row.find('.claim_btn').attr('data-id',lead_id)

        if (page_type=="lead"){
            lead_row.find('.claim_btn').html('<i class="material-icons left">add_circle_outline</i>claim')
            lead_row.find('.claim_btn').attr('data-tooltip','Click to Claim')
            lead_row.find('.claim_btn').click(function(){
                claimButtonClick($(this).attr('data-id'))
            })
        }else{
            lead_row.find('.claim_btn').html('<i class="material-icons left">cloud</i>Open')
            lead_row.find('.claim_btn').attr('data-tooltip','Open Lead Details')
            lead_row.find('.claim_btn').click(function(){
                $('#lead_modal_'+$(this).attr('data-id')).modal('open');
            });
        }

        lead_row.find('.tooltipped').tooltip({delay: 50});

        lead_row.appendTo( "#"+page_type+"_row" );

        $('.collapsible').collapsible();
        $('#lead_modal_'+lead_id).modal({
            starting_top: '4%', // Starting top style attribute
            ending_top: '10%', // Ending top style attribute
            ready: function(modal, trigger) { // Callback for Modal open. Modal and trigger parameters available.
                $.ajax({
                    url: "leads/"+modal.attr('data-id'),
                    type: "GET",
                    //data: JSON.stringify(post_data),
                    processData: false,
                    dataType: 'json',
                    contentType: "application/json; charset=UTF-8",
                    complete: function(data){
                        getLead(data);
                    }
                });
          },
          complete: function() {
            modalCompleteFunctions[page_type]();
          } // Callback for Modal close
        });
    }
}

claimButtonClick = function(lead_id){
    claimCheck = function(rec_data){
        data = rec_data.responseJSON
        if (!('error' in data)){
            $('#lead_modal_'+lead_id).modal('open');
        }else{
            Materialize.toast(data['error'], 4000);
            $('#'+lead_id).hide()
        }
    }
    $.ajax({
        url: "leads/"+lead_id+"?claim=true",
        type: "POST",
        //data: JSON.stringify(post_data),
        processData: false,
        dataType: 'json',
        contentType: "application/json; charset=UTF-8",
        complete: claimCheck
    });

}

getMoreLeads = function(page_type="leads"){
    getLeads(page, page_type);
    page++;
}

// Brings up a "new" page (i.e., card)
showCard = function(card_id){
    $(".nav_item").removeClass('active');
    $("#nav_"+card_id).addClass('active');
    $(".card-panel").find(".lead_model").each(function(){
        $(this).remove();
    })
    $(".lead_row").find(".lead_model").each(function(){
        $(this).remove();
    })

    page = 0;

    if (card_id == "lead_card"){
        current_page = "leads"
        getMoreLeads("leads")
    }

    if (card_id == "claimed_card"){
        current_page = "claimed"
        getMoreLeads("claimed")
    }

    if (card_id == "admin_card"){
        current_page = "admin"
        getMoreLeads("admin")
    }

    $('.main-card').hide();
    $('#'+card_id).show();
    $('.button-collapse').sideNav('hide');
};

// Gets additional parameters from URL
var page_param = location.search.split('page=')[1]
if (page_param){
    showCard(page_param + "_card");
}