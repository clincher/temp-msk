var order, orderForm, ajax_form;

function formatMoney(num) {
    var p = num.toFixed(2).split(".");
    var summ = p[0].split("").reverse().reduce(function(acc, num, i, orig) {
        return  num + (i && !(i % 3) ? " " : "") + acc;
    }, "") + " руб.";
    if (parseInt(p[1]) > 0)
    summ += p[1]+" коп.";
    return summ;
}


function parseCookieOrder(){
    order = JSON.parse($.cookie('order'));
    recalcCart();
}

function recalcCart(){
    $("#cart_link a").show();
    var summ = 0;
    $.each(order, function(k,v){
        var value_int = parseInt(v["order_num"]);
        if (value_int == 0)
            delete order[k];
        else
            order[k]["order_num"] = value_int;

        $("#order-summ-"+k).text(formatMoney(v["order_summ"]))
        $("#product_"+k).val(v["order_num"]);
        summ += parseFloat(v["order_summ"]);
    });

    $("#order_total").text(formatMoney(summ));

    if (summ > 0){
        $("#send-order-button").show();
        $("#order-form").show();
    } else {
        $("#send-order-button").hide();
        $("#order-form").hide();
    }
    $.cookie('order', JSON.stringify(order, null, 2), { expires: 1, path: '/' });
}

$.validator.setDefaults({
    highlight: function(input) {
        $(input).addClass("input-error");
    },
    unhighlight: function(input) {
        $(input).removeClass("input-error");
    }
});

$.validator.addMethod(
    "phone",
    function(value, element) {
        var RE_PHONE = /^(?:(?:8|\+7)(?:[-() ]*\d){10}|(?:[-() ]*\d){5,10})$/;
        return RE_PHONE.test(value);
    },
    "Некорректный номер телефона"
);

$(document).ready(function(){

    if ($.cookie('order'))
        parseCookieOrder();
    else
        order = {}

	$(".show-hide-link").click(function(){
		showHideText($(this));
		return false;
	});

    $(".menu-item-groups").live({
        click: function(){
            var id = $(this).attr("id").replace("menu-item-group-", "")
            $("#menu-sub_groups-"+id).toggle();
            return false;
        }
    });

    orderForm = $("#order-form").validate({
        errorPlacement: function(error, element) {
//            $(".errorlist").remove();
            error.appendTo( element.parent("p") );
        },
        rules: {
            company: {required: true},
            name: {required:true},
            phone: {required:true, phone: true},
            email: {required:true, email: true}
        },
        messages: {
            company: {required: "Введите название компании-заказчика"},
            name: {required:"Введите контактное лицо компании-заказчика"},
            phone: {required:"Введите контактный телефон компании-заказчика"},
            email: {required:"Введите контактный эл. почту компании-заказчика", email: "Некорректная эл. почта"}
        }
    });

    $("#send-order-button").live({
        click: function(){
            var count=0;
            $.each(order, function(){
                count++;
            });
            if (orderForm.form())
                $("#order-form").submit();
            else
                return false;
        }
    });


    $('#product-gallery a').lightBox({containerResizeSpeed: 350});

    $(".add_to_cart").live({
        click: function(){

            var product_id = $(this).attr("product_id");
            if (parseInt($("#product_"+product_id).val().replace(" ", "")) > 0){
                add_product2cart($(this));
            } else {
                delete order[product_id];
            }
            recalcCart();
            return false;
        }
    });

    $(".delete_from_cart").live({
        click: function(){
            var product_id = $(this).attr("product_id");
            delete order[product_id];
            $("#order-summ-"+product_id).text(formatMoney(0))
            $("#product_"+product_id).val(0);
            recalcCart();
            return false;
        }
    });

    $("#recalculate-button").live({
        click: function(){
            $.each($(".add_to_cart"), function(){
                add_product2cart($(this));
            });
            recalcCart();
        }
    });

    var validate_params = {
        errorPlacement: function(error, element) {
//            $(".errorlist").remove();
            error.appendTo( element.parent("p") );
        },
        rules: {
            "sender": {required: true},
            "email": {required:true, email: true},
            "content": {required: true, minlength: 5},
            "captcha_1": {
                required: true,
                minlength: 5
            }
        },

        messages:{
            "sender": {required: "Введите, пожалуйста, имя и фамилию"},
            "email": {
                required: "Адрес электронной почты",
                email: "Некорректный электронной почты"
            },
            "content": {required: "Введите, вопрос или сообщение.", minlength: "Слишком короткий текст"},
            "captcha_1": {
                required: "Пожалуйста, введите код подтверждения", minlength: "На картинке 5 символов"
            }
        }
    }


    $('#message-button').click(function(){
        $.get('/message', function(data){
            $("#dialog").html(data);
            $emtDialog.dialog({
                buttons:{
                    'Отправить': function(){
                        if(ajax_form.form()){
                            $("#overlay").show();
                            $('#message-form').ajaxSubmit({
                                success:function(data) {
                                    $("#dialog").html(data);
                                    ajax_form = $('#message-form').validate(validate_params);
                                    $("#overlay").hide();
                                },
                                error:function() {
                                    $emtDialog.dialog({buttons:{
                                        'Закрыть': function(){
                                            $emtDialog.dialog('close');
                                        }
                                    }});
                                    $emtDialog.html('При отправке произошла ошибка. Пожалуйста, повторите попытку позднее.');
                                    $("#overlay").hide();
                                }
                            });
                        }
                    },
                    'Закрыть': function(){
                        $emtDialog.dialog('close');
                    }
                },
                width:550,
                height:560
            });
            ajax_form = $('#message-form').validate(validate_params);
            $emtDialog.dialog('open');
        });
        return false;

    });

    $emtDialog = $("#dialog").dialog({
        autoOpen: false,
        resizable: true,
        modal: true,
        width:300,
        height:150,
        close: function() {
            $("#dialog").dialog({height:150, width:300, buttons:{}})
            $("#dialog").html('');
        }
    });

});

