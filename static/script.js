// $(document).on('ready', ()=>{
//     $('#shorten-form').on('submit', function(e) { // CHANGED: Use form submit event
//         e.preventDefault(); // ADDED: Prevent form from refreshing the page
//         var longUrl = $('#long-url').val(); // get the url inside the input
//         console.log(longUrl);
//         // $.ajax({
//         //     url: '/shorten',
//         //     type: 'POST',
//         //     dataType: 'json/application',
//         //     data: {
//         //         'url': longUrl
//         //     }
//         // }).success((data)=>{
//         //     console.log('success', data.status_code)
//         // }).error((request, error)=>{
//         //     alert(JSON.stringify(request));
//         // });
//     });
// });

$(document).ready(function(){
    $('#shorten-form').on('submit', function(event){
        event.preventDefault();
        var longUrl = $('#long-url').val()

        $.ajax({
            url: '/shorten',
            type: 'POST',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({
                'url': longUrl
            }),
            success: function(data){
                console.log('success');
                console.log(data);
                alert(data['shortCode']);
            },
            error: function(response, error){
                alert(response.responseText + " " + response.status);
            }
        });
    });

    $('.del-url').on('click', function(event){
        // Set the modal's attributes for form completion
        // $('#deleteModal').data('delete-id', )
        var shortCode = $(this).attr('data-shortCode');
        $('#deleteModal').attr('data-shortCode', shortCode);
    });

    $('.edit-url').on('click', function(event){
        $(':input', '#editModal').val('');
        var shortCode = $(this).attr('data-shortcode');
        var longURL = $(this).attr('data-longurl');

        $('#editModal').attr('data-shortCode', shortCode);
        $('#current-target').val(longURL);
    });

    $('#editModal').find('.btn-primary').on('click', function(event){
        var shortCode = $('#editModal').attr('data-shortCode');
        var newURL = $('#new-target').val().trim();
        console.log(newURL);
        // console.log(none_or_empty(newURL));
        // console.log($(`a.edit-url[data-shortCode="${shortCode}"]`))
        if (none_or_empty(newURL)){
            alert('The new URL cannot be empty');
            return;
        }
        $.ajax({
            url: '/shorten/' + shortCode,
            type: 'PUT',
            contentType: 'application/json',
            datatype: 'json',
            data: JSON.stringify({
                'url': newURL
            }),
            success: function(data){
                // edit the my_url table in real time here
                console.log(data['updatedAt']);
                $(`td.shortCode-${shortCode}.longUrl`).html(`<a href=${newURL}>${newURL}</a>`);
                $(`td.shortCode-${shortCode}.updatedAt`).html(data['updatedAt']);
                $('#editModal').modal('hide');
            },
            error: function(response, error){
                alert(response.responseText + " " + response.status);
            }
        });
    });

    $('#deleteModal').find('.btn-primary').on('click', function(event){
        var shortCode = $('#deleteModal').attr('data-shortCode');
        
        $.ajax({
            url: '/shorten/' + shortCode,
            type: 'DELETE',
            success: function(data){
                // edit the my_url table in real time here
                $(`tr[data-shortCode=${shortCode}]`).remove();
                console.log('URL with short code: ' + shortCode + ' has been deleted.');
                $('#deleteModal').modal('hide');
            }
        })
    });
});

function none_or_empty(string){
    return string === null || string.trim() === "";
}