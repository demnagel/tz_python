$(document).ready(function(){

    //Удаление комментария
     $(".del_comment").on('click', function(){
            if(confirm("Вы подтверждаете удаление?")){
                $.ajax({
                    dataType: 'json',
                    type: 'GET',
                    data: { 'comment_id': $(this).attr('data-object') },
                    url: '/ajax',
                    success: function (msg) {
                        console.log(msg)
                        if(msg.del == 1){
                            location.reload()
                            alert('Комментарий удален')
                        }
                        else{
                            alert('Не удалось удалить комментарий')
                        }

                    },
                    error: function (msg) {
                        return false
                    }
                });
            }
            else{
                return false
            }
        })

    //Подгрузка городов
    $("select[name='region_id']").change(function(){
		if($(this).val() == 0) return false
		 $.ajax({
		    dataType: 'json',
            type: 'GET',
            data: {'region_id': $(this).val()},
            url: '/ajax',
            success: function (msg){
                var option = '<option selected value="1">Не указано</option>';
				$.each(msg, function( key, value ) {
                    option +=  '<option value="' + key + '">' + value + '</option>'
                });
                $("select[name='city_id']").empty()
                $("select[name='city_id']").append(option)
            },
            error : function (msg){
				return false
            }
        })
	})

	//Маска
	$(function() {
        $.mask.definitions['~'] = "[+-]";
        $("#mask").mask("+7(999)-999-99-99");
    });

    //Статистика в таб
    $('div[data-win]').on('click', function(){
        $(".city_stat").empty()
        var cl = $(this).attr('data-win')
        var win = $('div[data-win-el]')
        if (!win) {
            return false
        }
        win.each(function (key, el){
            $(el).css('display', 'none')
        })
        $('div[data-win-el=' + cl + ']').css('display', 'block')
        return true
    })

    //Статистика городов
    $('div[data-id_reg]').on('click', function(){
        $.ajax({
		    dataType: 'json',
            type: 'GET',
            data: {'stat_region': $(this).attr('data-id_reg')},
            url: '/ajax',
            success: function (msg){
                var el = '';
				$.each(msg, function( key, value ) {
                    el += "<div class='info'>"
                    el += "    <div class='btn btn--noactive'>" + value[1] + "</div>"
                    el += "    <div class='info__list'>"
                    el += "        <div class='info__list__el'>"
                    el += "            <span>Ид города</span>"
                    el += "            <span class='value'>" + value[0] + "</span>"
                    el += "        </div>"
                    el += "        <div class='info__list__el'>"
                    el += "            <span>Комментариев </span>"
                    el += "            <span class='value'>" + value[2] + "</span>"
                    el += "        </div>"
                    el += "    </div>"
                    el += "</div>"
                });
                $(".city_stat").empty()
                $(".city_stat").append(el)
            },
            error : function (msg){
				return false
            }
        })
    })
 
    //Кнопки в теле страницы
    $('.btn').on('click', function(){
        $('.btn').each(function(key, val){
            $(val).removeClass('active')
        })
        $(this).addClass('active')
    })

    //Метка обязательных полей
    $('.required_field').on('change', function(){
        if($(this).val()){
            $(this).css('border-color', 'grey')
        }
        else{
            $(this).css('border-color', '#ea4c4b')
        }
    })

    //Определение страницы
    function checkPage(){
        var write = false
        var list =$('.top_menu').children('.top_menu_elem');
        var addr = window.location.href
        var regexp = {
           'stat_m': /\/stat/, 
           'comment_m': /\/comment/,
           'view_m': /\/view/,
        };
        
        if(!list){
            return false
        }

        $.each(regexp, function(key, val){
            if (addr.search(val) != -1){
                write = true
                $.each(list,function(k,v){
                    $(v).removeClass('active')
                })
                $('#' + key).addClass('active')
            }
            if(!write){
                $.each(list,function(k,v){
                    $(v).removeClass('active')
                })
                $('#index_m').addClass('active')
            }
        })
    }

    checkPage()
})