function add_product2cart(product){
    var product_id = $(product).attr("product_id");
    var order_num = parseInt($("#product_"+product_id).val().replace(" ", ""));
    order[product_id] = {
        "order_num": order_num,
        "order_summ": order_num * parseInt($(product).attr("load")) * parseFloat($(product).attr("price").replace(",", "."))
    }
}

function refreshCaptcha()
{
	randCK = Math.floor( Math.random()*10000000)
	$("#captchaIMG").attr('src', '/supercap/'+ randCK +'.jpg');
	$("#captchaCK").val(randCK);
}

function getBrowserInfo() {
	 var t,v = undefined;
	 if (window.opera) t = 'Opera';
	 else if (document.all) {
	  t = 'IE';
	  var nv = navigator.appVersion;
	  var s = nv.indexOf('MSIE')+5;
	  v = nv.substring(s,s+1);
	 }
	 else if (navigator.appName) t = 'Netscape';
	 return {type:t,version:v};
}
	 
function AddBookmark(a){
	 var url = window.document.location;
	 var title = window.document.title;
	 var b = getBrowserInfo();
	 if (b.type == 'IE' && 7 > b.version && b.version >= 4) window.external.AddFavorite(url,title);
	 else if (b.type == 'Opera') {
	  a.href = url;
	  a.rel = "sidebar";
	  a.title = url+','+title;
	  return true;
	 }
	 else if (b.type == "Netscape") window.sidebar.addPanel(title,url,"");
	 else alert("Нажмите CTRL-D, чтобы добавить страницу в закладки.");
	 return false;
}

function showHideText(element){
	var id_text = element.attr('id');
	var showElement = $('#'+id_text+'-content');
	if (showElement.css('display') == 'none'){
		element.attr('id', id_text+'-link');
		$('<a href="#" id="'+id_text+'" onclick="return showHideText($(this))">скрыть</a>').insertAfter(element);
		element.hide();
		showElement.show();
	} else {
		$("#"+id_text+'-link').attr('id', id_text).show();
		element.remove();
		showElement.hide();
	}
	return false;
}

function unSerialize (str) {
    var urlParams = {};
    var e,
        a = /\+/g,  // Regex for replacing addition symbol with a space
        r = /([^&=]+)=?([^&]*)/g,
        d = function (s) {
            return decodeURIComponent(s.replace(a, " "));
        }


    while (e = r.exec(str))
        urlParams[d(e[1])] = d(e[2]);

    return urlParams;
};
